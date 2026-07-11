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
- First validated checkpoint: 43 relevant sources with timestamped transcript evidence.
- Quarantined during validation: `yk2o6Sj3XQk` (ASR returned only repeated “Thank you”) and `dFIM6WcjYEc` (individual memory-training advertisement).
- Groq exposes `whisper-large-v3` and `whisper-large-v3-turbo`, each with a 7,200 audio-seconds/hour limit.
