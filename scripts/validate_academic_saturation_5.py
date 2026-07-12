#!/usr/bin/env python3
"""Validate academic saturation wave 5 retrieval and disposition evidence."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "academic-saturation-5"
DISPOSITIONS = {"accepted", "rejected", "duplicate", "blocked"}


def jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line.strip()]


def normalized_doi(value: str | None) -> str:
    return (value or "").lower().removeprefix("https://doi.org/").rstrip("/")


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
    required_candidate = {"round", "rank", "source_id", "title", "canonical_url", "disposition", "reason"}
    for row in candidates:
        missing = required_candidate - row.keys()
        if missing or any(row.get(key) in (None, "") for key in required_candidate - {"doi"}):
            errors.append(f"candidate missing audit fields: {row.get('source_id')}: {sorted(missing)}")
        if row.get("disposition") not in DISPOSITIONS:
            errors.append(f"invalid disposition: {row.get('source_id')}")
        parsed = urlparse(row.get("canonical_url", ""))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"invalid canonical URL: {row.get('canonical_url')}")
        if row.get("canonical_url") in seen_urls:
            errors.append(f"candidate URL repeated across bounded results: {row.get('canonical_url')}")
        seen_urls.add(row.get("canonical_url"))
        grouped[row.get("round")].append(row)

    eligible: list[int] = []
    for round_row in rounds:
        number = round_row["round"]
        items = grouped[number]
        if sorted(row["rank"] for row in items) != list(range(1, len(items) + 1)):
            errors.append(f"round {number}: incomplete/non-contiguous candidate ranks")
        counts = Counter(row["disposition"] for row in items)
        expected = {
            "retrieved_candidates": len(items),
            "accepted": counts["accepted"],
            "rejected": counts["rejected"],
            "duplicate": counts["duplicate"],
            "blocked": counts["blocked"],
            "unresolved_blockers": counts["blocked"],
        }
        for field, value in expected.items():
            if round_row.get(field) != value:
                errors.append(f"round {number} {field}: expected {value}, got {round_row.get(field)}")
        denominator = len(items)
        rate = counts["accepted"] / denominator if denominator else 0.0
        if round_row.get("net_new_accepted_rate") != rate:
            errors.append(f"round {number}: incorrect accepted rate")
        computed_eligible = (
            round_row.get("retrieval_status") == "complete"
            and counts["blocked"] == 0
            and rate < 0.05
            and denominator > 0
        )
        if round_row.get("saturation_eligible") is not computed_eligible:
            errors.append(f"round {number}: incorrect eligibility")
        if computed_eligible:
            eligible.append(number)
        for field in ("searched_at", "completed_at"):
            try:
                datetime.fromisoformat(round_row[field].replace("Z", "+00:00"))
            except (KeyError, ValueError):
                errors.append(f"round {number}: invalid {field}")
        if not round_row.get("request_urls") or not round_row.get("material_difference"):
            errors.append(f"round {number}: missing exact request or material-difference evidence")

    canonical_rows = list(csv.DictReader((ROOT / "metadata" / "sources.csv").open()))
    canonical_blob = "\n".join(" ".join(str(value) for value in row.values()).lower() for row in canonical_rows)
    for row in candidates:
        disposition = row["disposition"]
        doi = normalized_doi(row.get("doi"))
        canonical_match = row["canonical_url"].lower() in canonical_blob or (doi and doi in canonical_blob)
        if disposition == "duplicate" and not canonical_match:
            errors.append(f"duplicate lacks canonical match: {row['source_id']}")
        if disposition in {"accepted", "blocked"} and canonical_match:
            errors.append(f"net-new disposition already occurs canonically: {row['source_id']}")
        if disposition == "blocked" and "manager review" not in row["reason"].lower():
            errors.append(f"blocked source lacks manager-review handoff: {row['source_id']}")

    counts = Counter(row["disposition"] for row in candidates)
    expected_summary = {
        "round_count": len(rounds),
        "candidate_count": len(candidates),
        "accepted": counts["accepted"],
        "rejected": counts["rejected"],
        "duplicate": counts["duplicate"],
        "blocked": counts["blocked"],
        "net_new_sources_ingested": 0,
        "saturation_eligible_rounds": eligible,
        "ineligible_rounds": [row["round"] for row in rounds if not row["saturation_eligible"]],
        "saturated": eligible == [1, 2, 3],
    }
    for field, value in expected_summary.items():
        if summary.get(field) != value:
            errors.append(f"summary {field}: expected {value}, got {summary.get(field)}")

    if not any(row.get("status") == "retrieved_complete" for row in attempts):
        errors.append("citation/entity chase lacks complete access evidence")
    if any(not row.get("attempted_at") or not row.get("backend") or not row.get("evidence") for row in attempts):
        errors.append("access attempt lacks exact provenance/evidence")

    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({**expected_summary, "backends": [row["backend"] for row in rounds], "errors": []}))


if __name__ == "__main__":
    main()
