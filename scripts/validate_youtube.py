#!/usr/bin/env python3
"""Validate every counted YouTube source and print exact proof."""

import csv, hashlib, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
meta_files = sorted((ROOT / "metadata" / "youtube").glob("*.json"))
ids = set()
name_re = re.compile(r"^(?:\d{4}-\d{2}-\d{2}|unknown-date)--[a-z0-9-]+--[a-z0-9-]+--[A-Za-z0-9_-]{11}$")

def slug(value):
    value = html.unescape(value or "").lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:100].rstrip("-") or "untitled"

def canonical_stem(data):
    date = data.get("upload_date") or "unknown-date"
    if len(date) == 8 and date.isdigit(): date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    return f"{date}--{slug(data.get('title'))}--{slug(data.get('channel') or 'unknown-publisher')}--{data.get('video_id')}"

for mp in meta_files:
    data = json.loads(mp.read_text())
    vid = data.get("video_id")
    if vid in ids: errors.append(f"duplicate video_id: {vid}")
    ids.add(vid)
    if not name_re.match(mp.stem): errors.append(f"bad filename: {mp.name}")
    source_url = data.get("source_url") or ""
    if not re.fullmatch(rf"https://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/){re.escape(vid)}", source_url): errors.append(f"invalid source URL: {vid}")
    tp = ROOT / data.get("transcript_path", "")
    if not tp.exists(): errors.append(f"missing transcript: {vid}"); continue
    if tp.stem != mp.stem: errors.append(f"metadata/transcript basename mismatch: {vid}")
    digest = hashlib.sha256(tp.read_bytes()).hexdigest()
    if digest != data.get("transcript_sha256"): errors.append(f"transcript hash mismatch: {vid}")
    text = tp.read_text(errors="replace")
    stamp_values = re.findall(r"(?m)^((?:(\d+):)?(\d{1,2}):(\d{2})) ", text)
    stamps = [int(h or 0) * 3600 + int(m) * 60 + int(s) for _, h, m, s in stamp_values]
    if len(stamps) < 5: errors.append(f"insufficient timestamps: {vid} ({len(stamps)})")
    if len(stamps) != data.get("segment_count"): errors.append(f"segment mismatch: {vid}")
    if stamps != sorted(stamps): errors.append(f"nonmonotonic timestamps: {vid}")
    duration = data.get("duration_seconds") or 0
    if duration and stamps and stamps[-1] < min(duration * .80, duration - 30): errors.append(f"incomplete duration coverage: {vid} ({stamps[-1]}/{duration})")
    if not data.get("relevance_categories"): errors.append(f"missing relevance evidence: {vid}")
    if not data.get("relevance_spans"): errors.append(f"missing timestamped relevance span: {vid}")
    if not data.get("rights_note"): errors.append(f"missing rights note: {vid}")
    raw = ROOT / data.get("raw_path", "")
    if not (raw / "source-info.json").exists() and not (raw / "legacy-source.json").exists(): errors.append(f"missing raw provenance: {vid}")
    for name, expected in data.get("raw_files", {}).items():
        rp = raw / name
        if not rp.exists(): errors.append(f"missing raw file: {vid}/{name}"); continue
        actual = hashlib.sha256(rp.read_bytes()).hexdigest()
        if actual != expected: errors.append(f"raw hash mismatch: {vid}/{name}")
if "fVut0ceg2IY" in ids: errors.append("quarantined source counted: fVut0ceg2IY")
if "I9c8STV7Hnw" not in ids: errors.append("mandatory seed missing: I9c8STV7Hnw")
ledger_path = ROOT / "quarantine" / "youtube" / "ledger.jsonl"
ledger = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()] if ledger_path.exists() else []
if not any(row.get("video_id") == "fVut0ceg2IY" for row in ledger): errors.append("mandatory exclusion missing from quarantine ledger: fVut0ceg2IY")
csv_path = ROOT / "metadata" / "sources.csv"
csv_rows = list(csv.DictReader(csv_path.open())) if csv_path.exists() else []
csv_ids = [
    row.get("stable_id") for row in csv_rows
    if row.get("platform") == "youtube"
    and row.get("status") == "accepted"
    and row.get("relevance_status") == "relevant"
]
if len(csv_ids) != len(ids) or set(csv_ids) != ids: errors.append("metadata/sources.csv YouTube inventory does not exactly match metadata files")
print(f"validated_relevant_transcripts={len(meta_files) - len({e.split(': ')[-1].split('/')[0].split(' ')[0] for e in errors if ': ' in e})}")
print(f"metadata_files={len(meta_files)}")
print(f"unique_video_ids={len(ids)}")
print(f"errors={len(errors)}")
for error in errors: print(f"ERROR {error}")
sys.exit(bool(errors))
