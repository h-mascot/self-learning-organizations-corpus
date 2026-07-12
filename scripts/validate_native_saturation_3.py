#!/usr/bin/env python3
"""Validate the isolated native/high-precision saturation-3 ledgers."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "native-saturation-3"
CHANNELS = {"x", "reddit", "substack", "youtube"}


def jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line.strip()]


def main() -> None:
    rounds = jsonl("rounds.jsonl")
    attempts = jsonl("path-attempts.jsonl")
    candidates = jsonl("candidates.jsonl")
    summary = json.loads((BASE / "summary.json").read_text())
    errors: list[str] = []
    by_channel: dict[str, list[dict]] = defaultdict(list)

    for row in rounds:
        by_channel[row["channel"]].append(row)
        disposed = row["accepted"] + row["rejected"] + row["duplicates"] + row["blocked"]
        if disposed != row["retrieved_candidates"]:
            errors.append(f"round disposition mismatch: {row['channel']} {row['round']}")
        if row["access_status"] != "retrieved" and row["saturation_eligible"]:
            errors.append(f"blocked/shallow round marked eligible: {row['channel']} {row['round']}")
        if row["retrieved_candidates"] == 0 and row["saturation_eligible"]:
            errors.append(f"zero-yield round marked eligible: {row['channel']} {row['round']}")
        if not row.get("material_difference") or not row.get("eligibility_note"):
            errors.append(f"round lacks audit rationale: {row['channel']} {row['round']}")
        expected_rate = row["accepted"] / row["retrieved_candidates"] if row["retrieved_candidates"] else 0.0
        if row.get("net_new_accepted_rate") != expected_rate:
            errors.append(f"round acceptance-rate mismatch: {row['channel']} {row['round']}")
        if row["saturation_eligible"] and expected_rate >= 0.05:
            errors.append(f"eligible round is not low yield: {row['channel']} {row['round']}")

    if set(by_channel) != CHANNELS:
        errors.append(f"channel set mismatch: {sorted(by_channel)}")
    for channel, rows in by_channel.items():
        if sorted(row["round"] for row in rows) != [1, 2, 3]:
            errors.append(f"{channel}: expected rounds 1..3")
        if len({row["query_family"] for row in rows}) != 3:
            errors.append(f"{channel}: query families are not distinct")

    attempt_counts = Counter(row["channel"] for row in attempts)
    if any(attempt_counts[channel] < 3 for channel in CHANNELS):
        errors.append(f"expected at least three path attempts per channel: {dict(attempt_counts)}")
    if any(row["yielded_candidates"] < 0 or not row.get("evidence") for row in attempts):
        errors.append("path attempt lacks evidence or has a negative yield")

    candidate_keys = Counter((row["channel"], row["round"]) for row in candidates)
    for row in rounds:
        if candidate_keys[(row["channel"], row["round"])] != row["retrieved_candidates"]:
            errors.append(f"candidate ledger mismatch: {row['channel']} {row['round']}")
    for row in candidates:
        if row.get("disposition") not in {"accepted", "rejected", "duplicate", "blocked"}:
            errors.append("candidate has invalid disposition")
        if not row.get("canonical_url") or not row.get("reason"):
            errors.append("candidate lacks canonical URL or reason")
        if not row.get("title") or not isinstance(row.get("rank"), int):
            errors.append("candidate lacks title or integer rank")

    candidate_urls = [row["canonical_url"] for row in candidates]
    if len(candidate_urls) != len(set(candidate_urls)):
        errors.append("candidate ledger contains duplicate canonical URLs")

    expected = {
        "round_count": len(rounds),
        "path_attempt_count": len(attempts),
        "candidate_count": len(candidates),
        "accepted": sum(row["accepted"] for row in rounds),
        "rejected": sum(row["rejected"] for row in rounds),
        "duplicates": sum(row["duplicates"] for row in rounds),
        "blocked": sum(row["blocked"] for row in rounds),
        "saturation_eligible_rounds": sum(bool(row["saturation_eligible"]) for row in rounds),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"summary {key}: expected {value}, got {summary.get(key)}")
    if summary.get("saturated_channels"):
        errors.append("blocked-only evidence cannot declare a saturated channel")
    eligible_by_channel = {
        channel: sum(bool(row["saturation_eligible"]) for row in rows)
        for channel, rows in sorted(by_channel.items())
    }
    if summary.get("eligible_rounds_by_channel") != eligible_by_channel:
        errors.append("summary eligible-round channel counts mismatch")

    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"channels": sorted(CHANNELS), **expected, "errors": []}))


if __name__ == "__main__":
    main()
