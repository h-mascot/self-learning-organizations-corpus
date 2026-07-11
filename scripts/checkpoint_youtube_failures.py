#!/usr/bin/env python3
"""Materialize attempted-but-uningested sources and their last observed failures."""

import json, re
from pathlib import Path
from youtube_pipeline import META, ROOT

existing = {json.loads(p.read_text())["video_id"] for p in META.glob("*.json")}
logs = list(Path("/tmp/youtube-discovery").glob("**/*.log"))
failures = {}
for log in logs:
    for line in log.read_text(errors="replace").splitlines():
        match = re.match(r"FAILED(?:-CACHED)? (?:https://www\.youtube\.com/watch\?v=)?([A-Za-z0-9_-]{11}): (.+)", line)
        if match and match[1] not in existing:
            reason = match[2]
            if "Rate limit reached" in reason: kind = "asr-hourly-quota"
            elif "not available" in reason or "non-zero exit" in reason: kind = "youtube-extraction-blocked"
            else: kind = "ingestion-failed"
            failures[match[1]] = {"video_id": match[1], "url": f"https://www.youtube.com/watch?v={match[1]}", "failure_kind": kind, "last_error": reason[-1000:]}
output = ROOT / "research" / "progress" / "youtube-failures.jsonl"
output.write_text("".join(json.dumps(v, ensure_ascii=False, sort_keys=True) + "\n" for v in sorted(failures.values(), key=lambda x: x["video_id"])))
print(f"failed_sources={len(failures)}")
print(f"output={output}")
