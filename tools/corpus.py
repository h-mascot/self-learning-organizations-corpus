#!/usr/bin/env python3
"""Validate, migrate, and generate the self-learning organizations corpus."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ("youtube", "arxiv", "x", "reddit", "substack", "blogs", "podcasts", "conferences", "books", "case-studies")
REQUIRED = ("schema_version", "platform", "stable_id", "title", "publisher", "canonical_url", "published_date", "content_type", "status", "relevance_status", "provenance", "rights_status", "rights_holder", "content_sha256")
OPTIONAL = (
    "duration_seconds", "transcript_source", "rejection_reason",
    "availability", "license", "caption_error", "segment_count",
    "relevance_categories", "relevance_evidence", "relevance_spans",
    "rights_note", "raw_files", "raw_path", "asr_models",
)
CONTENT_TYPES = {"transcript", "paper", "post", "article", "episode", "talk", "book", "case-study"}
TIMESTAMP = re.compile(r"(?m)^(?P<m>\d+):(?P<s>[0-5]\d)(?::(?P<ss>[0-5]\d))?\s+\S")
SLUG_BAD = re.compile(r"[^a-z0-9]+")


class CorpusError(ValueError):
    pass


def slug(value: str) -> str:
    return SLUG_BAD.sub("-", value.lower()).strip("-") or "untitled"


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
    return parsed._replace(fragment="").geturl()


def expected_name(meta: dict[str, str]) -> str:
    return "--".join((meta["published_date"], slug(meta["title"]), slug(meta["publisher"]), meta["stable_id"])) + ".md"


def parse_document(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise CorpusError("missing or malformed YAML front matter")
    raw, body = text[4:].split("\n---\n", 1)
    meta: dict[str, str] = {}
    for number, line in enumerate(raw.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise CorpusError(f"malformed metadata at line {number}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key or key in meta or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise CorpusError(f"invalid or duplicate metadata key at line {number}")
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('\\"', '"')
        meta[key] = value
    return meta, body


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def format_document(meta: dict[str, str], body: str) -> str:
    order = REQUIRED + ("duration_seconds", "transcript_source", "rejection_reason")
    lines = []
    for key in order:
        if key in meta and meta[key] != "":
            value = str(meta[key])
            if key in {"title", "publisher", "provenance", "rights_holder", "rejection_reason"}:
                value = json.dumps(value, ensure_ascii=False)
            lines.append(f"{key}: {value}")
    for key in sorted(set(meta) - set(order)):
        lines.append(f"{key}: {meta[key]}")
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def transcript_end(body: str) -> int | None:
    ends = []
    for match in TIMESTAMP.finditer(body):
        a, b, c = match.group("m"), match.group("s"), match.group("ss")
        ends.append(int(a) * 60 + int(b) if c is None else int(a) * 3600 + int(b) * 60 + int(c))
    return max(ends) if ends else None


def validate(path: Path, meta: dict[str, str], body: str) -> list[str]:
    errors = []
    missing = [key for key in REQUIRED if not meta.get(key)]
    if missing:
        errors.append("missing required metadata: " + ", ".join(missing))
    if errors:
        return errors
    if meta["schema_version"] != "1": errors.append("schema_version must be 1")
    unknown = sorted(set(meta) - set(REQUIRED) - set(OPTIONAL))
    if unknown: errors.append("unknown metadata: " + ", ".join(unknown))
    if meta["platform"] not in PLATFORMS: errors.append("unsupported platform")
    if meta["content_type"] not in CONTENT_TYPES: errors.append("invalid content_type")
    try: date.fromisoformat(meta["published_date"])
    except ValueError: errors.append("published_date must be a real YYYY-MM-DD date")
    try:
        normalized = canonical_url(meta["platform"], meta["canonical_url"], meta["stable_id"])
        if normalized != meta["canonical_url"]: errors.append(f"canonical_url is not canonical; use {normalized}")
    except CorpusError as exc: errors.append(str(exc))
    if meta["status"] not in {"accepted", "rejected"}: errors.append("status must be accepted or rejected")
    if meta["relevance_status"] not in {"relevant", "irrelevant"}: errors.append("relevance_status must be relevant or irrelevant")
    if meta["status"] == "accepted" and meta["relevance_status"] != "relevant": errors.append("accepted sources must be relevant")
    if meta["status"] == "rejected" and not meta.get("rejection_reason"): errors.append("rejected sources require rejection_reason")
    if meta["rights_status"] not in {"third-party", "licensed", "public-domain", "permission-granted"}: errors.append("invalid rights_status")
    if meta["content_sha256"] != body_hash(body): errors.append("content_sha256 does not match body")
    if path.name != expected_name(meta): errors.append(f"noncanonical filename; expected {expected_name(meta)}")
    expected_parent = Path("sources") / meta["platform"] / meta["status"]
    try: relative_parent = path.resolve().parent.relative_to(ROOT.resolve())
    except ValueError: relative_parent = path.parent
    if relative_parent != expected_parent: errors.append(f"wrong directory; expected {expected_parent}")
    if meta["content_type"] == "transcript":
        if not body.strip(): errors.append("transcript is empty")
        try:
            duration = int(meta.get("duration_seconds", ""))
            if duration <= 0: raise ValueError
        except ValueError: errors.append("duration_seconds must be a positive integer")
        else:
            end = transcript_end(body)
            if end is None: errors.append("transcript has no timestamped lines")
            elif meta["status"] == "accepted" and end < duration * 0.8: errors.append(f"transcript incomplete: last timestamp {end}s is below 80% of {duration}s")
    return errors


def documents(root: Path = ROOT) -> list[Path]:
    return sorted((root / "sources").glob("*/*/*.md")) if (root / "sources").exists() else []


def audit(root: Path = ROOT) -> tuple[list[dict[str, str]], list[str]]:
    records, errors, seen_ids, seen_urls = [], [], {}, {}
    for path in documents(root):
        try: meta, body = parse_document(path)
        except (OSError, UnicodeError, CorpusError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}"); continue
        for error in validate(path if root == ROOT else ROOT / path.relative_to(root), meta, body):
            errors.append(f"{path.relative_to(root)}: {error}")
        for key, seen in (("stable_id", seen_ids), ("canonical_url", seen_urls)):
            value = meta.get(key)
            if value in seen: errors.append(f"{path.relative_to(root)}: duplicate {key} also in {seen[value]}")
            elif value: seen[value] = path.relative_to(root)
        meta["path"] = path.relative_to(root).as_posix()
        records.append(meta)
    return records, errors


def migrate(root: Path = ROOT) -> list[dict[str, str]]:
    legacy = sorted((root / "transcripts" / "youtube").glob("*.md"))
    migrated, prepared = [], []
    destinations: set[Path] = set()
    for old in legacy:
        meta, body = parse_document(old)
        stable_id = meta.pop("video_id")
        rejected = stable_id == "fVut0ceg2IY"
        published = meta.pop("upload_date")
        published = f"{published[:4]}-{published[4:6]}-{published[6:8]}"
        new_meta = {
            "schema_version": "1", "platform": "youtube", "stable_id": stable_id,
            "title": meta["title"], "publisher": meta.pop("channel"),
            "canonical_url": canonical_url("youtube", meta.pop("source_url"), stable_id),
            "published_date": published, "content_type": "transcript",
            "status": "rejected" if rejected else "accepted",
            "relevance_status": "irrelevant" if rejected else "relevant",
            "provenance": "YouTube captions retained from the original repository seed",
            "rights_status": "third-party", "rights_holder": meta["title"] and ("OpenTable UK & Ireland" if rejected else "Y Combinator"),
            "content_sha256": body_hash(body), "duration_seconds": meta["duration_seconds"],
            "transcript_source": meta["transcript_source"],
        }
        if rejected: new_meta["rejection_reason"] = "Unrelated restaurant advertisement retained as a false-positive control"
        destination = root / "sources" / "youtube" / new_meta["status"] / expected_name(new_meta)
        if destination in destinations or destination.exists(): raise CorpusError(f"migration collision: {destination}")
        destinations.add(destination)
        prepared.append((old, destination, new_meta, body))
    for old, destination, new_meta, body in prepared:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(format_document(new_meta, body), encoding="utf-8")
        migrated.append({"old_path": old.relative_to(root).as_posix(), "new_path": destination.relative_to(root).as_posix(), "stable_id": new_meta["stable_id"], "pre_migration_sha256": hashlib.sha256(old.read_bytes()).hexdigest(), "content_sha256": body_hash(body)})
    if legacy:
        manifest = root / "metadata" / "migration-manifest.csv"
        with manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=migrated[0], lineterminator="\n"); writer.writeheader(); writer.writerows(migrated)
        for old in legacy: old.unlink()
    return migrated


def generate(root: Path = ROOT) -> dict[str, object]:
    records, errors = audit(root)
    if errors: raise CorpusError("cannot generate from invalid corpus:\n" + "\n".join(errors))
    metadata = root / "metadata"; metadata.mkdir(exist_ok=True)
    fields = ["stable_id", "platform", "title", "publisher", "canonical_url", "published_date", "duration_seconds", "content_type", "status", "relevance_status", "rights_status", "content_sha256", "path"]
    with (metadata / "sources.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(records)
    rejected = [r for r in records if r["status"] == "rejected"]
    with (metadata / "rejected-sources.csv").open("w", newline="", encoding="utf-8") as handle:
        fields2 = ["stable_id", "platform", "title", "canonical_url", "rejection_reason", "path"]
        writer = csv.DictWriter(handle, fields2, extrasaction="ignore", lineterminator="\n"); writer.writeheader(); writer.writerows(rejected)
    accepted = [r for r in records if r["status"] == "accepted" and r["relevance_status"] == "relevant"]
    stats = {"schema_version": 1, "discovered_sources": len(records), "validated_relevant_sources": len(accepted), "rejected_sources": len(rejected), "complete_timestamped_transcripts": sum(r["content_type"] == "transcript" for r in accepted), "by_platform": dict(sorted(Counter(r["platform"] for r in records).items())), "by_status": dict(sorted(Counter(r["status"] for r in records).items()))}
    (metadata / "statistics.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = "\n".join(f"| {platform} | {stats['by_platform'].get(platform, 0)} |" for platform in PLATFORMS)
    readme = f"""# Self-Learning Organizations Corpus

Open research corpus about self-learning, self-improving, AI-native organizations and recursive organizational feedback loops.

## Corpus status

- Discovered sources (including rejected controls): **{stats['discovered_sources']}**
- Validated relevant sources: **{stats['validated_relevant_sources']}**
- Complete timestamped transcripts: **{stats['complete_timestamped_transcripts']}**
- Rejected sources excluded from validated totals: **{stats['rejected_sources']}**

| Platform | Discovered sources |
| --- | ---: |
{rows}

## Layout and contracts

- `sources/<platform>/accepted/` contains validated, relevant source records.
- `sources/<platform>/rejected/` preserves false positives and other excluded evidence.
- `raw/youtube/` preserves immutable caption/ASR evidence and source metadata.
- `metadata/youtube/` records per-video hashes, relevance spans, and retrieval details.
- `schema/source.schema.json` defines canonical metadata.
- `metadata/sources.csv` is the generated inventory.
- `metadata/rejected-sources.csv` is the generated rejection log.
- `metadata/migration-manifest.csv` maps legacy paths to canonical paths and hashes.
- `metadata/statistics.json` is the generated machine-readable status.
- `research/` contains taxonomy, reports, synthesis, and progress checkpoints.
- `research/recursive-loops/` contains the validated 200-loop dependent research DAG.

Canonical filenames are `<date>--<normalized-title>--<publisher>--<stable-id>.md`. Run `make check` before committing. Run `make generate` after changing corpus records; generated files must remain reproducible.
Run `python3 scripts/validate_youtube.py` for the exact YouTube evidence count and `python3 scripts/validate_genuine_recursive_research.py` for the recursive DAG gate.

## Counting policy

Only `accepted` records with `relevance_status: relevant` count toward validated totals. Timestamped transcripts additionally require non-empty timestamped text whose final timestamp reaches at least 80% of the declared duration. Rejected evidence remains discoverable but never inflates the relevant-source or complete-transcript totals.

## Rights

Repository metadata and original annotations may be reused subject to the repository license. Third-party transcripts remain subject to source-platform terms and original rights holders. Inclusion does not transfer ownership; each record must declare its provenance, rights status, and rights holder.

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
        if errors:
            print("\n".join(errors), file=sys.stderr); return 1
        print(f"validated {len(records)} sources")
        return 0
    except (CorpusError, OSError, UnicodeError) as exc:
        print(exc, file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
