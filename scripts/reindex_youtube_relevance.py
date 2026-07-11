#!/usr/bin/env python3
"""Recompute transcript-grounded relevance spans for all metadata records."""

import json, re
from pathlib import Path
from youtube_pipeline import META, ROOT, relevance, rebuild_csv

for path in sorted(META.glob("*.json")):
    data = json.loads(path.read_text())
    transcript = (ROOT / data["transcript_path"]).read_text(errors="replace")
    segments = []
    for line in transcript.splitlines():
        match = re.match(r"(?:(\d+):)?(\d{1,2}):(\d{2})\s+(.+)", line)
        if match:
            segments.append({"start": int(match[1] or 0) * 3600 + int(match[2]) * 60 + int(match[3]), "text": match[4]})
    categories, evidence, spans = relevance(data, segments)
    data["relevance_categories"] = categories
    data["relevance_evidence"] = evidence
    data["relevance_spans"] = spans
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
rebuild_csv()
print(f"reindexed={len(list(META.glob('*.json')))}")
