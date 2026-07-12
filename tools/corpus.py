#!/usr/bin/env python3
"""Validate and deterministically index every corpus record family."""

from __future__ import annotations

import argparse
import csv
import hashlib
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
ARTIFACT_LEVELS = {"full_text", "transcript", "abstract", "excerpt", "metadata_only", "retrieval_evidence"}
LIFECYCLES = {"discovered", "retrieved", "accepted", "rejected", "blocked"}
CONTENT_TYPES = {"transcript", "paper", "post", "article", "episode", "talk", "book", "case-study", "repository", "discussion"}
RIGHTS_STATUSES = {"third-party", "licensed", "open-license", "public-domain", "permission-granted", "third-party-metadata-and-abstract", "third-party-full-text", "metadata-only", "short-evidence-spans-only", "metadata-and-short-evidence-spans-only", "retrieval-evidence-only"}
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


def documents(root: Path = ROOT) -> list[Path]:
    source_root = root / "sources"
    if not source_root.exists(): return []
    return sorted(path for path in source_root.rglob("*.md") if path.name != "README.md")


def audit(root: Path = ROOT) -> tuple[list[dict[str, object]], list[str]]:
    records, errors = [], []
    seen: dict[str, dict[str, Path]] = {key: {} for key in ("stable_id", "canonical_url", "content_sha256")}
    for path in documents(root):
        rel = path.relative_to(root)
        try: meta, body = parse_document(path)
        except (OSError, UnicodeError, CorpusError) as exc: errors.append(f"{rel}: {exc}"); continue
        if "academic_schema_version" in meta:
            record = dict(meta); record.update(platform="academic", status=meta.get("lifecycle"), content_type="paper", path=rel.as_posix())
            local_errors = _validate_academic(rel, meta, body)
        elif meta.get("schema_version") == 1:
            record = dict(meta); record.update(lifecycle=meta.get("status"), artifact_level="transcript", path=rel.as_posix())
            local_errors = _validate_youtube(rel, meta, body)
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


def _channel_stats(records: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result = {}
    for platform in PLATFORMS:
        rows = [record for record in records if record["platform"] == platform]
        result[platform] = {
            "discovered": len(rows), "retrieved": sum(r["lifecycle"] in {"retrieved", "accepted", "rejected"} for r in rows),
            "accepted": sum(r["lifecycle"] == "accepted" for r in rows), "rejected": sum(r["lifecycle"] == "rejected" for r in rows),
            "blocked": sum(r["lifecycle"] == "blocked" for r in rows), "by_artifact_level": _counts(rows, "artifact_level") if rows else {},
        }
    return result


def generate(root: Path = ROOT) -> dict[str, object]:
    records, errors = audit(root)
    if errors: raise CorpusError("cannot generate from invalid corpus:\n" + "\n".join(errors))
    records.sort(key=lambda r: (str(r["platform"]), str(r.get("lifecycle")), str(r["stable_id"]), str(r["path"])))
    metadata = root / "metadata"; metadata.mkdir(exist_ok=True)
    fields = ["stable_id", "platform", "title", "publisher", "canonical_url", "published_date", "duration_seconds", "content_type", "status", "lifecycle", "relevance_status", "artifact_level", "rights_status", "content_sha256", "path"]
    with (metadata / "sources.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(records)
    rejected = [r for r in records if r["lifecycle"] == "rejected"]
    with (metadata / "rejected-sources.csv").open("w", newline="", encoding="utf-8") as handle:
        fields2 = ["stable_id", "platform", "title", "canonical_url", "rejection_reason", "path"]
        writer = csv.DictWriter(handle, fields2, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(rejected)
    accepted = [r for r in records if r["lifecycle"] == "accepted" and r["relevance_status"] == "relevant"]
    stats: dict[str, object] = {
        "schema_version": 2, "total_records": len(records), "discovered_sources": len(records),
        "validated_relevant_sources": len(accepted), "accepted_sources": sum(r["lifecycle"] == "accepted" for r in records),
        "rejected_sources": len(rejected), "retrieved_sources": sum(r["lifecycle"] in {"retrieved", "accepted", "rejected"} for r in records),
        "blocked_sources": sum(r["lifecycle"] == "blocked" for r in records),
        "complete_timestamped_transcripts": sum(r["platform"] == "youtube" and r["lifecycle"] == "accepted" for r in records),
        "by_platform": _counts(records, "platform"), "by_artifact_level": _counts(records, "artifact_level"),
        "by_lifecycle": _counts(records, "lifecycle"), "by_content_type": _counts(records, "content_type"),
        "academic_by_source_type": _counts([r for r in records if r["platform"] == "academic"], "source_type"),
    }
    stats["channels"] = _channel_stats(records)
    (metadata / "statistics.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    platform_rows = "\n".join(
        f"| {p} | {stats['channels'][p]['discovered']} | {stats['channels'][p]['retrieved']} | {stats['channels'][p]['accepted']} | {stats['channels'][p]['rejected']} | {stats['channels'][p]['blocked']} |"
        for p in PLATFORMS
    )
    artifact_rows = "\n".join(f"| {k} | {v} |" for k, v in stats["by_artifact_level"].items())
    lifecycle_rows = "\n".join(f"| {k} | {v} |" for k, v in stats["by_lifecycle"].items())
    readme = f"""# Self-Learning Organizations Corpus

Open research corpus about self-learning, self-improving, AI-native organizations and recursive organizational feedback loops.

## Corpus status

- Accounted canonical/evidence records: **{stats['total_records']}**
- Accepted relevant sources: **{stats['validated_relevant_sources']}**
- Retrieved records (including accepted/rejected): **{stats['retrieved_sources']}**
- Rejected records: **{stats['rejected_sources']}**
- Blocked retrieval records: **{stats['blocked_sources']}**
- Complete timestamped YouTube transcripts: **{stats['complete_timestamped_transcripts']}**

| Platform | Discovered | Retrieved | Accepted | Rejected | Blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
{platform_rows}

| Artifact level | Records |
| --- | ---: |
{artifact_rows}

| Lifecycle | Records |
| --- | ---: |
{lifecycle_rows}

## Layout and contracts

- `sources/youtube/<lifecycle>/` contains strict canonical transcript records.
- `sources/academic/<source-type>/<lifecycle>/` contains academic metadata, abstract, or legally available full-text records.
- Other platform directories may contain acquisition evidence or canonical records; their lifecycle and artifact level are reported honestly.
- `schema/source.schema.json` documents the canonical cross-platform contract and academic specialization.
- `metadata/sources.csv`, `metadata/rejected-sources.csv`, and `metadata/statistics.json` are deterministic generated views.
- `research/recursive-loops/` contains the separate 200-loop dependent research DAG; its artifacts are not double-counted as corpus sources.

Canonical validation rejects duplicate stable IDs, normalized URLs, and content hashes globally. Placeholder `.gitkeep` files and `sources/README.md` are never records. Run `make check` before committing; it verifies regeneration is clean and preserves the dedicated YouTube gate.

## Counting and rights policy

Only `accepted` + `relevant` records count as validated sources. Artifact levels distinguish full text, transcripts, abstracts, excerpts, metadata-only records, and failed retrieval evidence. A URL to full text does not itself make a record `full_text`; the preserved body must contain it. Third-party content remains subject to the declared rights holder and source terms, and inclusion transfers no ownership.

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
