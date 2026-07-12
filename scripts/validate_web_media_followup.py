#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

root = Path("research/web-media-followup")
rounds = [json.loads(x) for x in (root / "rounds.jsonl").read_text().splitlines() if x]
candidates = [json.loads(x) for x in (root / "candidates.jsonl").read_text().splitlines() if x]
summary = json.loads((root / "summary.json").read_text())
errors = []
expected = {"blogs", "podcasts", "books", "conferences", "case-studies", "github", "academic"}
by_channel = Counter(x["channel"] for x in rounds)
if set(by_channel) != expected or any(by_channel[x] != 3 for x in expected):
    errors.append(f"expected three rounds for seven channels: {dict(by_channel)}")
keys = Counter((x["channel"], x["round"]) for x in candidates)
for row in rounds:
    if row["accepted"] + row["rejected"] + row["blocked"] != row["result_count"]:
        errors.append(f"count mismatch: {row['channel']} round {row['round']}")
    if keys[(row["channel"], row["round"])] != row["result_count"]:
        errors.append(f"candidate mismatch: {row['channel']} round {row['round']}")
    if row["saturation_eligible"]:
        errors.append(f"unsupported saturation claim: {row['channel']} round {row['round']}")
accepted = [x for x in candidates if x["disposition"] == "accepted"]
if len(accepted) != 1 or "google/building-secure-and-reliable-systems" not in accepted[0]["url"]:
    errors.append("expected exactly the manually verified Google implementation artifact")
if summary["accepted"] != len(accepted) or summary["channels_saturated"]:
    errors.append("summary acceptance mismatch or unsupported saturation")
print(json.dumps({"rounds": len(rounds), "candidates": len(candidates), "errors": errors}, indent=2))
sys.exit(bool(errors))
