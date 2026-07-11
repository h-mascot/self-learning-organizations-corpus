#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

errors = []
ledger = Path("research/loops/ledger.csv")
rows = list(csv.DictReader(ledger.open())) if ledger.exists() else []
productive = [r for r in rows if r["outcome"] == "productive"]
for row in productive:
    artifact = ledger.parent / row["artifact"]
    if not artifact.exists(): errors.append(f"missing loop artifact: {artifact}")
    else:
        data = json.loads(artifact.read_text())
        if not data.get("works"): errors.append(f"productive loop lacks evidence: {artifact}")
for required in ["research/company-index.md", "research/competitive-github-benchmark.md", "research/sources/index.md", "research/deep-research/manifest.json", "research/progress/research.md"]:
    if not Path(required).exists(): errors.append(f"missing required artifact: {required}")
print(json.dumps({"ledger_rows": len(rows), "productive_loops": len(productive), "errors": errors}, indent=2))
sys.exit(bool(errors))
