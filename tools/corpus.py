#!/usr/bin/env python3
"""Validate and deterministically index every corpus record family."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse, urlunparse

import yaml


class _FrontMatterLoader(yaml.SafeLoader):
    """Safe YAML loader that leaves dates as strings for explicit validation."""


_FrontMatterLoader.yaml_implicit_resolvers = {
    key: [(tag, regex) for tag, regex in values if tag != "tag:yaml.org,2002:timestamp"]
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ("youtube", "academic", "x", "reddit", "substack", "blogs", "podcasts", "conferences", "books", "case-studies", "github")
ACADEMIC_TYPES = {"arxiv", "journal-article", "conference-paper", "book-chapter", "repository-preprint", "thesis"}
ARTIFACT_LEVELS = {"full_text", "transcript", "abstract", "excerpt", "metadata_only", "unavailable", "retrieval_evidence"}
LIFECYCLES = {"discovered", "retrieved", "accepted", "rejected", "blocked"}
CONTENT_TYPES = {"transcript", "paper", "post", "article", "episode", "talk", "book", "case-study", "repository", "discussion"}
RIGHTS_STATUSES = {"third-party", "licensed", "open-license", "public-domain", "permission-granted", "third-party-metadata-and-abstract", "third-party-full-text", "metadata-only", "bounded-public-evidence", "short-evidence-spans-only", "metadata-and-short-evidence-spans-only", "retrieval-evidence-only"}
WEB_MEDIA_PLATFORMS = {"blogs", "podcasts", "books", "conferences", "case-studies", "github"}
WEB_MEDIA_SOURCE_TYPES = {"article", "episode", "book", "book-chapter", "talk", "proceeding", "case-study", "repository", "issue", "discussion"}
WEB_MEDIA_REQUIRED = {"schema_version", "platform", "stable_id", "title", "creator", "publisher", "canonical_url", "published_date", "date_precision", "source_type", "status", "artifact_level", "retrieved_at", "retrieval_method", "provenance", "rights_status", "rights_note", "content_sha256", "relevance_evidence", "evidence", "query_ids"}
YOUTUBE_REQUIRED = ("schema_version", "platform", "stable_id", "title", "publisher", "canonical_url", "published_date", "content_type", "status", "relevance_status", "provenance", "rights_status", "rights_holder", "content_sha256")
YOUTUBE_OPTIONAL = {"duration_seconds", "transcript_source", "rejection_reason", "availability", "license", "caption_error", "segment_count", "relevance_categories", "relevance_evidence", "relevance_spans", "rights_note", "raw_files", "raw_path", "asr_models"}
ACADEMIC_REQUIRED = ("academic_schema_version", "stable_id", "openalex_id", "title", "authors", "publisher", "published_date", "canonical_url", "source_type", "lifecycle", "relevance_status", "relevance_reason", "artifact_level", "rights_status", "rights_holder", "retrieved_at", "provenance", "content_sha256")
TIMESTAMP = re.compile(r"(?m)^(?P<m>\d+):(?P<s>[0-5]\d)(?::(?P<ss>[0-5]\d))?\s+\S")
SLUG_BAD = re.compile(r"[^a-z0-9]+")


class CorpusError(ValueError):
    pass


def slug(value: str) -> str:
    return SLUG_BAD.sub("-", value.lower()).strip("-") or "untitled"


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise CorpusError("canonical_url must be an absolute HTTP(S) URL")
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme.lower(), host, path, "", parsed.query, ""))


def canonical_url(platform: str, url: str, stable_id: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise CorpusError("canonical_url must be an absolute HTTP(S) URL")
    if platform == "youtube":
        host = parsed.netloc.lower().removeprefix("www.")
        found = parsed.path.strip("/") if host == "youtu.be" else parse_qs(parsed.query).get("v", [""])[0]
        if host not in {"youtube.com", "m.youtube.com", "youtu.be"} or found != stable_id:
            raise CorpusError("YouTube URL ID does not match stable_id")
        return f"https://www.youtube.com/watch?v={stable_id}"
    return urlunparse(parsed._replace(fragment=""))


def expected_name(meta: dict[str, object]) -> str:
    return "--".join((str(meta["published_date"]), slug(str(meta["title"])), slug(str(meta["publisher"])), str(meta["stable_id"]))) + ".md"


def parse_document(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise CorpusError("missing or malformed YAML front matter")
    raw, body = text[4:].split("\n---\n", 1)
    try:
        loaded = yaml.load(raw, Loader=_FrontMatterLoader)
    except (yaml.YAMLError, ValueError) as exc:
        raise CorpusError(f"malformed metadata: {exc}") from exc
    if not isinstance(loaded, dict) or any(not isinstance(key, str) for key in loaded):
        raise CorpusError("malformed metadata: front matter must be a mapping")
    return loaded, body


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def evidence_hash(evidence: object) -> str:
    payload = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def format_document(meta: dict[str, object], body: str) -> str:
    order = YOUTUBE_REQUIRED + ("duration_seconds", "transcript_source", "rejection_reason")
    lines = []
    for key in order:
        if key in meta and meta[key] != "":
            value = meta[key]
            if isinstance(value, str) and key in {"title", "publisher", "provenance", "rights_holder", "rejection_reason"}:
                rendered = json.dumps(value, ensure_ascii=False)
            else:
                rendered = str(value).lower() if isinstance(value, bool) else str(value)
            lines.append(f"{key}: {rendered}")
    for key in sorted(set(meta) - set(order)):
        lines.append(f"{key}: {json.dumps(meta[key], ensure_ascii=False) if isinstance(meta[key], (dict, list)) else meta[key]}")
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def _date(value: object, allow_unknown: bool = False) -> bool:
    if allow_unknown and value == "unknown":
        return True
    try:
        date.fromisoformat(str(value)); return True
    except ValueError:
        return False


def _timestamp(value: object) -> bool:
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00")); return True
    except ValueError:
        return False


def transcript_end(body: str) -> int | None:
    ends = []
    for match in TIMESTAMP.finditer(body):
        a, b, c = match.group("m"), match.group("s"), match.group("ss")
        ends.append(int(a) * 60 + int(b) if c is None else int(a) * 3600 + int(b) * 60 + int(c))
    return max(ends) if ends else None


def _validate_youtube(path: Path, meta: dict[str, object], body: str) -> list[str]:
    errors = []
    missing = [key for key in YOUTUBE_REQUIRED if meta.get(key) is None or meta.get(key) == ""]
    if missing: return ["missing required metadata: " + ", ".join(missing)]
    if str(meta["schema_version"]) != "1": errors.append("schema_version must be 1")
    unknown = sorted(set(meta) - set(YOUTUBE_REQUIRED) - YOUTUBE_OPTIONAL)
    if unknown: errors.append("unknown metadata: " + ", ".join(unknown))
    if meta["platform"] != "youtube": errors.append("YouTube record platform must be youtube")
    if meta["content_type"] != "transcript": errors.append("YouTube content_type must be transcript")
    if not _date(meta["published_date"]): errors.append("published_date must be a real YYYY-MM-DD date")
    try:
        normalized = canonical_url("youtube", str(meta["canonical_url"]), str(meta["stable_id"]))
        if normalized != meta["canonical_url"]: errors.append(f"canonical_url is not canonical; use {normalized}")
    except CorpusError as exc: errors.append(str(exc))
    status = meta["status"]
    if status not in {"accepted", "rejected"}: errors.append("status must be accepted or rejected")
    if meta["relevance_status"] not in {"relevant", "irrelevant"}: errors.append("relevance_status must be relevant or irrelevant")
    if status == "accepted" and meta["relevance_status"] != "relevant": errors.append("accepted sources must be relevant")
    if status == "rejected" and not meta.get("rejection_reason"): errors.append("rejected sources require rejection_reason")
    if meta["rights_status"] not in RIGHTS_STATUSES or not meta.get("rights_holder") or not meta.get("provenance"): errors.append("invalid or incomplete rights/provenance metadata")
    if meta["content_sha256"] != body_hash(body): errors.append("content_sha256 does not match body")
    string_meta = {key: str(value) for key, value in meta.items()}
    if path.name != expected_name(string_meta): errors.append(f"noncanonical filename; expected {expected_name(string_meta)}")
    if path.parts[-3:-1] != ("youtube", str(status)): errors.append(f"wrong directory; expected sources/youtube/{status}")
    if not body.strip(): errors.append("transcript is empty")
    try:
        duration = int(meta.get("duration_seconds", ""))
        if duration <= 0: raise ValueError
    except (ValueError, TypeError): errors.append("duration_seconds must be a positive integer")
    else:
        end = transcript_end(body)
        if end is None: errors.append("transcript has no timestamped lines")
        elif status == "accepted" and end < duration * .8: errors.append(f"transcript incomplete: last timestamp {end}s is below 80% of {duration}s")
    return errors


def _validate_academic(path: Path, meta: dict[str, object], body: str) -> list[str]:
    errors = []
    missing = [key for key in ACADEMIC_REQUIRED if meta.get(key) is None or meta.get(key) == ""]
    if missing: return ["missing required academic metadata: " + ", ".join(missing)]
    if meta["academic_schema_version"] != 1: errors.append("academic_schema_version must be 1")
    if meta["source_type"] not in ACADEMIC_TYPES: errors.append("invalid academic source_type")
    if meta["lifecycle"] not in {"accepted", "rejected"}: errors.append("academic lifecycle must be accepted or rejected")
    if meta["artifact_level"] not in {"full_text", "abstract", "metadata_only"}: errors.append("invalid academic artifact_level")
    if not _date(meta["published_date"]): errors.append("published_date must be a real YYYY-MM-DD date")
    if not _timestamp(meta["retrieved_at"]): errors.append("retrieved_at must be an ISO-8601 timestamp")
    if not re.fullmatch(r"W\d+", str(meta["openalex_id"])) or meta["stable_id"] != f"openalex:{meta['openalex_id']}": errors.append("academic stable_id must match openalex_id")
    try: canonical_url("academic", str(meta["canonical_url"]), str(meta["stable_id"]))
    except CorpusError as exc: errors.append(str(exc))
    if meta["lifecycle"] == "accepted" and meta["relevance_status"] != "relevant": errors.append("accepted academic sources must be relevant")
    if meta["lifecycle"] == "rejected" and not meta.get("rejection_reason"): errors.append("rejected academic sources require rejection_reason")
    if meta["artifact_level"] == "full_text" and not meta.get("open_full_text_url"): errors.append("full_text records require open_full_text_url")
    if meta["artifact_level"] == "metadata_only" and "No full text is claimed" not in body: errors.append("metadata_only record must state that no full text is claimed")
    if meta["rights_status"] not in RIGHTS_STATUSES or not meta.get("rights_holder") or not meta.get("provenance"): errors.append("invalid or incomplete rights/provenance metadata")
    if meta["content_sha256"] != body_hash(body): errors.append("content_sha256 does not match body")
    expected_parent = ("academic", str(meta["source_type"]), str(meta["lifecycle"]))
    if path.parts[-4:-1] != expected_parent: errors.append(f"wrong academic directory; expected sources/{'/'.join(expected_parent)}")
    if not path.name.endswith(f"--{str(meta['openalex_id']).lower()}.md"): errors.append("academic filename must end with lowercase OpenAlex ID")
    return errors


def _adapt_evidence(path: Path, meta: dict[str, object], body: str) -> tuple[dict[str, object], list[str]]:
    errors = []
    platform_alias = {"blog": "blogs", "case-study": "case-studies"}
    platform = platform_alias.get(str(meta.get("platform")), str(meta.get("platform")))
    for key in ("title", "platform", "canonical_url", "publisher", "rights_status", "retrieved_via", "retrieved_at"):
        if not meta.get(key): errors.append(f"evidence record missing {key}")
    if platform not in PLATFORMS: errors.append("unsupported evidence platform")
    try: url_key = normalize_url(str(meta.get("canonical_url", "")))
    except CorpusError as exc: errors.append(str(exc)); url_key = str(meta.get("canonical_url", ""))
    if not _date(meta.get("retrieved_at"), allow_unknown=False): errors.append("evidence retrieved_at must be YYYY-MM-DD")
    rights = str(meta.get("rights_status", ""))
    if rights not in RIGHTS_STATUSES: errors.append("invalid evidence rights_status")
    blocked = rights == "retrieval-evidence-only" or "## Contradiction" in body
    adapted = {
        "record_format": "evidence-v1", "platform": platform,
        "stable_id": hashlib.sha256(url_key.encode()).hexdigest()[:24], "title": meta.get("title", ""),
        "publisher": meta.get("publisher", ""), "canonical_url": meta.get("canonical_url", ""),
        "published_date": "unknown", "content_type": "case-study" if platform == "case-studies" else "article",
        "lifecycle": "blocked" if blocked else "retrieved", "relevance_status": "unknown",
        "provenance": meta.get("retrieved_via", ""), "rights_status": rights,
        "rights_holder": meta.get("publisher", ""), "content_sha256": body_hash(body),
        "artifact_level": "retrieval_evidence" if blocked else "excerpt", "path": path.as_posix(),
    }
    return adapted, errors


def _validate_canonical(path: Path, meta: dict[str, object], body: str) -> list[str]:
    required = ("schema_version", "platform", "stable_id", "title", "publisher", "canonical_url", "published_date", "content_type", "lifecycle", "relevance_status", "artifact_level", "retrieved_at", "provenance", "rights_status", "rights_holder", "content_sha256")
    errors = []
    missing = [key for key in required if meta.get(key) is None or meta.get(key) == ""]
    if missing: return ["missing required canonical metadata: " + ", ".join(missing)]
    if meta["schema_version"] != 2: errors.append("schema_version must be 2")
    if meta["platform"] not in PLATFORMS or meta["platform"] in {"youtube", "academic"}: errors.append("canonical v2 platform must be a supported non-specialized platform")
    if meta["content_type"] not in CONTENT_TYPES: errors.append("invalid content_type")
    if meta["lifecycle"] not in LIFECYCLES: errors.append("invalid lifecycle")
    if meta["artifact_level"] not in ARTIFACT_LEVELS: errors.append("invalid artifact_level")
    if not _date(meta["published_date"], allow_unknown=True): errors.append("published_date must be YYYY-MM-DD or explicit unknown")
    if not _timestamp(meta["retrieved_at"]): errors.append("retrieved_at must be an ISO-8601 timestamp")
    try: canonical_url(str(meta["platform"]), str(meta["canonical_url"]), str(meta["stable_id"]))
    except CorpusError as exc: errors.append(str(exc))
    if meta["lifecycle"] == "accepted" and meta["relevance_status"] != "relevant": errors.append("accepted sources must be relevant")
    if meta["lifecycle"] == "rejected" and not meta.get("rejection_reason"): errors.append("rejected sources require rejection_reason")
    if meta["lifecycle"] == "blocked" and not meta.get("retrieval_error"): errors.append("blocked sources require retrieval_error")
    if meta["rights_status"] not in RIGHTS_STATUSES or not meta.get("rights_holder") or not meta.get("provenance"): errors.append("invalid or incomplete rights/provenance metadata")
    if meta["content_sha256"] != body_hash(body): errors.append("content_sha256 does not match body")
    if path.parts[1] != meta["platform"]: errors.append(f"wrong platform directory; expected sources/{meta['platform']}")
    if meta["lifecycle"] in {"accepted", "rejected", "blocked"} and path.parent.name != meta["lifecycle"]: errors.append("canonical finalized record directory must match lifecycle")
    return errors


def _web_media_slug(value: object) -> str:
    return slug(str(value))[:80] or "source"


def _adapt_web_media(path: Path, record: dict[str, object]) -> tuple[dict[str, object], list[str]]:
    errors = []
    missing = sorted(key for key in WEB_MEDIA_REQUIRED if key not in record)
    if missing:
        return dict(record), ["missing required web/media metadata: " + ", ".join(missing)]
    platform = record.get("platform")
    status = record.get("status")
    evidence = record.get("evidence")
    if record.get("schema_version") != 2: errors.append("web/media schema_version must be 2")
    if not isinstance(platform, str) or platform not in WEB_MEDIA_PLATFORMS: errors.append("invalid web/media platform")
    if not isinstance(status, str) or status not in {"accepted", "rejected", "blocked"}: errors.append("invalid web/media status")
    if not isinstance(record.get("source_type"), str) or record.get("source_type") not in WEB_MEDIA_SOURCE_TYPES: errors.append("invalid web/media source_type")
    if not isinstance(record.get("artifact_level"), str) or record.get("artifact_level") not in {"full_text", "transcript", "abstract", "metadata_only", "unavailable"}: errors.append("invalid web/media artifact_level")
    if not isinstance(record.get("rights_status"), str) or record.get("rights_status") not in RIGHTS_STATUSES: errors.append("invalid web/media rights_status")
    for key in ("stable_id", "title", "creator", "publisher", "retrieval_method", "provenance", "rights_note"):
        if not isinstance(record.get(key), str) or not str(record[key]).strip(): errors.append(f"web/media {key} must be a non-empty string")
    try: normalize_url(str(record.get("canonical_url", "")))
    except CorpusError as exc: errors.append(str(exc))
    if not _timestamp(record.get("retrieved_at")): errors.append("web/media retrieved_at must be an ISO-8601 timestamp")
    precision = record.get("date_precision")
    published = record.get("published_date")
    if precision not in {"day", "year", "unknown"}: errors.append("invalid web/media date_precision")
    if published is None:
        if precision != "unknown": errors.append("null published_date requires unknown date_precision")
    elif not _date(published): errors.append("web/media published_date must be a real YYYY-MM-DD date or null")
    if not isinstance(evidence, list):
        errors.append("web/media evidence must be a list")
    else:
        for item in evidence:
            if not isinstance(item, dict) or not all(isinstance(item.get(key), str) and item[key].strip() for key in ("kind", "locator", "text")):
                errors.append("web/media evidence spans require non-empty kind, locator, and text"); break
            if len(item["text"]) > 700: errors.append("web/media evidence span exceeds bounded 700-character limit")
        if record.get("content_sha256") != evidence_hash(evidence): errors.append("content_sha256 does not match evidence")
    if not isinstance(record.get("query_ids"), list) or not record["query_ids"] or not all(isinstance(item, str) and item.strip() for item in record["query_ids"]): errors.append("web/media query_ids must be a non-empty list of strings")
    relevance = record.get("relevance_evidence")
    if not isinstance(relevance, list) or not all(isinstance(item, str) and item.strip() for item in relevance): errors.append("web/media relevance_evidence must contain strings")
    if status == "accepted":
        if not relevance: errors.append("accepted web/media record requires relevance_evidence")
        if not evidence: errors.append("accepted web/media record requires retained evidence")
        if record.get("artifact_level") == "unavailable": errors.append("accepted web/media record cannot be unavailable")
    elif not isinstance(record.get("rejection_reason"), str) or not str(record["rejection_reason"]).strip(): errors.append(f"{status} web/media record requires rejection_reason")
    if record.get("artifact_level") == "full_text" and record.get("rights_status") not in {"licensed", "public-domain", "permission-granted", "open-license"}: errors.append("full_text web/media record lacks affirmative rights")
    if record.get("artifact_level") == "transcript" and record.get("retained_complete_transcript") is not True: errors.append("transcript web/media record requires a retained complete transcript")
    expected = f"{_web_media_slug(record.get('title'))}--{_web_media_slug(record.get('stable_id'))}.json"
    if path.name != expected: errors.append("filename must be title-derived and end in the stable ID")
    if len(path.parts) < 4 or path.parts[0] != "sources" or path.parts[1] != platform or path.parts[-2] != status: errors.append("web/media platform/status path mismatch")
    content_type = "book" if record.get("source_type") == "book-chapter" else record.get("source_type")
    adapted = dict(record)
    adapted.update(
        lifecycle=status, content_type=content_type,
        relevance_status="relevant" if status == "accepted" else "unknown",
        rights_holder=record.get("creator") or record.get("publisher"), path=path.as_posix(),
    )
    return adapted, errors


def documents(root: Path = ROOT) -> list[Path]:
    source_root = root / "sources"
    if not source_root.exists(): return []
    return sorted(path for path in source_root.rglob("*") if path.is_file() and path.suffix in {".md", ".json"} and path.name != "README.md")


def _strict_web_media_errors(root: Path) -> list[str]:
    spec = importlib.util.spec_from_file_location("corpus_web_media_validator", ROOT / "scripts/validate_web_media.py")
    if spec is None or spec.loader is None: return ["cannot load strict web/media validator"]
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    errors, _, _ = module.validate(root, enforce_quotas=False, enforce_ledgers=False)
    return errors


def audit(root: Path = ROOT) -> tuple[list[dict[str, object]], list[str]]:
    records, errors = [], _strict_web_media_errors(root)
    seen: dict[str, dict[str, Path]] = {key: {} for key in ("stable_id", "canonical_url", "content_sha256")}
    for path in documents(root):
        rel = path.relative_to(root)
        if path.suffix == ".json":
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(loaded, dict): raise CorpusError("JSON source record must be an object")
            except (OSError, UnicodeError, json.JSONDecodeError, CorpusError) as exc:
                errors.append(f"{rel}: malformed JSON record: {exc}"); continue
            record, local_errors = _adapt_web_media(rel, loaded)
            errors.extend(f"{rel}: {error}" for error in local_errors)
            # JSON is a distinct web/media record format; never dispatch it as canonical Markdown by version.
            # Web/media hashes identify retained evidence arrays (including the common empty array),
            # not the source itself. Deduplicate these records by source identities only.
            for key in ("stable_id", "canonical_url"):
                value = str(record.get(key, ""))
                identity = normalize_url(value) if key == "canonical_url" and value else value.casefold() if key == "stable_id" else value
                if identity and identity in seen[key]: errors.append(f"{rel}: duplicate {key} also in {seen[key][identity]}")
                elif identity: seen[key][identity] = rel
            records.append(record)
            continue
        try: meta, body = parse_document(path)
        except (OSError, UnicodeError, CorpusError) as exc: errors.append(f"{rel}: {exc}"); continue
        if "academic_schema_version" in meta:
            record = dict(meta); record.update(platform="academic", status=meta.get("lifecycle"), content_type="paper", path=rel.as_posix())
            local_errors = _validate_academic(rel, meta, body)
        elif meta.get("schema_version") == 1 and meta.get("platform") == "youtube":
            record = dict(meta); record.update(lifecycle=meta.get("status"), artifact_level="transcript", path=rel.as_posix())
            local_errors = _validate_youtube(rel, meta, body)
        elif meta.get("schema_version") == 1 and meta.get("platform") in {"x", "reddit", "substack"}:
            # Social acquisition predates canonical v2 but carries equivalent fields.
            # Normalize it for global accounting while retaining lane-level validation.
            retrieved = re.search(r"retrieved (\d{4}-\d{2}-\d{2}T[^;\s]+)", str(meta.get("rights_note", "")))
            record = dict(meta)
            record.update(
                lifecycle=meta.get("status"),
                artifact_level=meta.get("availability"),
                retrieved_at=retrieved.group(1) if retrieved else "",
                path=rel.as_posix(),
            )
            canonical_meta = dict(record)
            canonical_meta["schema_version"] = 2
            local_errors = _validate_canonical(rel, canonical_meta, body)
        elif meta.get("schema_version") is not None:
            record = dict(meta); record["path"] = rel.as_posix()
            local_errors = _validate_canonical(rel, meta, body)
        else:
            record, local_errors = _adapt_evidence(rel, meta, body)
        errors.extend(f"{rel}: {error}" for error in local_errors)
        for key in seen:
            value = str(record.get(key, ""))
            identity = normalize_url(value) if key == "canonical_url" and value else value.casefold() if key == "stable_id" else value
            if identity and identity in seen[key]:
                declared_duplicate = key == "content_sha256" and record.get("lifecycle") == "rejected" and record.get("duplicate_of")
                if not declared_duplicate: errors.append(f"{rel}: duplicate {key} also in {seen[key][identity]}")
            elif identity: seen[key][identity] = rel
        records.append(record)
    return records, errors


def migrate(root: Path = ROOT) -> list[dict[str, str]]:
    legacy = sorted((root / "transcripts" / "youtube").glob("*.md"))
    destinations: set[Path] = set()
    for old in legacy:
        meta, _ = parse_document(old)
        stable_id = str(meta.get("video_id", ""))
        published = str(meta.get("upload_date", ""))
        preview = {"published_date": f"{published[:4]}-{published[4:6]}-{published[6:8]}", "title": meta.get("title", ""), "publisher": meta.get("channel", ""), "stable_id": stable_id}
        destination = root / "sources" / "youtube" / ("rejected" if stable_id == "fVut0ceg2IY" else "accepted") / expected_name(preview)
        if destination in destinations or destination.exists(): raise CorpusError(f"migration collision: {destination}")
        destinations.add(destination)
    if legacy:
        raise CorpusError("legacy migration input remains; run scripts/migrate_legacy_youtube.py")
    return []


def _counts(records: list[dict[str, object]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(record.get(key) or "unknown") for record in records).items()))


def _csv_row(record: dict[str, object]) -> dict[str, object]:
    return {key: re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else value for key, value in record.items()}


def _channel_stats(records: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result = {}
    for platform in PLATFORMS:
        rows = [record for record in records if record["platform"] == platform]
        result[platform] = {
            "discovered": len(rows), "retrieved": sum(r["lifecycle"] in {"retrieved", "accepted", "rejected"} for r in rows),
            "accepted": sum(r["lifecycle"] == "accepted" for r in rows), "rejected": sum(r["lifecycle"] == "rejected" for r in rows),
            "blocked": sum(r["lifecycle"] == "blocked" for r in rows), "by_artifact_level": _counts(rows, "artifact_level") if rows else {},
            "by_lifecycle": _counts(rows, "lifecycle") if rows else {},
            "by_rights_status": _counts(rows, "rights_status") if rows else {},
            "by_provenance": _counts(rows, "provenance") if rows else {},
        }
    return result


def generate(root: Path = ROOT) -> dict[str, object]:
    records, errors = audit(root)
    if errors: raise CorpusError("cannot generate from invalid corpus:\n" + "\n".join(errors))
    records.sort(key=lambda r: (str(r["platform"]), str(r.get("lifecycle")), str(r["stable_id"]), str(r["path"])))
    metadata = root / "metadata"; metadata.mkdir(exist_ok=True)
    fields = ["stable_id", "platform", "title", "publisher", "canonical_url", "published_date", "duration_seconds", "content_type", "status", "lifecycle", "relevance_status", "artifact_level", "rights_status", "content_sha256", "path"]
    with (metadata / "sources.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(_csv_row(record) for record in records)
    rejected = [r for r in records if r["lifecycle"] == "rejected"]
    with (metadata / "rejected-sources.csv").open("w", newline="", encoding="utf-8") as handle:
        fields2 = ["stable_id", "platform", "title", "canonical_url", "rejection_reason", "path"]
        writer = csv.DictWriter(handle, fields2, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(_csv_row(record) for record in rejected)
    accepted = [r for r in records if r["lifecycle"] == "accepted" and r["relevance_status"] == "relevant"]
    stats: dict[str, object] = {
        "schema_version": 2, "total_records": len(records), "discovered_sources": len(records),
        "validated_relevant_sources": len(accepted), "accepted_sources": sum(r["lifecycle"] == "accepted" for r in records),
        "rejected_sources": len(rejected), "retrieved_sources": sum(r["lifecycle"] in {"retrieved", "accepted", "rejected"} for r in records),
        "blocked_sources": sum(r["lifecycle"] == "blocked" for r in records),
        "complete_timestamped_transcripts": sum(r["platform"] == "youtube" and r["lifecycle"] == "accepted" for r in records),
        "by_platform": _counts(records, "platform"), "by_artifact_level": _counts(records, "artifact_level"),
        "by_lifecycle": _counts(records, "lifecycle"), "by_content_type": _counts(records, "content_type"),
        "by_rights_status": _counts(records, "rights_status"), "by_provenance": _counts(records, "provenance"),
        "academic_by_source_type": _counts([r for r in records if r["platform"] == "academic"], "source_type"),
    }
    stats["channels"] = _channel_stats(records)
    (metadata / "statistics.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    platform_rows = "\n".join(
        f"| {p} | {stats['channels'][p]['discovered']} | {stats['channels'][p]['retrieved']} | {stats['channels'][p]['accepted']} | {stats['channels'][p]['rejected']} | {stats['channels'][p]['blocked']} | "
        f"{', '.join(f'{key}: {value}' for key, value in stats['channels'][p]['by_artifact_level'].items()) or '—'} | "
        f"{', '.join(f'{key}: {value}' for key, value in stats['channels'][p]['by_rights_status'].items()) or '—'} | "
        f"{sum(stats['channels'][p]['by_provenance'].values())} records / {len(stats['channels'][p]['by_provenance'])} distinct values |"
        for p in PLATFORMS
    )
    artifact_rows = "\n".join(f"| {k} | {v} |" for k, v in stats["by_artifact_level"].items())
    lifecycle_rows = "\n".join(f"| {k} | {v} |" for k, v in stats["by_lifecycle"].items())
    rights_rows = "\n".join(f"| {k} | {v} |" for k, v in stats["by_rights_status"].items())
    readme = f"""# Self-Learning Organizations Corpus

Open research corpus about self-learning, self-improving, AI-native organizations and recursive organizational feedback loops.

## Corpus status

- Accounted canonical/evidence records: **{stats['total_records']}**
- Accepted relevant sources: **{stats['validated_relevant_sources']}**
- Retrieved records (including accepted/rejected): **{stats['retrieved_sources']}**
- Rejected records: **{stats['rejected_sources']}**
- Blocked retrieval records: **{stats['blocked_sources']}**
- Complete timestamped YouTube transcripts: **{stats['complete_timestamped_transcripts']}**

| Platform | Discovered | Retrieved | Accepted | Rejected | Blocked | Artifact levels | Rights statuses | Provenance coverage |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
{platform_rows}

| Artifact level | Records |
| --- | ---: |
{artifact_rows}

| Lifecycle | Records |
| --- | ---: |
{lifecycle_rows}

| Rights status | Records |
| --- | ---: |
{rights_rows}

## Layout and contracts

- `sources/youtube/<lifecycle>/` contains strict canonical transcript records.
- `sources/academic/<source-type>/<lifecycle>/` contains academic metadata, abstract, or legally available full-text records.
- Web/media platform directories contain strict JSON acquisition records; social and legacy evidence may use canonical Markdown. Dispatch is by record format and path, not schema version alone.
- `schema/source.schema.json` documents the canonical cross-platform contract and academic specialization.
- `metadata/sources.csv`, `metadata/rejected-sources.csv`, and `metadata/statistics.json` are deterministic generated views.
- `research/recursive-loops/` contains the separate 200-loop dependent research DAG; its artifacts are not double-counted as corpus sources.

Canonical validation rejects duplicate stable IDs and normalized URLs globally. Markdown body hashes are also deduplicated; web/media evidence-array hashes are integrity checks because empty or shared bounded evidence is not a source identity. Placeholder `.gitkeep` files and `sources/README.md` are never records. Run `make check` before committing; it verifies regeneration is clean and preserves the dedicated lane gates.

## Counting and rights policy

Only `accepted` + `relevant` records count as validated sources. Artifact levels distinguish full text, transcripts, abstracts, excerpts, metadata-only records, unavailable artifacts, and failed retrieval evidence. Statistics retain platform, lifecycle, artifact, rights-status, and provenance dimensions. A URL to full text does not itself make a record `full_text`; the preserved body must contain it. Third-party content remains subject to the declared rights holder and source terms, and inclusion transfers no ownership.

_This README is generated by `python3 tools/corpus.py generate`._
"""
    (root / "README.md").write_text(readme, encoding="utf-8")
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("command", choices=("audit", "migrate", "generate", "all")); args = parser.parse_args()
    try:
        if args.command in {"migrate", "all"}: print(f"migrated {len(migrate())} legacy documents")
        if args.command in {"generate", "all"}: print(json.dumps(generate(), sort_keys=True))
        records, errors = audit()
        if errors: print("\n".join(errors), file=sys.stderr); return 1
        print(f"validated {len(records)} sources"); return 0
    except (CorpusError, OSError, UnicodeError) as exc:
        print(exc, file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
