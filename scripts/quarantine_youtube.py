#!/usr/bin/env python3
"""Remove a source from counted metadata while preserving all evidence."""

import argparse, json, shutil
from pathlib import Path
from youtube_pipeline import META, RAW, ROOT, rebuild_csv

parser = argparse.ArgumentParser()
parser.add_argument("video_id")
parser.add_argument("reason")
args = parser.parse_args()
matches = list(META.glob(f"*--{args.video_id}.json"))
if not matches: raise SystemExit(f"metadata not found: {args.video_id}")
mp = matches[0]; data = json.loads(mp.read_text())
qroot = ROOT / "quarantine" / "youtube" / mp.stem
qroot.mkdir(parents=True, exist_ok=True)
for source in [ROOT / data["transcript_path"], ROOT / data["raw_path"], mp]:
    if source.exists(): shutil.move(source, qroot / source.name)
ledger = ROOT / "quarantine" / "youtube" / "ledger.jsonl"
with ledger.open("a") as f: f.write(json.dumps({"video_id": args.video_id, "title": data["title"], "reason": args.reason, "former_transcript_path": data["transcript_path"]}, ensure_ascii=False) + "\n")
rebuild_csv()
print(f"quarantined={args.video_id}")
