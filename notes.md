# Notes: YouTube corpus lane

## Repository baseline
- Branch: `goal/youtube`
- Existing YouTube transcript files: 6
- Existing relevant candidates: 5
- Required missing seed: `I9c8STV7Hnw`
- Required quarantine: `fVut0ceg2IY` (OpenTable advertisement; unrelated)

## Retrieval environment
- `yt-dlp`: available at `/home/henrymascot/.local/bin/yt-dlp`
- `ffmpeg`: available at `/usr/bin/ffmpeg`
- `agent-reach`: unavailable on PATH; its documented direct YouTube backend is `yt-dlp`

## Discovery notes

- 25 reproducible search queries yielded 478 unique candidates.
- Caption retrieval is externally rate-limited (HTTP 429), so ASR is currently the operative fallback.
- Current checkpoint: 70 relevant sources pass strengthened transcript-grounded validation (`metadata_files=70`, `unique_video_ids=70`, `errors=0`).
- Quarantined during validation: `yk2o6Sj3XQk` (ASR returned only repeated “Thank you”) and `dFIM6WcjYEc` (individual memory-training advertisement).
- Groq exposes `whisper-large-v3` and `whisper-large-v3-turbo`, each with a 7,200 audio-seconds/hour limit.
- Final YouTube probe with Chrome cookies and `--remote-components ejs:github` returned HTTP 429 and “Sign in to confirm you’re not a bot.”
- 47 attempted/unresolved sources are materialized in `research/progress/youtube-failures.jsonl`.
- Ranged cached-audio downloads removed the transport stall and enabled additional short-form completions; transcript-grounded review quarantined title-only false positives.
