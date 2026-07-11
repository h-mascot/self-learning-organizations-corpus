#!/usr/bin/env python3
"""Run the versioned query set and emit a deduplicated discovery manifest."""

import argparse, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--results-per-query", type=int, default=20)
parser.add_argument("--output", type=Path, default=ROOT / "research" / "youtube-discovery.jsonl")
args = parser.parse_args()
queries = [q.strip() for q in (ROOT / "config" / "youtube_queries.txt").read_text().splitlines() if q.strip()]
seen, records = set(), []
for query in queries:
    result = subprocess.run(["yt-dlp", "--flat-playlist", "--dump-json", f"ytsearch{args.results_per_query}:{query}"], capture_output=True, text=True, check=True)
    for rank, line in enumerate(result.stdout.splitlines(), 1):
        item = json.loads(line)
        if item["id"] in seen: continue
        seen.add(item["id"])
        records.append({"video_id": item["id"], "title": item.get("title"), "channel": item.get("channel") or item.get("uploader"), "duration_seconds": item.get("duration"), "discovery_query": query, "query_rank": rank, "url": item.get("url")})
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records))
print(f"queries={len(queries)}")
print(f"unique_candidates={len(records)}")
print(f"output={args.output}")
