#!/usr/bin/env python3
"""Validate the isolated web/media acquisition lane against GOAL.md gates."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
LANES = {
    "blogs": 75,
    "podcasts": 30,
    "books": 25,
    "conferences": 30,
    "case-studies": 50,
    "github": 30,
}
STATUSES = {"accepted", "rejected", "blocked"}
ARTIFACT_LEVELS = {"full_text", "transcript", "abstract", "metadata_only", "unavailable"}
SOURCE_TYPES = {"article", "episode", "book", "book-chapter", "talk", "proceeding", "case-study", "repository", "issue", "discussion"}
REQUIRED = {
    "schema_version", "platform", "stable_id", "title", "creator", "publisher",
    "canonical_url", "published_date", "date_precision", "source_type", "status",
    "artifact_level", "retrieved_at", "retrieval_method", "provenance",
    "rights_status", "rights_note", "content_sha256", "relevance_evidence",
    "evidence", "query_ids",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
TIMESTAMP = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")
BOILERPLATE = re.compile(r"skip to (?:content|main)|privacy policy|cookie settings|sign in|log in|upcoming events|all rights reserved", re.I)


def slug(value: str, limit: int = 80) -> str:
    return (re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")[:limit] or "source")


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower().removeprefix("www.")
    path = parts.path.rstrip("/") or "/"
    kept_query = urllib_parse_query(parts.query)
    return urlunsplit((parts.scheme.lower(), host, path, kept_query, ""))


def urllib_parse_query(query: str) -> str:
    from urllib.parse import parse_qsl, urlencode
    return urlencode(sorted((key, value) for key, value in parse_qsl(query, keep_blank_values=True) if not key.casefold().startswith("utm_") and key.casefold() not in {"gh_src", "ref", "source"}))


def evidence_hash(evidence: list[dict[str, str]]) -> str:
    payload = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def load_ledger(path: Path, errors: list[str]) -> list[dict]:
    if not path.exists():
        errors.append(f"missing ledger: {path.relative_to(ROOT)}")
        return []
    rows = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}:{number}: invalid JSON: {exc}")
    return rows


def validate() -> tuple[list[str], Counter, Counter]:
    errors: list[str] = []
    counts: Counter = Counter()
    artifact_counts: Counter = Counter()
    seen_ids: dict[str, Path] = {}
    seen_urls: dict[str, Path] = {}
    seen_titles: dict[tuple[str, str], Path] = {}

    query_rows = load_ledger(ROOT / "research/web-media-acquisition/query-ledger.jsonl", errors)
    retrieval_rows = load_ledger(ROOT / "research/web-media-acquisition/retrieval-ledger.jsonl", errors)
    query_ids = {row.get("query_id") for row in query_rows}
    if len(query_ids) != len(query_rows):
        errors.append("query ledger contains duplicate query_ids")
    retrieval_ids = {row.get("stable_id") for row in retrieval_rows}
    for lane in LANES:
        if not any(row.get("lane") == lane for row in query_rows):
            errors.append(f"{lane}: no query-ledger entries")

        lane_root = ROOT / "sources" / lane
        for path in sorted(lane_root.glob("*/*.json")):
            try:
                record = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: unreadable JSON: {exc}")
                continue

            missing = sorted(REQUIRED - record.keys())
            if missing:
                errors.append(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")
                continue
            rel = path.relative_to(ROOT)
            expected_filename = f"{slug(record['title'])}--{slug(record['stable_id'])}.json"
            if path.name != expected_filename:
                errors.append(f"{rel}: filename must be title-derived and end in the stable ID")
            if record["schema_version"] != 2:
                errors.append(f"{rel}: schema_version must be 2")
            if record["platform"] != lane:
                errors.append(f"{rel}: platform/path mismatch")
            if record["status"] not in STATUSES or path.parent.name != record["status"]:
                errors.append(f"{rel}: status/path mismatch")
            if record["artifact_level"] not in ARTIFACT_LEVELS:
                errors.append(f"{rel}: invalid artifact_level")
            if record["source_type"] not in SOURCE_TYPES:
                errors.append(f"{rel}: invalid source_type")
            if not isinstance(record["canonical_url"], str) or not record["canonical_url"].startswith(("https://", "http://")):
                errors.append(f"{rel}: invalid canonical_url")
            if record["published_date"] is None and record["date_precision"] != "unknown":
                errors.append(f"{rel}: null date must be explicit unknown")
            if not SHA256.fullmatch(record["content_sha256"]):
                errors.append(f"{rel}: invalid content_sha256")
            elif record["content_sha256"] != evidence_hash(record["evidence"]):
                errors.append(f"{rel}: content_sha256 does not match evidence")
            if record["status"] == "accepted":
                counts[lane] += 1
                artifact_counts[(lane, record["artifact_level"])] += 1
                if not isinstance(record["relevance_evidence"], list) or not record["relevance_evidence"] or not all(isinstance(item, str) and item.strip() for item in record["relevance_evidence"]):
                    errors.append(f"{rel}: accepted record lacks relevance evidence")
                if record["artifact_level"] == "unavailable":
                    errors.append(f"{rel}: accepted record cannot be unavailable")
                if not isinstance(record["evidence"], list) or not record["evidence"]:
                    errors.append(f"{rel}: acceptance lacks retained evidence")
                elif not all(isinstance(e, dict) and e.get("kind") and e.get("locator") and isinstance(e.get("text"), str) and e["text"].strip() for e in record["evidence"]):
                    errors.append(f"{rel}: evidence spans must have non-empty kind, locator, and text")
            if record["artifact_level"] == "full_text" and record["rights_status"] not in {"licensed", "public-domain", "permission-granted", "open-license"}:
                errors.append(f"{rel}: full_text lacks an affirmative rights basis")
            if record["artifact_level"] == "transcript" and not record.get("retained_complete_transcript"):
                errors.append(f"{rel}: transcript artifact requires a retained complete transcript")
            if record["status"] == "accepted" and record.get("transcript_source") and not any(TIMESTAMP.search(e.get("text", "")) for e in record["evidence"]):
                errors.append(f"{rel}: cited timestamped transcript lacks a timestamp in retained evidence")
            if record["status"] == "accepted" and re.search(r"page not found|\b404\b", record["title"], re.I):
                errors.append(f"{rel}: accepted title indicates a missing page")
            if any(len(e.get("text", "")) > 700 for e in record["evidence"]):
                errors.append(f"{rel}: evidence span exceeds bounded 700-character limit")
            if record["status"] == "accepted" and lane in {"blogs", "case-studies"}:
                if any(BOILERPLATE.search(e.get("text", "")) for e in record["evidence"]):
                    errors.append(f"{rel}: accepted source excerpt contains navigation boilerplate")
                if not any(len(e.get("text", "")) >= 180 and e.get("kind") == "excerpt" for e in record["evidence"]):
                    errors.append(f"{rel}: accepted source lacks a substantive publisher excerpt")
            if record["status"] == "accepted" and lane == "conferences":
                proof = record.get("event_proof") or {}
                if record["source_type"] not in {"talk", "proceeding"} or not proof.get("recorded_marker_observed") or not proof.get("duration_or_media_observed"):
                    errors.append(f"{rel}: conference acceptance lacks event/talk/proceeding proof")
            if record["status"] == "accepted" and lane == "github":
                if not isinstance(record.get("organizational_mechanism"), str) or len(record["organizational_mechanism"].strip()) < 20:
                    errors.append(f"{rel}: GitHub acceptance lacks a concrete organizational mechanism")
            if record["status"] == "accepted" and lane == "podcasts":
                if record.get("media_format") != "podcast_episode" or record["source_type"] != "episode":
                    errors.append(f"{rel}: podcast acceptance lacks genuine episode classification")
                if record.get("transcript_available") is not True or record.get("retained_complete_transcript") is not False:
                    errors.append(f"{rel}: podcast transcript availability/retention is dishonest or missing")
                if record["artifact_level"] == "transcript":
                    errors.append(f"{rel}: bounded excerpt cannot claim transcript artifact level")
                if not record.get("transcript_source") or canonical_url(record["transcript_source"]) == canonical_url(record["canonical_url"]):
                    errors.append(f"{rel}: podcast needs distinct episode and transcript/notes sources")
                if not any(e.get("kind") in {"transcript_excerpt", "timestamped-note"} and TIMESTAMP.search(e.get("text", "")) for e in record["evidence"]):
                    errors.append(f"{rel}: podcast lacks a retained timestamped transcript excerpt/note")
            if record["status"] == "accepted" and lane == "books":
                identifiers = record.get("identifiers") or {}
                if not identifiers.get("catalog_id"):
                    errors.append(f"{rel}: book lacks an exact bibliographic catalog identifier")
                if record["creator"] == "Unknown" or record["publisher"] == "Unknown":
                    errors.append(f"{rel}: book lacks exact creator/publisher metadata")
                if not any(e.get("kind") == "bibliographic_metadata" for e in record["evidence"]):
                    errors.append(f"{rel}: book lacks retained bibliographic evidence")
            if not set(record["query_ids"]).issubset(query_ids):
                errors.append(f"{rel}: query_ids absent from query ledger")
            if record["stable_id"] not in retrieval_ids:
                errors.append(f"{rel}: no retrieval-ledger entry")

            for key, value in (
                ("stable_id", record["stable_id"]),
                ("canonical_url", canonical_url(record["canonical_url"])),
            ):
                seen = seen_ids if key == "stable_id" else seen_urls
                if value in seen:
                    errors.append(f"{rel}: duplicate {key} with {seen[value].relative_to(ROOT)}")
                else:
                    seen[value] = path
            title_key = (re.sub(r"\W+", " ", record["title"].casefold()).strip(), record["publisher"].casefold())
            if title_key in seen_titles:
                errors.append(f"{rel}: duplicate normalized title/publisher with {seen_titles[title_key].relative_to(ROOT)}")
            else:
                seen_titles[title_key] = path

    for lane, quota in LANES.items():
        if counts[lane] < quota:
            errors.append(f"{lane}: accepted {counts[lane]} below quota {quota}")
    return errors, counts, artifact_counts


def main() -> int:
    errors, counts, artifact_counts = validate()
    print("accepted=" + json.dumps(dict(sorted(counts.items())), sort_keys=True))
    print("artifact_levels=" + json.dumps({f"{k[0]}:{k[1]}": v for k, v in sorted(artifact_counts.items())}, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("web/media lane validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
