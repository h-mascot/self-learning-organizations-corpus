#!/usr/bin/env python3
"""Validate every counted YouTube source and print exact proof."""

import csv, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
meta_files = sorted((ROOT / "metadata" / "youtube").glob("*.json"))
ids = set()
name_re = re.compile(r"^(?:\d{4}-\d{2}-\d{2}|unknown-date)--[a-z0-9-]+--[a-z0-9-]+--[A-Za-z0-9_-]{11}$")
for mp in meta_files:
    data = json.loads(mp.read_text())
    vid = data.get("video_id")
    if vid in ids: errors.append(f"duplicate video_id: {vid}")
    ids.add(vid)
    if not name_re.match(mp.stem): errors.append(f"bad filename: {mp.name}")
    tp = ROOT / data.get("transcript_path", "")
    if not tp.exists(): errors.append(f"missing transcript: {vid}"); continue
    if tp.stem != mp.stem: errors.append(f"metadata/transcript basename mismatch: {vid}")
    digest = hashlib.sha256(tp.read_bytes()).hexdigest()
    if digest != data.get("transcript_sha256"): errors.append(f"transcript hash mismatch: {vid}")
    text = tp.read_text(errors="replace")
    stamps = re.findall(r"(?m)^(?:\d+:)?\d{1,2}:\d{2} ", text)
    if len(stamps) < 5: errors.append(f"insufficient timestamps: {vid} ({len(stamps)})")
    if len(stamps) != data.get("segment_count"): errors.append(f"segment mismatch: {vid}")
    if not data.get("relevance_categories"): errors.append(f"missing relevance evidence: {vid}")
    if not data.get("relevance_spans"): errors.append(f"missing timestamped relevance span: {vid}")
    if not data.get("rights_note"): errors.append(f"missing rights note: {vid}")
    raw = ROOT / data.get("raw_path", "")
    for name, expected in data.get("raw_files", {}).items():
        rp = raw / name
        if not rp.exists(): errors.append(f"missing raw file: {vid}/{name}"); continue
        actual = hashlib.sha256(rp.read_bytes()).hexdigest()
        if actual != expected: errors.append(f"raw hash mismatch: {vid}/{name}")
if "fVut0ceg2IY" in ids: errors.append("quarantined source counted: fVut0ceg2IY")
print(f"validated_relevant_transcripts={len(meta_files) - len({e.split(': ')[-1].split('/')[0].split(' ')[0] for e in errors if ': ' in e})}")
print(f"metadata_files={len(meta_files)}")
print(f"unique_video_ids={len(ids)}")
print(f"errors={len(errors)}")
for error in errors: print(f"ERROR {error}")
sys.exit(bool(errors))
