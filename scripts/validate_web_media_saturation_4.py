#!/usr/bin/env python3
"""Validate the isolated fourth web/media saturation checkpoint."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "web-media-saturation-4"
CHANNELS = {"blogs", "podcasts", "books", "conferences", "case-studies", "github"}


def rows(name: str) -> list[dict]:
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line.strip()]


def main() -> None:
    rounds, candidates, access = rows("rounds.jsonl"), rows("candidates.jsonl"), rows("access.jsonl")
    summary = json.loads((BASE / "summary.json").read_text())
    errors: list[str] = []
    by_channel: dict[str, list[dict]] = defaultdict(list)
    accepted_records: dict[str, dict] = {}
    for lane in CHANNELS:
        for path in (ROOT / "sources" / lane / "accepted").glob("*.json"):
            record = json.loads(path.read_text())
            accepted_records[record["stable_id"]] = record

    candidate_keys = Counter((row["channel"], row["round"]) for row in candidates)
    disposition_keys = Counter((row["channel"], row["round"], row["disposition"]) for row in candidates)
    candidate_urls = [row["canonical_url"].rstrip("/") for row in candidates]
    if len(candidate_urls) != len(set(candidate_urls)):
        errors.append("candidate ledger contains repeated canonical URLs")

    for row in candidates:
        if row["channel"] not in CHANNELS or row["disposition"] not in {"accepted", "rejected", "duplicate", "blocked"}:
            errors.append(f"invalid candidate disposition: {row.get('canonical_url')}")
        if not row.get("canonical_url") or not row.get("stable_id") or not row.get("reason"):
            errors.append(f"candidate lacks identity or reason: {row.get('canonical_url')}")
        if row["disposition"] == "duplicate":
            record = accepted_records.get(row["stable_id"])
            if not record or record["canonical_url"].rstrip("/") != row["canonical_url"].rstrip("/"):
                errors.append(f"unproved canonical duplicate: {row['canonical_url']}")
        if row["channel"] == "github" and row["disposition"] == "rejected":
            reason = row["reason"].lower()
            if "generic" not in reason or "organization-level learning mechanism" not in reason:
                errors.append(f"GitHub rejection lacks organization-evidence rationale: {row['canonical_url']}")

    for row in rounds:
        by_channel[row["channel"]].append(row)
        key = (row["channel"], row["round"])
        disposed = row["accepted"] + row["rejected"] + row["duplicates"] + row["blocked"]
        if disposed != row["retrieved_candidates"] or candidate_keys[key] != row["retrieved_candidates"]:
            errors.append(f"incomplete round: {row['channel']} {row['round']}")
        for field, disposition in (("accepted", "accepted"), ("rejected", "rejected"),
                                   ("duplicates", "duplicate"), ("blocked", "blocked")):
            if row[field] != disposition_keys[(*key, disposition)]:
                errors.append(f"{field} mismatch: {row['channel']} {row['round']}")
        rate = row.get("net_new_accepted_unique_rate", {})
        numerator, denominator = row["accepted"], row["retrieved_candidates"]
        exact_value = numerator / denominator if denominator else 0.0
        if rate != {"numerator": numerator, "denominator": denominator, "value": exact_value}:
            errors.append(f"exact novelty math mismatch: {row['channel']} {row['round']}")
        if row["saturation_eligible"] and (
            row.get("access_status") != "retrieved" or not row["fully_reviewed"]
            or denominator == 0 or row["blocked"] or exact_value >= 0.05
        ):
            errors.append(f"blocked/shallow/high-yield round counted: {row['channel']} {row['round']}")
        if not row.get("query_family") or not row.get("backend") or not row.get("material_difference") or not row.get("eligibility_note"):
            errors.append(f"round lacks audit rationale: {row['channel']} {row['round']}")

    if set(by_channel) != CHANNELS:
        errors.append(f"owned channel set mismatch: {sorted(by_channel)}")
    for channel, items in by_channel.items():
        ordered = sorted(items, key=lambda item: item["round"])
        if [item["round"] for item in ordered] != [1, 2, 3]:
            errors.append(f"{channel}: expected three consecutive rounds")
        if len({item["query_family"] for item in items}) != 3:
            errors.append(f"{channel}: query families are not materially distinct")
        if not all(item["saturation_eligible"] for item in ordered):
            errors.append(f"{channel}: saturation claim includes an ineligible round")

    if any(row.get("counts_toward_saturation") for row in access):
        errors.append("blocked or shallow access attempt counted toward saturation")
    if not all(row.get("evidence") and row.get("status") for row in access):
        errors.append("access attempt lacks status/evidence")

    expected = {
        "round_count": len(rounds),
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
    eligible_by_channel = {channel: sum(bool(row["saturation_eligible"]) for row in items)
                           for channel, items in sorted(by_channel.items())}
    if summary.get("eligible_rounds_by_channel") != eligible_by_channel:
        errors.append("summary eligible-round counts mismatch")
    if set(summary.get("saturated_channels", [])) != CHANNELS:
        errors.append("summary saturation set does not match three-round proof")
    if set(summary.get("scope", [])) != CHANNELS or "academic" not in summary.get("excluded_scope", {}):
        errors.append("summary must preserve the web/media ownership boundary")

    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"channels": sorted(CHANNELS), **expected,
                      "saturated_channels": sorted(CHANNELS), "errors": []}))


if __name__ == "__main__":
    main()
