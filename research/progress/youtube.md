# YouTube lane progress

## Baseline

- Started from 6 ID-only transcript files and 6 metadata rows.
- Five sources appear topically relevant; `fVut0ceg2IY` is an unrelated OpenTable advertisement and must be quarantined.
- `I9c8STV7Hnw` is required and missing.

## Current checkpoint

- Validated relevant transcripts: **43** (`errors=0`).
- Mandatory seed ingestion: complete (`I9c8STV7Hnw`, 1,062 ASR segments, raw chunk JSON preserved).
- Filename migration: complete for all six legacy files; manifest at `metadata/youtube-filename-migration.json`.
- Required quarantine: complete (`fVut0ceg2IY`, unrelated OpenTable advertisement, excluded from metadata/count).
- Reproducible pipeline: implemented in `scripts/youtube_pipeline.py`; validator in `scripts/validate_youtube.py`.

## Retrieval/tooling notes

- Caption-first retrieval uses `yt-dlp` per the agent-reach YouTube route.
- The `agent-reach` wrapper is unavailable on PATH; direct `yt-dlp` is installed and usable.
- Caption download for the mandatory seed returned HTTP 429; Groq Whisper ASR fallback succeeded.
- Both available Groq Whisper models have externally reported 7,200 audio-seconds/hour limits. Ingestion is batched across quota windows.

## Validation checkpoint

```text
validated_relevant_transcripts=43
metadata_files=43
unique_video_ids=43
errors=0
```

## Quarantine additions

- `fVut0ceg2IY`: unrelated restaurant advertisement (required exclusion).
- `yk2o6Sj3XQk`: unusable ASR output containing only repeated acknowledgements.
- `dFIM6WcjYEc`: individual memory-training advertisement, not organizational learning/memory.
