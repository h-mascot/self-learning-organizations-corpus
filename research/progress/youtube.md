# YouTube lane progress

## Baseline

- Started from 6 ID-only transcript files and 6 metadata rows.
- Five sources appear topically relevant; `fVut0ceg2IY` is an unrelated OpenTable advertisement and must be quarantined.
- `I9c8STV7Hnw` is required and missing.

## Current checkpoint

- Validated relevant transcripts: **64** (`errors=0`).
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

Final blocker checkpoint:

```text
validated_relevant_transcripts=64
metadata_files=64
unique_video_ids=64
errors=0
```

## Quarantine additions

- `fVut0ceg2IY`: unrelated restaurant advertisement (required exclusion).
- `yk2o6Sj3XQk`: unusable ASR output containing only repeated acknowledgements.
- `dFIM6WcjYEc`: individual memory-training advertisement, not organizational learning/memory.
- `LRe3ffFb6AI`: adaptive case-management product explainer without learning mechanisms.
- `e1xTu2k2LnE`: ERP consulting advertisement without organizational-learning mechanisms.

## Hard external blocker

After 64 validated transcripts, the final recovery probe used both the available Chrome cookie database and yt-dlp's recommended remote EJS component:

```text
WARNING: [youtube] Xsrcf1jMFWk: Unable to download webpage: HTTP Error 429: Too Many Requests
ERROR: [youtube] Xsrcf1jMFWk: Sign in to confirm you’re not a bot.
```

Cached signed audio URLs were attempted without new YouTube page requests. Google Video repeatedly returned `OpenSSL SSL_read: Connection reset by peer`; signed URLs are time-limited. Groq also enforced 7,200 audio-seconds/hour on each available Whisper model. The 47 attempted but unresolved source IDs, URLs, and last errors are preserved in `research/progress/youtube-failures.jsonl`.
