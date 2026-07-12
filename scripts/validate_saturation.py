#!/usr/bin/env python3
"""Validate saturation ledgers without asserting that incomplete rounds pass."""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "research" / "saturation"
rounds = [json.loads(line) for line in (base / "rounds.jsonl").read_text().splitlines() if line]
candidates = [json.loads(line) for line in (base / "candidates.jsonl").read_text().splitlines() if line]
errors = []
by_channel = defaultdict(list)
for row in rounds:
    by_channel[row["channel"]].append(row)
    if row["accepted"] + row["rejected"] + row["blocked"] != row["result_count"]:
        errors.append(f"count mismatch: {row['channel']} round {row['round']}")
    if row["saturation_eligible"] and row["blocked"]:
        errors.append(f"blocked round incorrectly eligible: {row['channel']} round {row['round']}")
for channel, rows in by_channel.items():
    if sorted(x["round"] for x in rows) != [1, 2, 3]:
        errors.append(f"expected rounds 1..3 for {channel}")
    if len({x["query_family"] for x in rows}) != 3:
        errors.append(f"query families not materially distinct for {channel}")
round_keys = Counter((x["channel"], x["round"]) for x in candidates)
for row in rounds:
    if round_keys[(row["channel"], row["round"])] != row["result_count"]:
        errors.append(f"candidate ledger mismatch: {row['channel']} round {row['round']}")
summary = json.loads((base / "summary.json").read_text())
if summary["rounds"] != len(rounds) or summary["results"] != len(candidates):
    errors.append("summary totals do not match ledgers")
if errors:
    raise SystemExit("\n".join(errors))
print(json.dumps({"channels": len(by_channel), "rounds": len(rounds),
                  "candidates": len(candidates), "errors": []}))
