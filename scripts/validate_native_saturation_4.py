#!/usr/bin/env python3
"""Validate high-integrity native/public saturation wave 4 evidence."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "native-saturation-4"
LANES = ("x", "reddit", "substack", "youtube")
DISPOSITIONS = {"accepted", "rejected", "duplicate", "blocked"}
MIN_CANDIDATES = 3


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> None:
    summary = json.loads((BASE / "summary.json").read_text())
    rows = {lane: load_jsonl(BASE / f"{lane}.jsonl") for lane in LANES}
    attempts = load_jsonl(BASE / "path-attempts.jsonl")
    errors: list[str] = []
    all_rows = [row | {"channel": lane} for lane, lane_rows in rows.items() for row in lane_rows]
    eligible_by_lane: dict[str, int] = {}

    required = (
        "searched_at", "round", "query_family", "query", "backend", "access_path",
        "access_evidence", "rank", "title", "canonical_url", "disposition", "reason",
    )
    for lane, lane_rows in rows.items():
        rounds: dict[int, list[dict]] = defaultdict(list)
        for row in lane_rows:
            rounds[row.get("round")].append(row)
            if any(row.get(field) in (None, "") for field in required):
                errors.append(f"{lane}: candidate lacks required audit field")
            if row.get("disposition") not in DISPOSITIONS:
                errors.append(f"{lane}: invalid disposition")
            parsed = urlparse(row.get("canonical_url", ""))
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{lane}: non-canonical candidate URL")
        if sorted(rounds) != [1, 2, 3]:
            errors.append(f"{lane}: expected exactly rounds 1..3")
        if len({items[0]["query_family"] for items in rounds.values()}) != 3:
            errors.append(f"{lane}: query families are not materially distinct")
        eligible = 0
        for number, items in sorted(rounds.items()):
            if len(items) < MIN_CANDIDATES:
                errors.append(f"{lane} round {number}: shallow candidate set")
            if sorted(row["rank"] for row in items) != list(range(1, len(items) + 1)):
                errors.append(f"{lane} round {number}: ranks are not complete")
            stable_fields = ("searched_at", "query_family", "query", "backend", "access_path")
            if any(len({row[field] for row in items}) != 1 for field in stable_fields):
                errors.append(f"{lane} round {number}: inconsistent round provenance")
            accepted_rate = sum(row["disposition"] == "accepted" for row in items) / len(items)
            blocked = any(row["disposition"] == "blocked" for row in items)
            complete = all("complete" in row["access_evidence"].lower() or
                           "full" in row["access_evidence"].lower() or
                           "reviewed" in row["access_evidence"].lower() for row in items)
            if not blocked and complete and accepted_rate < 0.05:
                eligible += 1
            elif summary.get("saturated_lanes") and lane in summary["saturated_lanes"]:
                errors.append(f"{lane} round {number}: saturated lane has an ineligible round")
        eligible_by_lane[lane] = eligible

    # Repeated results across different rounds are legitimate only when marked duplicate.
    occurrences: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in all_rows:
        occurrences[(row["channel"], row["canonical_url"])].append(row)
    for (lane, url), repeated in occurrences.items():
        if len(repeated) > 1 and any(row["disposition"] != "duplicate" for row in repeated[1:]):
            errors.append(f"{lane}: repeated URL is not honestly dispositioned duplicate: {url}")

    attempt_lanes = {row.get("channel") for row in attempts}
    if attempt_lanes != set(LANES):
        errors.append("access-path attempts do not cover all lanes")
    if any(not row.get("evidence") or not row.get("status") or not row.get("path") for row in attempts):
        errors.append("access-path attempt lacks path/status/evidence")
    complete_attempts = Counter(
        row["channel"] for row in attempts if row.get("status") == "retrieved_complete"
    )
    if any(complete_attempts[lane] < 1 for lane in LANES):
        errors.append("every saturated lane needs a complete native/public access path")

    counts = Counter(row["disposition"] for row in all_rows)
    expected = {
        "candidate_count": len(all_rows),
        **{key: counts[key] for key in DISPOSITIONS},
        "rounds_per_lane": {lane: len({row["round"] for row in lane_rows}) for lane, lane_rows in rows.items()},
        "saturation_eligible_rounds": sum(eligible_by_lane.values()),
        "eligible_rounds_by_lane": eligible_by_lane,
        "low_yield_rounds": sum(eligible_by_lane.values()),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"summary {key}: expected {value}, got {summary.get(key)}")
    expected_saturated = sorted(lane for lane, count in eligible_by_lane.items() if count == 3)
    if sorted(summary.get("saturated_lanes", [])) != expected_saturated:
        errors.append(f"summary saturated_lanes: expected {expected_saturated}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"lanes": list(LANES), **expected, "saturated_lanes": expected_saturated, "errors": []}))


if __name__ == "__main__":
    main()
