#!/usr/bin/env python3
"""Reproducible caption-first YouTube transcript ingestion.

The corpus stores source metadata, raw caption/ASR evidence, a cleaned timestamped
Markdown transcript, hashes, relevance evidence, and an explicit rights note.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS = ROOT / "transcripts" / "youtube"
RAW = ROOT / "raw" / "youtube"
META = ROOT / "metadata" / "youtube"
CSV_PATH = ROOT / "metadata" / "videos.csv"

TERMS = {
    "organizational-learning": ["organizational learning", "organisational learning", "learning organization", "learning organisation", "learn as an organization", "organisation as a whole can learn"],
    "continuous-improvement": ["continuous improvement", "kaizen", "improvement loop", "experiment their way forward", "pdsa"],
    "feedback-systems": ["feedback loop", "cybernetic", "systems thinking", "viable system"],
    "ai-native-company": ["ai native", "ai-native", "company with ai", "agentic organization"],
    "organizational-memory": ["organizational memory", "organisational memory", "organisation's memory", "corporate memory", "company brain", "second brain", "institutional knowledge", "knowledge management", "company knowledge", "siloed emails"],
    "adaptive-enterprise": ["adaptive enterprise", "adaptive organization", "adaptable organization", "adaptable organizations", "self organizing"],
    "agent-operations": ["ai agent", "agents", "agent monitoring", "agent evaluation", "eval driven"],
    "experimentation-flywheel": ["experimentation", "data flywheel", "self optimizing", "decision intelligence"],
    "named-lanes": ["pedro franceschi", "brex", "ramp", "y combinator"],
}


def run(args: list[str], **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def slug(text: str) -> str:
    value = html.unescape(text).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:100].rstrip("-") or "untitled"


def base_name(info: dict) -> str:
    date = info.get("upload_date") or "unknown-date"
    if len(date) == 8 and date.isdigit():
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    publisher = info.get("channel") or info.get("uploader") or "unknown-publisher"
    return f"{date}--{slug(info.get('title') or 'untitled')}--{slug(publisher)}--{info['id']}"


def timestamp(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_vtt(path: Path) -> list[dict]:
    lines = path.read_text(errors="replace").splitlines()
    segments, seen = [], set()
    i = 0
    while i < len(lines):
        match = re.match(r"(\d\d):(\d\d):(\d\d)[.,]\d+ -->", lines[i])
        if not match:
            i += 1
            continue
        start = int(match[1]) * 3600 + int(match[2]) * 60 + int(match[3])
        i += 1
        text = []
        while i < len(lines) and lines[i].strip():
            cleaned = re.sub(r"<[^>]+>", "", lines[i]).strip()
            if cleaned and cleaned not in text:
                text.append(cleaned)
            i += 1
        value = html.unescape(" ".join(text)).strip()
        key = (start, value)
        if value and key not in seen:
            segments.append({"start": start, "text": value})
            seen.add(key)
    return segments


def groq_key() -> str | None:
    if os.environ.get("GROQ_API_KEY"):
        return os.environ["GROQ_API_KEY"]
    config = Path.home() / ".agent-reach" / "config.yaml"
    if config.exists():
        match = re.search(r"^groq_api_key:\s*(.+)$", config.read_text(), re.M)
        if match:
            return match.group(1).strip().strip("'\"")
    return None


def transcribe_asr(url: str, work: Path, raw_dir: Path, cached_info: dict | None = None) -> tuple[list[dict], list[str]]:
    key = groq_key()
    if not key:
        raise RuntimeError("ASR fallback unavailable: no GROQ_API_KEY or agent-reach Groq key")
    audio = work / "audio-source"
    if cached_info:
        prefetched = Path("/tmp/youtube-cached-audio") / cached_info["id"]
        if prefetched.exists():
            shutil.copy2(prefetched, audio)
        else:
            formats = [f for f in cached_info.get("formats", []) if f.get("vcodec") == "none" and f.get("acodec") not in (None, "none") and f.get("url")]
            if not formats: raise RuntimeError("Cached source metadata has no signed audio format URL")
            selected = min(formats, key=lambda f: f.get("abr") or 99999)
            run(["curl", "-fsSL", "--retry", "8", "--retry-all-errors", "--continue-at", "-", "-o", str(audio), selected["url"]])
    else:
        audio = work / "audio.mp3"
        run(["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "--audio-quality", "9", "-o", str(audio), url])
    chunks = work / "chunks"
    chunks.mkdir()
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(audio), "-f", "segment", "-segment_time", "600", "-ac", "1", "-ar", "16000", "-b:a", "32k", str(chunks / "%03d.mp3")])
    output, models_used = [], []
    models = ["whisper-large-v3", "whisper-large-v3-turbo"]
    if int(hashlib.sha256(url.encode()).hexdigest(), 16) % 2:
        models.reverse()
    for idx, chunk in enumerate(sorted(chunks.glob("*.mp3"))):
        raw_json = raw_dir / f"asr-{idx:03d}.json"
        # ASPH quotas are rolling hourly windows. Keep the already-downloaded
        # chunk and retry in place rather than redownloading or losing work.
        for attempt in range(120):
            model = models[attempt % len(models)]
            result = subprocess.run([
                "curl", "-sS", "-X", "POST", "https://api.groq.com/openai/v1/audio/transcriptions",
                "-H", f"Authorization: Bearer {key}", "-F", f"file=@{chunk}",
                "-F", f"model={model}", "-F", "response_format=verbose_json",
                "-F", "timestamp_granularities[]=segment",
            ], capture_output=True, text=True)
            data = json.loads(result.stdout or "{}")
            if data.get("segments"):
                raw_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
                models_used.append(model)
                break
            if attempt == 119:
                raise RuntimeError(f"Groq ASR failed: {data.get('error', data)}")
            message = str(data.get("error", {}).get("message", ""))
            retry = re.search(r"try again in ([0-9.]+)s", message, re.I)
            time.sleep(max(15, float(retry.group(1)) if retry else min(60, 2 ** min(attempt, 6))))
        offset = idx * 600
        output.extend({"start": offset + float(s["start"]), "text": s["text"].strip()} for s in data["segments"] if s.get("text", "").strip())
    return output, sorted(set(models_used))


def fetch_info(url: str, work: Path) -> dict:
    path = work / "info.json"
    with path.open("w") as f:
        run(["yt-dlp", "--dump-single-json", "--skip-download", url], stdout=f)
    return json.loads(path.read_text())


def relevance(info: dict, segments: list[dict]) -> tuple[list[str], list[str], list[dict]]:
    transcript = " ".join(s["text"] for s in segments).lower()
    categories, evidence, spans = [], [], []
    for category, phrases in TERMS.items():
        matches = [p for p in phrases if p in transcript]
        if matches:
            categories.append(category)
            evidence.extend(matches[:2])
            for phrase in matches[:2]:
                segment = next(s for s in segments if phrase in s["text"].lower())
                spans.append({"category": category, "timestamp": timestamp(segment["start"]), "phrase": phrase, "text": segment["text"][:300]})
    return categories, sorted(set(evidence)), spans


def write_source(info: dict, segments: list[dict], method: str, raw_dir: Path, caption_error: str | None = None, asr_models: list[str] | None = None) -> Path:
    name = base_name(info)
    transcript_path = TRANSCRIPTS / f"{name}.md"
    meta_path = META / f"{name}.json"
    categories, evidence, spans = relevance(info, segments)
    raw_hashes = {p.name: sha256(p) for p in sorted(raw_dir.glob("*")) if p.is_file()}
    metadata = {
        "video_id": info["id"], "title": info.get("title"), "channel": info.get("channel") or info.get("uploader"),
        "source_url": info.get("webpage_url") or f"https://www.youtube.com/watch?v={info['id']}",
        "duration_seconds": info.get("duration"), "upload_date": info.get("upload_date"),
        "availability": info.get("availability"), "license": info.get("license"),
        "transcript_method": method, "asr_models": asr_models or [], "caption_error": caption_error,
        "raw_files": raw_hashes, "segment_count": len(segments),
        "relevance_categories": categories, "relevance_evidence": evidence, "relevance_spans": spans,
        "rights_note": "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed.",
    }
    front = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in metadata.items() if k != "raw_files"] + [f"raw_files: {json.dumps(raw_hashes, sort_keys=True)}", "---", "", f"# {info.get('title')}", ""]
    body = [f"{timestamp(s['start'])} {s['text']}" for s in segments]
    transcript_path.write_text("\n".join(front + body) + "\n")
    metadata["transcript_sha256"] = sha256(transcript_path)
    metadata["transcript_path"] = str(transcript_path.relative_to(ROOT))
    metadata["raw_path"] = str(raw_dir.relative_to(ROOT))
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    rebuild_csv()
    return transcript_path


def rebuild_csv() -> None:
    fields = ["video_id", "title", "channel", "source_url", "duration_seconds", "upload_date", "transcript_method", "transcript_path", "raw_path", "transcript_sha256", "relevance_categories", "rights_note"]
    rows = []
    for path in sorted(META.glob("*.json")):
        data = json.loads(path.read_text())
        row = {k: data.get(k, "") for k in fields}
        row["relevance_categories"] = "|".join(data.get("relevance_categories", []))
        rows.append(row)
    with CSV_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def ingest(url: str, prebuilt_asr: Path | None = None) -> Path:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True); META.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="youtube-ingest-") as temp:
        work = Path(temp)
        info = fetch_info(url, work)
        raw_dir = RAW / base_name(info)
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "source-info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n")
        caption_error = None
        try:
            run(["yt-dlp", "--write-subs", "--write-auto-subs", "--sub-langs", "en-orig,en", "--sub-format", "vtt", "--skip-download", "-o", str(work / "caption.%(ext)s"), url], capture_output=True)
            caption = next(work.glob("caption*.vtt"))
            shutil.copy2(caption, raw_dir / "captions.vtt")
            segments, method = parse_vtt(caption), "youtube-captions"
        except Exception as exc:
            caption_error = ((exc.stderr if isinstance(exc, subprocess.CalledProcessError) else "") or str(exc)).strip()[-2000:]
            if prebuilt_asr:
                for p in sorted(prebuilt_asr.glob("*.json")):
                    shutil.copy2(p, raw_dir / f"asr-{p.name}")
                segments = []
                for idx, p in enumerate(sorted(prebuilt_asr.glob("*.json"))):
                    data = json.loads(p.read_text())
                    segments.extend({"start": idx * 600 + float(s["start"]), "text": s["text"].strip()} for s in data["segments"] if s.get("text", "").strip())
            else:
                segments, asr_models = transcribe_asr(url, work, raw_dir)
            method = "groq-whisper-asr"
        if not segments:
            raise RuntimeError("No transcript segments produced")
        return write_source(info, segments, method, raw_dir, caption_error, locals().get("asr_models", ["whisper-large-v3-turbo"] if prebuilt_asr else []))


def resume_cached(raw_dir: Path) -> Path:
    info = json.loads((raw_dir / "source-info.json").read_text())
    with tempfile.TemporaryDirectory(prefix="youtube-resume-") as temp:
        segments, models = transcribe_asr(info.get("webpage_url") or f"https://www.youtube.com/watch?v={info['id']}", Path(temp), raw_dir, info)
    return write_source(info, segments, "groq-whisper-asr", raw_dir, "YouTube captions unavailable; recovered from cached signed audio URL.", models)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--prebuilt-asr", type=Path)
    parser.add_argument("--resume-cached", action="store_true")
    parser.add_argument("--max-duration", type=int, default=600)
    args = parser.parse_args()
    if args.resume_cached:
        existing = {json.loads(p.read_text())["video_id"] for p in META.glob("*.json")}
        for info_path in sorted(RAW.glob("*/source-info.json")):
            info = json.loads(info_path.read_text())
            if info.get("id") in existing or (info.get("duration") or 0) > args.max_duration: continue
            try: print(resume_cached(info_path.parent))
            except Exception as exc: print(f"FAILED-CACHED {info.get('id')}: {exc}")
        rebuild_csv()
        return
    for url in args.urls:
        try:
            print(ingest(url, args.prebuilt_asr))
        except Exception as exc:
            print(f"FAILED {url}: {exc}", flush=True)


if __name__ == "__main__":
    main()
