#!/usr/bin/env python3
"""Deterministic recovery pipeline for the 200 legacy OpenAlex records.

This module intentionally does not depend on the repository-wide schema while that
schema is being upgraded by the manager.  Its validator enforces the academic lane
contract and every legacy input's disposition independently.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LEGACY_DIR = ROOT / "sources" / "arxiv"
ACADEMIC_DIR = ROOT / "sources" / "academic"
RESEARCH_DIR = ROOT / "research" / "academic"
RAW_DIR = ROOT / "raw" / "academic" / "open-full-text"
SNAPSHOT = RESEARCH_DIR / "legacy-snapshot.json"
OPENALEX_CACHE = RESEARCH_DIR / "openalex-records.json"
AUDIT_LEDGER = RESEARCH_DIR / "audit-ledger.csv"
QUERY_LEDGER = RESEARCH_DIR / "query-ledger.jsonl"
RETRIEVAL_LEDGER = RESEARCH_DIR / "retrieval-ledger.csv"
REJECTION_LEDGER = RESEARCH_DIR / "rejection-ledger.csv"
BLOCKER_LEDGER = RESEARCH_DIR / "blocker-ledger.csv"
FULL_TEXT_ATTEMPT_LEDGER = RESEARCH_DIR / "full-text-attempt-ledger.csv"

SOURCE_TYPES = {
    "arxiv",
    "journal-article",
    "conference-paper",
    "book-chapter",
    "thesis",
    "repository-preprint",
    "other-academic",
}
ARTIFACT_LEVELS = {"full_text", "abstract", "metadata_only", "unavailable"}
LIFECYCLES = {"discovered", "retrieved", "accepted", "rejected", "blocked"}
REUSABLE_LICENSES = {
    "cc0", "cc-by", "cc-by-sa", "public-domain",
    "https://creativecommons.org/publicdomain/zero/1.0/",
}
ORG_TERMS = re.compile(
    r"\b(organization(?:al|s)?|organisation(?:al|s)?|compan(?:y|ies)|firms?|"
    r"enterprises?|business(?:es)?|workplaces?|teams?|subsidiar(?:y|ies)|"
    r"multinational|smes?|supply chains?|ventures?|industr(?:y|ies|ial)|"
    r"management|innovation|knowledge transfer|absorptive capacit|dynamic capabilit|"
    r"organizational learning|organisational learning|competitive advantage)\b",
    re.I,
)
LEARNING_TERMS = re.compile(
    r"\b(learn(?:ing|ed)?|knowledge|absorb(?:ing|ed|s)?|absorpt(?:ion|ive)|feedback|adapt(?:ive|ation)?|"
    r"improv(?:e|ement|ing)|innovat(?:e|ion|ive)|capabilit(?:y|ies)|agility|"
    r"exploration|exploitation|memory|transfer|search|creation|spillover)\b",
    re.I,
)
EXPLICIT_OFF_TOPIC = re.compile(
    r"stochastic parrots|international trade in a knowledge-driven|customer satisfaction model in nano food",
    re.I,
)
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+/\d{7})", re.I)
DOI_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/(10\..+)$", re.I)
TITLE_BAD = re.compile(r"[^a-z0-9]+")


class AcademicError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def normalize_title(value: str) -> str:
    return TITLE_BAD.sub(" ", value.casefold()).strip()


def slug(value: str) -> str:
    return TITLE_BAD.sub("-", value.casefold()).strip("-") or "untitled"


def parse_legacy(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise AcademicError(f"malformed legacy document: {path}")
    raw, body = text[4:].split("\n---\n", 1)
    meta: dict[str, object] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        try:
            meta[key.strip()] = json.loads(value)
        except json.JSONDecodeError:
            meta[key.strip()] = value
    evidence = ""
    if "## Evidence span\n\n" in body:
        evidence = body.split("## Evidence span\n\n", 1)[1].split("\n\n## ", 1)[0].strip()
        evidence = re.sub(r"^> ?", "", evidence, flags=re.M).strip()
    openalex_url = str(meta.get("openalex_url", ""))
    openalex_id = openalex_url.rstrip("/").rsplit("/", 1)[-1]
    if not re.fullmatch(r"W\d+", openalex_id):
        raise AcademicError(f"missing valid OpenAlex ID: {path}")
    return {
        "legacy_path": path.relative_to(ROOT).as_posix(),
        "legacy_sha256": sha256_bytes(path.read_bytes()),
        "openalex_id": openalex_id,
        "legacy_metadata": meta,
        "legacy_evidence": evidence,
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def snapshot() -> list[dict[str, object]]:
    legacy_paths = sorted(LEGACY_DIR.glob("*.md"))
    if not legacy_paths and SNAPSHOT.exists():
        payload = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        records = payload.get("records", [])
        if payload.get("record_count") == 200 and len(records) == 200:
            return records
        raise AcademicError("existing legacy snapshot is incomplete")
    records = [parse_legacy(path) for path in legacy_paths]
    if len(records) != 200:
        raise AcademicError(f"expected exactly 200 legacy records, found {len(records)}")
    ids = [str(record["openalex_id"]) for record in records]
    if len(ids) != len(set(ids)):
        raise AcademicError("legacy OpenAlex IDs are not unique")
    payload = {
        "schema_version": 1,
        "created_at": "2026-07-12T00:00:00+00:00",
        "record_count": len(records),
        "records": records,
    }
    write_json(SNAPSHOT, payload)
    return records


def load_snapshot() -> list[dict[str, object]]:
    if not SNAPSHOT.exists():
        return snapshot()
    payload = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if payload.get("record_count") != 200 or len(records) != 200:
        raise AcademicError("legacy snapshot does not account for exactly 200 records")
    return records


def request_json(url: str, attempts: int = 3) -> tuple[dict[str, object], int]:
    request = urllib.request.Request(url, headers={"User-Agent": "academic-recovery/1.0 (mailto:corpus-research@example.com)"})
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.load(response), int(response.status)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            if attempt < attempts:
                time.sleep(attempt)
    raise AcademicError(f"request failed after {attempts} attempts: {url}: {last}")


def fetch_openalex() -> list[dict[str, object]]:
    records = load_snapshot()
    results: list[dict[str, object]] = []
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    batches = [records[index:index + 50] for index in range(0, len(records), 50)]
    with QUERY_LEDGER.open("w", encoding="utf-8") as log:
        for index, batch in enumerate(batches, 1):
            ids = [str(record["openalex_id"]) for record in batch]
            filter_value = quote("|".join(ids), safe="")
            url = f"https://api.openalex.org/works?filter=openalex_id:{filter_value}&per-page=100&mailto=corpus-research@example.com"
            started = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            try:
                result, status = request_json(url)
                outcome, error = "success", ""
                found = result.get("results", [])
                if not isinstance(found, list) or len(found) != len(ids):
                    raise AcademicError(f"batch {index} returned {len(found) if isinstance(found, list) else 'invalid'} of {len(ids)} records")
                results.extend(found)
            except AcademicError as exc:
                status, outcome, error = 0, "blocked", str(exc)
            log.write(json.dumps({
                "sequence": index, "retrieved_at": started, "service": "OpenAlex",
                "query_family": "legacy-openalex-id-audit", "openalex_ids": ids,
                "url": url, "http_status": status, "outcome": outcome, "error": error,
            }, sort_keys=True) + "\n")
    if len(results) != 200:
        raise AcademicError(f"OpenAlex retrieval incomplete: {len(results)}/200")
    results.sort(key=lambda item: str(item["id"]))
    write_json(OPENALEX_CACHE, {
        "schema_version": 1,
        "retrieved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "record_count": len(results),
        "records": results,
    })
    return results


def reconstruct_abstract(inverted: object) -> str:
    if not isinstance(inverted, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for word, indexes in inverted.items():
        if isinstance(indexes, list):
            positions.extend((int(index), str(word)) for index in indexes)
    return " ".join(word for _, word in sorted(positions))


def arxiv_id(work: dict[str, object]) -> str:
    candidates: list[str] = []
    ids = work.get("ids") or {}
    if isinstance(ids, dict):
        candidates.extend(str(value) for value in ids.values() if value)
    for location in work.get("locations") or []:
        if isinstance(location, dict):
            candidates.extend(str(location.get(key) or "") for key in ("landing_page_url", "pdf_url"))
    for candidate in candidates:
        match = ARXIV_RE.search(candidate)
        if match:
            return match.group(1).removesuffix(".pdf")
    return ""


def source_type(work: dict[str, object]) -> str:
    if arxiv_id(work):
        return "arxiv"
    work_type = str(work.get("type") or "").casefold()
    primary = work.get("primary_location") or {}
    best = work.get("best_oa_location") or {}
    source = primary.get("source") if isinstance(primary, dict) else {}
    source_kind = str((source or {}).get("type") or "").casefold() if isinstance(source, dict) else ""
    raw_types = " ".join(
        str(location.get("raw_type") or "") for location in work.get("locations") or [] if isinstance(location, dict)
    ).casefold()
    if isinstance(best, dict):
        raw_types += " " + str(best.get("raw_type") or "").casefold()
    venue_text = venue(work).casefold()
    doi_text = str(work.get("doi") or "").casefold()
    if work_type in {"dissertation"} or "dissertation" in raw_types or "thesis" in raw_types:
        return "thesis"
    if (work_type in {"book", "book-chapter", "reference-entry"} or "book-chapter" in raw_types
            or "chapter in book" in raw_types or "handbook" in venue_text or re.search(r"\.ch\d+$", doi_text)):
        return "book-chapter"
    if work_type in {"proceedings-article"} or "proceedings" in raw_types or "conference" in raw_types:
        return "conference-paper"
    if source_kind == "repository" or work_type in {"preprint", "report", "working-paper"}:
        return "repository-preprint"
    if source_kind == "journal":
        return "journal-article"
    if work_type == "article":
        return "journal-article"
    return "other-academic"


def canonical_url(work: dict[str, object]) -> str:
    aid = arxiv_id(work)
    if aid:
        return f"https://arxiv.org/abs/{aid}"
    doi = str(work.get("doi") or "")
    if DOI_RE.match(doi):
        return "https://doi.org/" + DOI_RE.match(doi).group(1).lower()  # type: ignore[union-attr]
    primary = work.get("primary_location") or {}
    if isinstance(primary, dict) and primary.get("landing_page_url"):
        return str(primary["landing_page_url"])
    return str(work["id"])


def venue(work: dict[str, object]) -> str:
    primary = work.get("primary_location") or {}
    if isinstance(primary, dict):
        source = primary.get("source") or {}
        if isinstance(source, dict) and source.get("display_name"):
            return str(source["display_name"])
        if primary.get("raw_source_name"):
            return str(primary["raw_source_name"])
    best = work.get("best_oa_location") or {}
    if isinstance(best, dict) and best.get("raw_source_name"):
        return str(best["raw_source_name"])
    return "Unknown academic venue"


def authors(work: dict[str, object]) -> list[str]:
    values = []
    for authorship in work.get("authorships") or []:
        if isinstance(authorship, dict):
            author = authorship.get("author") or {}
            if isinstance(author, dict) and author.get("display_name"):
                values.append(str(author["display_name"]))
    return values or ["Unknown"]


def relevance(work: dict[str, object], abstract: str) -> tuple[bool, str, list[str]]:
    title = str(work.get("title") or work.get("display_name") or "")
    text = f"{title}\n{abstract}"
    org = sorted(set(match.group(0).casefold() for match in ORG_TERMS.finditer(text)))
    learning = sorted(set(match.group(0).casefold() for match in LEARNING_TERMS.finditer(text)))
    if EXPLICIT_OFF_TOPIC.search(title):
        return False, "Title describes a non-organizational topic or an incidental keyword collision.", (org + learning)[:8]
    construct = bool(re.search(r"\babsorptive capacit(?:y|ies)\b", title, re.I))
    relevant = bool((org and learning) or construct)
    if construct:
        reason = "Title directly studies absorptive capacity, an established organizational learning and knowledge-conversion construct."
    elif relevant:
        reason = "Title/abstract directly connects an organizational unit or business context with learning, knowledge, adaptation, innovation, or improvement."
    else:
        reason = "Available title/abstract does not directly connect organizational entities to a learning or improvement mechanism."
    return relevant, reason, (org + learning)[:12]


def best_oa(work: dict[str, object]) -> dict[str, object]:
    value = work.get("best_oa_location")
    return value if isinstance(value, dict) else {}


def duplicate_keys(work: dict[str, object]) -> list[str]:
    keys = ["openalex:" + str(work["id"]).rsplit("/", 1)[-1].casefold()]
    doi = str(work.get("doi") or "")
    if doi:
        keys.append("doi:" + doi.casefold().removeprefix("https://doi.org/"))
    keys.append("url:" + canonical_url(work).casefold().rstrip("/"))
    keys.append("title:" + normalize_title(str(work.get("title") or work.get("display_name") or "")))
    return keys


def deduplicate(works: list[dict[str, object]]) -> dict[str, str]:
    parent = {str(work["id"]).rsplit("/", 1)[-1]: str(work["id"]).rsplit("/", 1)[-1] for work in works}

    def find(value: str) -> str:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: str, right: str) -> None:
        a, b = find(left), find(right)
        if a != b:
            parent[max(a, b)] = min(a, b)

    seen: dict[str, str] = {}
    for work in works:
        current = str(work["id"]).rsplit("/", 1)[-1]
        for key in duplicate_keys(work):
            if key in seen:
                union(current, seen[key])
            else:
                seen[key] = current
    groups: dict[str, list[str]] = defaultdict(list)
    for value in parent:
        groups[find(value)].append(value)
    duplicates: dict[str, str] = {}
    by_id = {str(work["id"]).rsplit("/", 1)[-1]: work for work in works}
    for members in groups.values():
        if len(members) < 2:
            continue
        def quality(value: str) -> tuple[int, int, str]:
            work = by_id[value]
            return (bool(work.get("doi")), bool(work.get("abstract_inverted_index")), value)
        winner = max(members, key=quality)
        for member in members:
            if member != winner:
                duplicates[member] = winner
    return duplicates


def format_frontmatter(meta: dict[str, object]) -> str:
    return "---\n" + "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in meta.items()) + "\n---\n"


def record_body(meta: dict[str, object], abstract: str, legacy_evidence: str, full_text: str = "") -> str:
    evidence = abstract or legacy_evidence or "No abstract or full text was available from the audited public metadata."
    sections = [
        f"# {meta['title']}",
        "## Relevance decision",
        str(meta["relevance_reason"]),
        "## Preserved evidence",
        evidence,
    ]
    if full_text:
        sections.extend(["## Legally retrieved full text", full_text])
    sections.extend([
        "## Artifact honesty",
        f"Artifact level: `{meta['artifact_level']}`. "
        + ("The complete extracted text is preserved above under the declared reusable license." if full_text else "No full text is claimed by this record."),
    ])
    return "\n\n".join(sections).rstrip() + "\n"


def load_works() -> list[dict[str, object]]:
    if not OPENALEX_CACHE.exists():
        return fetch_openalex()
    payload = json.loads(OPENALEX_CACHE.read_text(encoding="utf-8"))
    works = payload.get("records", [])
    if payload.get("record_count") != 200 or len(works) != 200:
        raise AcademicError("OpenAlex cache does not contain exactly 200 records")
    return works


def cache_retrieved_at() -> str:
    payload = json.loads(OPENALEX_CACHE.read_text(encoding="utf-8"))
    value = str(payload.get("retrieved_at") or "")
    if not value:
        raise AcademicError("OpenAlex cache lacks retrieval timestamp")
    return value


def migrate() -> Counter[str]:
    legacy = {str(item["openalex_id"]): item for item in load_snapshot()}
    works = load_works()
    retrieved_at = cache_retrieved_at()
    duplicates = deduplicate(works)
    if ACADEMIC_DIR.exists():
        shutil.rmtree(ACADEMIC_DIR)
    rows: list[dict[str, object]] = []
    rejection_rows: list[dict[str, object]] = []
    retrieval_rows: list[dict[str, object]] = []
    blocker_rows: list[dict[str, object]] = []
    attempts = {}
    if FULL_TEXT_ATTEMPT_LEDGER.exists():
        with FULL_TEXT_ATTEMPT_LEDGER.open(encoding="utf-8", newline="") as handle:
            attempts = {row["openalex_id"]: row for row in csv.DictReader(handle)}
    counts: Counter[str] = Counter()
    for work in sorted(works, key=lambda item: str(item["id"])):
        oid = str(work["id"]).rsplit("/", 1)[-1]
        snap = legacy[oid]
        abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
        relevant, reason, terms = relevance(work, abstract)
        duplicate_of = duplicates.get(oid, "")
        status = "rejected" if duplicate_of or not relevant else "accepted"
        lifecycle = "rejected" if status == "rejected" else "accepted"
        rejection_reason = f"Duplicate of OpenAlex {duplicate_of}." if duplicate_of else ("" if relevant else reason)
        kind = source_type(work)
        oa = best_oa(work)
        license_value = str(oa.get("license") or "")
        pdf_url = str(oa.get("pdf_url") or "")
        full_text_path = RAW_DIR / f"{oid.casefold()}.txt"
        full_text = full_text_path.read_text(encoding="utf-8", errors="replace").strip() if full_text_path.exists() and license_value in REUSABLE_LICENSES else ""
        artifact = "full_text" if full_text else ("abstract" if abstract else "metadata_only")
        published = str(work.get("publication_date") or "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published):
            published = f"{int(work.get('publication_year') or 1):04d}-01-01"
        title = str(work.get("title") or work.get("display_name") or "Untitled")
        meta: dict[str, object] = {
            "academic_schema_version": 1,
            "stable_id": f"openalex:{oid}",
            "openalex_id": oid,
            "doi": str(work.get("doi") or "").removeprefix("https://doi.org/"),
            "arxiv_id": arxiv_id(work),
            "title": title,
            "authors": authors(work),
            "publisher": venue(work),
            "published_date": published,
            "canonical_url": canonical_url(work),
            "source_type": kind,
            "lifecycle": lifecycle,
            "relevance_status": "relevant" if relevant else "irrelevant",
            "relevance_reason": reason,
            "relevance_terms": terms,
            "artifact_level": artifact,
            "rights_status": "open-license" if license_value in REUSABLE_LICENSES else "third-party-metadata-and-abstract",
            "rights_license": license_value or None,
            "rights_holder": venue(work),
            "retrieved_at": retrieved_at,
            "provenance": f"OpenAlex {oid} API metadata plus preserved legacy evidence",
            "open_full_text_url": pdf_url or None,
            "duplicate_of": f"openalex:{duplicate_of}" if duplicate_of else None,
            "rejection_reason": rejection_reason or None,
            "legacy_path": str(snap["legacy_path"]),
            "legacy_sha256": str(snap["legacy_sha256"]),
        }
        body = record_body(meta, abstract, str(snap["legacy_evidence"]), full_text)
        meta["content_sha256"] = sha256_text(body)
        filename = f"{published}--{slug(title)[:100]}--{oid.casefold()}.md"
        destination = ACADEMIC_DIR / kind / status / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(format_frontmatter(meta) + body, encoding="utf-8")
        disposition = "duplicate" if duplicate_of else ("accepted" if relevant else "irrelevant")
        row = {
            "legacy_path": snap["legacy_path"], "legacy_sha256": snap["legacy_sha256"],
            "openalex_id": oid, "doi": meta["doi"], "canonical_url": meta["canonical_url"],
            "title": title, "source_type": kind, "disposition": disposition,
            "lifecycle": lifecycle, "artifact_level": artifact,
            "relevance_status": meta["relevance_status"], "duplicate_of": meta["duplicate_of"] or "",
            "output_path": destination.relative_to(ROOT).as_posix(), "reason": rejection_reason or reason,
        }
        rows.append(row)
        if status == "rejected": rejection_rows.append(row)
        attempt = attempts.get(oid, {})
        retrieval_disposition = (
            str(attempt.get("outcome")) if full_text else
            ("blocked-after-attempt" if attempt.get("outcome") == "blocked" else
             ("eligible-explicit-license" if pdf_url and license_value in REUSABLE_LICENSES else
              ("not-redistributable" if pdf_url else "no-pdf-url")))
        )
        retrieval_rows.append({
            "openalex_id": oid, "canonical_url": meta["canonical_url"], "oa_status": (work.get("open_access") or {}).get("oa_status", ""),
            "candidate_full_text_url": pdf_url, "license": license_value,
            "retrieval_disposition": retrieval_disposition,
            "artifact_level": artifact, "content_sha256": meta["content_sha256"],
        })
        if not full_text:
            if attempt.get("outcome") == "blocked":
                blocker, blocker_url = str(attempt.get("error")), str(attempt.get("url"))
            elif pdf_url and license_value not in REUSABLE_LICENSES:
                blocker, blocker_url = "Open PDF lacks an explicit reusable license in audited metadata", pdf_url
            elif not pdf_url:
                blocker, blocker_url = "OpenAlex exposes no direct open PDF URL; no full text is claimed", str(meta["canonical_url"])
            else:
                blocker, blocker_url = "Explicitly licensed PDF remains eligible for a retrieval attempt", pdf_url
            blocker_rows.append({"openalex_id": oid, "blocker": blocker, "url": blocker_url, "retryable": "yes"})
        counts.update([f"status:{status}", f"type:{kind}", f"artifact:{artifact}", f"disposition:{disposition}"])
    write_csv(AUDIT_LEDGER, rows)
    write_csv(REJECTION_LEDGER, rejection_rows)
    write_csv(RETRIEVAL_LEDGER, retrieval_rows)
    write_csv(BLOCKER_LEDGER, blocker_rows)
    for path in sorted(LEGACY_DIR.glob("*.md")):
        path.unlink()
    return counts


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["openalex_id"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_record(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise AcademicError("missing front matter")
    raw, body = text[4:].split("\n---\n", 1)
    meta: dict[str, object] = {}
    for number, line in enumerate(raw.splitlines(), 2):
        if ": " not in line:
            raise AcademicError(f"malformed metadata at line {number}")
        key, value = line.split(": ", 1)
        if key in meta:
            raise AcademicError(f"duplicate metadata key {key}")
        meta[key] = json.loads(value)
    return meta, body


def validate() -> Counter[str]:
    errors: list[str] = []
    paths = sorted(ACADEMIC_DIR.glob("*/*/*.md"))
    if len(paths) != 200:
        errors.append(f"expected 200 academic record files, found {len(paths)}")
    seen_openalex: dict[str, Path] = {}
    accepted_keys: dict[str, Path] = {}
    legacy_paths: set[str] = set()
    counts: Counter[str] = Counter()
    required = {
        "academic_schema_version", "stable_id", "openalex_id", "doi", "arxiv_id", "title", "authors", "publisher",
        "published_date", "canonical_url", "source_type", "lifecycle", "relevance_status", "relevance_reason",
        "relevance_terms", "artifact_level", "rights_status", "rights_license", "rights_holder", "retrieved_at",
        "provenance", "open_full_text_url", "duplicate_of", "rejection_reason", "legacy_path", "legacy_sha256", "content_sha256",
    }
    for path in paths:
        label = path.relative_to(ROOT).as_posix()
        try:
            meta, body = parse_record(path)
        except (AcademicError, OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: {exc}")
            continue
        missing = sorted(required - set(meta))
        if missing: errors.append(f"{label}: missing fields: {', '.join(missing)}")
        oid = str(meta.get("openalex_id", ""))
        if not re.fullmatch(r"W\d+", oid): errors.append(f"{label}: invalid OpenAlex ID")
        if oid in seen_openalex: errors.append(f"{label}: duplicate OpenAlex ID also in {seen_openalex[oid]}")
        seen_openalex[oid] = path
        legacy_paths.add(str(meta.get("legacy_path", "")))
        kind = str(meta.get("source_type", ""))
        lifecycle = str(meta.get("lifecycle", ""))
        artifact = str(meta.get("artifact_level", ""))
        if kind not in SOURCE_TYPES: errors.append(f"{label}: invalid source_type")
        if lifecycle not in LIFECYCLES: errors.append(f"{label}: invalid lifecycle")
        if artifact not in ARTIFACT_LEVELS: errors.append(f"{label}: invalid artifact_level")
        expected_parent = ACADEMIC_DIR / kind / ("accepted" if lifecycle == "accepted" else "rejected")
        if path.parent != expected_parent: errors.append(f"{label}: path disagrees with source_type/lifecycle")
        if kind == "arxiv" and not meta.get("arxiv_id"):
            errors.append(f"{label}: arXiv classification lacks a proven arXiv ID")
        if kind != "arxiv" and meta.get("arxiv_id"):
            errors.append(f"{label}: proven arXiv ID is filed outside arxiv")
        url = str(meta.get("canonical_url", "")); parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc: errors.append(f"{label}: invalid canonical_url")
        if artifact == "full_text" and "## Legally retrieved full text\n\n" not in body:
            errors.append(f"{label}: full_text claim lacks preserved full text")
        if artifact != "full_text" and "## Legally retrieved full text\n\n" in body:
            errors.append(f"{label}: preserved full text is not declared")
        if meta.get("content_sha256") != sha256_text(body): errors.append(f"{label}: content hash mismatch")
        if lifecycle == "accepted":
            if meta.get("relevance_status") != "relevant": errors.append(f"{label}: accepted record is not relevant")
            if meta.get("duplicate_of"): errors.append(f"{label}: accepted record declares duplicate_of")
            for key in ("doi:" + str(meta.get("doi") or "").casefold(), "url:" + url.casefold().rstrip("/"), "title:" + normalize_title(str(meta.get("title") or ""))):
                if key.split(":", 1)[1] and key in accepted_keys: errors.append(f"{label}: accepted duplicate {key} also in {accepted_keys[key]}")
                elif key.split(":", 1)[1]: accepted_keys[key] = path
        else:
            if not meta.get("rejection_reason"): errors.append(f"{label}: rejected record lacks reason")
        counts.update([f"status:{'accepted' if lifecycle == 'accepted' else 'rejected'}", f"type:{kind}", f"artifact:{artifact}"])
    snapshot_paths = {str(item["legacy_path"]) for item in load_snapshot()}
    if legacy_paths != snapshot_paths:
        errors.append(f"legacy accounting mismatch: records={len(legacy_paths)} snapshot={len(snapshot_paths)}")
    if AUDIT_LEDGER.exists():
        with AUDIT_LEDGER.open(encoding="utf-8", newline="") as handle:
            ledger = list(csv.DictReader(handle))
        if len(ledger) != 200 or len({row["legacy_path"] for row in ledger}) != 200:
            errors.append("audit ledger must contain exactly one row for every legacy record")
    else: errors.append("missing audit ledger")
    remaining_legacy = sorted(LEGACY_DIR.glob("*.md"))
    if remaining_legacy:
        errors.append(f"legacy arxiv directory still contains {len(remaining_legacy)} misclassified records")
    if counts["status:accepted"] < 150:
        errors.append(f"academic acceptance gate failed: {counts['status:accepted']} < 150")
    if errors:
        raise AcademicError("\n".join(errors))
    return counts


def retrieve_full_text() -> Counter[str]:
    """Retrieve only PDFs with an explicit reusable license and verify extraction."""
    if not RETRIEVAL_LEDGER.exists():
        migrate()
    if not shutil.which("pdftotext"):
        raise AcademicError("pdftotext is unavailable")
    rows = list(csv.DictReader(RETRIEVAL_LEDGER.open(encoding="utf-8", newline="")))
    works = {str(work["id"]).rsplit("/", 1)[-1]: work for work in load_works()}
    outcomes: Counter[str] = Counter()
    attempts: list[dict[str, object]] = []
    for row in rows:
        if row["retrieval_disposition"] != "eligible-explicit-license":
            continue
        oid, url = row["openalex_id"], row["candidate_full_text_url"]
        pdf = RAW_DIR / f"{oid.casefold()}.pdf"
        txt = RAW_DIR / f"{oid.casefold()}.txt"
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "academic-recovery/1.0"})
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read(50_000_001)
            if len(data) > 50_000_000 or not data.startswith(b"%PDF"):
                raise AcademicError("response is not a bounded PDF")
            pdf.write_bytes(data)
            result = subprocess.run(["pdftotext", str(pdf), str(txt)], capture_output=True, text=True, timeout=90)
            if result.returncode or not txt.exists() or len(txt.read_text(encoding="utf-8", errors="replace").strip()) < 1000:
                raise AcademicError("PDF text extraction failed or produced insufficient text")
            outcomes["retrieved"] += 1
            attempts.append({
                "openalex_id": oid, "url": url, "outcome": "retrieved", "error": "",
                "license": row["license"], "pdf_sha256": sha256_bytes(data),
                "text_sha256": sha256_bytes(txt.read_bytes()), "text_bytes": txt.stat().st_size,
            })
        except (AcademicError, OSError, TimeoutError, urllib.error.URLError, subprocess.TimeoutExpired) as exc:
            pdf.unlink(missing_ok=True); txt.unlink(missing_ok=True)
            pdf_error = str(exc)
            work = works[oid]
            landing = canonical_url(work)
            fallback_url = "https://r.jina.ai/" + landing
            try:
                request = urllib.request.Request(fallback_url, headers={"User-Agent": "academic-recovery/1.0"})
                with urllib.request.urlopen(request, timeout=90) as response:
                    fallback = response.read(5_000_001)
                fallback_text = fallback.decode("utf-8", errors="replace").strip()
                title_words = normalize_title(str(work.get("title") or "")).split()[:5]
                normalized = normalize_title(fallback_text)
                if len(fallback) > 5_000_000 or len(fallback_text) < 5_000:
                    raise AcademicError("Jina fallback did not return a substantive bounded document")
                if not all(word in normalized for word in title_words) or "references" not in normalized or "introduction" not in normalized:
                    raise AcademicError("Jina fallback failed title/full-article structure checks")
                txt.write_text(fallback_text + "\n", encoding="utf-8")
                outcomes["retrieved"] += 1
                attempts.append({
                    "openalex_id": oid, "url": fallback_url, "outcome": "retrieved-html-fallback",
                    "error": f"PDF failed first: {pdf_error}", "license": row["license"], "pdf_sha256": "",
                    "text_sha256": sha256_bytes(txt.read_bytes()), "text_bytes": txt.stat().st_size,
                })
            except (AcademicError, OSError, TimeoutError, urllib.error.URLError) as fallback_exc:
                txt.unlink(missing_ok=True)
                outcomes["blocked"] += 1
                attempts.append({
                    "openalex_id": oid, "url": url, "outcome": "blocked",
                    "error": f"PDF: {pdf_error}; Jina: {fallback_exc}",
                    "license": row["license"], "pdf_sha256": "", "text_sha256": "", "text_bytes": "",
                })
    write_csv(FULL_TEXT_ATTEMPT_LEDGER, attempts)
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("snapshot", "fetch", "migrate", "retrieve", "validate", "all"))
    args = parser.parse_args()
    try:
        if args.command in {"snapshot", "all"}: print(f"snapshotted {len(snapshot())} legacy records")
        if args.command in {"fetch", "all"}: print(f"fetched {len(fetch_openalex())} OpenAlex records")
        if args.command in {"migrate", "all"}: print(json.dumps(migrate(), sort_keys=True))
        if args.command == "retrieve": print(json.dumps(retrieve_full_text(), sort_keys=True))
        if args.command in {"validate", "all"}: print(json.dumps(validate(), sort_keys=True))
        return 0
    except (AcademicError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
