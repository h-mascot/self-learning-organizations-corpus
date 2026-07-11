#!/usr/bin/env python3
"""One-time migration of seed ID-only Markdown files into the pipeline layout."""

import json, re, shutil
from pathlib import Path

from youtube_pipeline import RAW, ROOT, TRANSCRIPTS, base_name, write_source

QUARANTINE = ROOT / "quarantine" / "youtube"
MANIFEST = ROOT / "metadata" / "youtube-filename-migration.json"


def scalar(text: str, key: str):
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", text)
    if not match: return None
    value = match.group(1).strip().strip("'\"")
    return int(value) if value.isdigit() and key == "duration_seconds" else value


def segments(text: str):
    output = []
    for line in text.splitlines():
        match = re.match(r"(?:(\d+):)?(\d{1,2}):(\d{2})\s+(.+)", line)
        if match:
            h, m, s = int(match[1] or 0), int(match[2]), int(match[3])
            output.append({"start": h * 3600 + m * 60 + s, "text": match[4].strip()})
    return output


def main():
    records = []
    for old in sorted(TRANSCRIPTS.glob("???????????.md")):
        text = old.read_text()
        info = {
            "id": scalar(text, "video_id"), "title": scalar(text, "title"),
            "channel": scalar(text, "channel"), "webpage_url": scalar(text, "source_url"),
            "duration": scalar(text, "duration_seconds"), "upload_date": scalar(text, "upload_date"),
            "availability": "public-at-ingestion", "license": None,
        }
        name = base_name(info)
        if info["id"] == "fVut0ceg2IY":
            QUARANTINE.mkdir(parents=True, exist_ok=True)
            target = QUARANTINE / f"{name}.md"
            shutil.move(old, target)
            records.append({"video_id": info["id"], "old": str(old.relative_to(ROOT)), "new": str(target.relative_to(ROOT)), "status": "quarantined-unrelated", "reason": "Restaurant advertisement; no organizational learning or adaptive-organization content."})
            continue
        raw_dir = RAW / name
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_copy = raw_dir / "legacy-transcript.md"
        shutil.copy2(old, raw_copy)
        (raw_dir / "source-info.json").write_text(json.dumps(info, indent=2) + "\n")
        target = write_source(info, segments(text), "legacy-youtube-captions", raw_dir)
        old.unlink()
        records.append({"video_id": info["id"], "old": str(old.relative_to(ROOT)), "new": str(target.relative_to(ROOT)), "status": "migrated"})
    MANIFEST.write_text(json.dumps({"schema_version": 1, "records": records}, indent=2) + "\n")
    print(json.dumps({"migrated": sum(r["status"] == "migrated" for r in records), "quarantined": sum(r["status"].startswith("quarantined") for r in records)}, sort_keys=True))


if __name__ == "__main__": main()
