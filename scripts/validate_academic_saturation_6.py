#!/usr/bin/env python3
"""Validate post-acceptance academic saturation wave 6."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "academic-saturation-6"
DISPOSITIONS = {"accepted", "rejected", "duplicate", "blocked"}


def jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line.strip()]


def main() -> None:
    rounds = jsonl("rounds.jsonl")
    candidates = jsonl("candidates.jsonl")
    attempts = jsonl("access-attempts.jsonl")
    summary = json.loads((BASE / "summary.json").read_text())
    errors: list[str] = []

    if [row.get("round") for row in rounds] != [1, 2, 3]:
        errors.append("rounds must be exactly 1, 2, 3 in order")
    if len({row.get("backend") for row in rounds}) != 3:
        errors.append("rounds must use three materially different live backends")
    if len({row.get("query_family") for row in rounds}) != 3:
        errors.append("round query families must be materially distinct")

    grouped: dict[int, list[dict]] = defaultdict(list)
    seen_urls: set[str] = set()
    required = {"round", "rank", "source_id", "title", "canonical_url", "disposition", "reason"}
    for row in candidates:
        missing = required - row.keys()
        if missing or any(row.get(key) in (None, "") for key in required):
            errors.append(f"candidate missing audit fields: {row.get('source_id')}: {sorted(missing)}")
        if row.get("disposition") not in DISPOSITIONS:
            errors.append(f"invalid disposition: {row.get('source_id')}")
        parsed = urlparse(row.get("canonical_url", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"invalid canonical URL: {row.get('canonical_url')}")
        if row.get("canonical_url") in seen_urls:
            errors.append(f"candidate URL repeated within wave: {row.get('canonical_url')}")
        seen_urls.add(row.get("canonical_url"))
        grouped[row.get("round")].append(row)

    eligible: list[int] = []
    for round_row in rounds:
        number = round_row["round"]
        items = grouped[number]
        if sorted(row["rank"] for row in items) != list(range(1, len(items) + 1)):
            errors.append(f"round {number}: incomplete/non-contiguous candidate ranks")
        counts = Counter(row["disposition"] for row in items)
        expected = {"retrieved_candidates": len(items), "accepted": counts["accepted"],
                    "rejected": counts["rejected"], "duplicate": counts["duplicate"],
                    "blocked": counts["blocked"], "unresolved_blockers": counts["blocked"]}
        for field, value in expected.items():
            if round_row.get(field) != value:
                errors.append(f"round {number} {field}: expected {value}, got {round_row.get(field)}")
        rate = counts["accepted"] / len(items) if items else 0.0
        computed = round_row.get("retrieval_status") == "complete" and bool(items) and not counts["blocked"] and rate < 0.05
        if round_row.get("net_new_accepted_rate") != rate:
            errors.append(f"round {number}: incorrect accepted rate")
        if round_row.get("saturation_eligible") is not computed:
            errors.append(f"round {number}: incorrect eligibility")
        if computed:
            eligible.append(number)
        if not round_row.get("request_urls") or not round_row.get("material_difference"):
            errors.append(f"round {number}: missing exact request/material-difference evidence")
        for field in ("searched_at", "completed_at"):
            try:
                datetime.fromisoformat(round_row[field].replace("Z", "+00:00"))
            except (KeyError, ValueError):
                errors.append(f"round {number}: invalid {field}")

    canonical = "\n".join(" ".join(row.values()).lower() for row in csv.DictReader((ROOT / "metadata" / "sources.csv").open()))
    wave5 = (ROOT / "research" / "academic-saturation-5" / "candidates.jsonl").read_text().lower()
    for row in candidates:
        match = row["canonical_url"].lower() in canonical or (row.get("doi") or "").lower() in canonical
        if row["disposition"] == "accepted" and not match:
            errors.append(f"accepted source lacks canonical ingestion: {row['source_id']}")
        if row["disposition"] == "duplicate" and row["canonical_url"].lower() not in canonical and row["canonical_url"].lower() not in wave5:
            errors.append(f"duplicate lacks prior evidence: {row['source_id']}")

    counts = Counter(row["disposition"] for row in candidates)
    expected_summary = {"round_count": 3, "candidate_count": len(candidates), "accepted": counts["accepted"],
                        "rejected": counts["rejected"], "duplicate": counts["duplicate"], "blocked": counts["blocked"],
                        "net_new_sources_ingested": counts["accepted"], "saturation_eligible_rounds": eligible,
                        "ineligible_rounds": [row["round"] for row in rounds if not row["saturation_eligible"]],
                        "saturated": eligible == [1, 2, 3]}
    for field, value in expected_summary.items():
        if summary.get(field) != value:
            errors.append(f"summary {field}: expected {value}, got {summary.get(field)}")
    if "10.47176/smok.2025.1821" not in summary.get("precondition", ""):
        errors.append("summary lacks explicit pre-round acceptance precondition")
    if not any(row.get("status") == "retrieved_complete" for row in attempts):
        errors.append("DOI investigation lacks complete primary/metadata access evidence")

    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({**expected_summary, "backends": [row["backend"] for row in rounds], "errors": []}))


if __name__ == "__main__":
    main()
