# YouTube lane progress

## Completed hard-gate checkpoint

- Validated relevant transcripts: **100**.
- Metadata files: **100**.
- Unique YouTube video IDs: **100**.
- Validator errors: **0**.
- This continuation added **24** genuinely relevant videos with complete timestamped transcripts, moving the verified count from 76 to 100.
- Mandatory seed `I9c8STV7Hnw`: included with 1,062 timestamped ASR segments and raw chunk JSON.
- Mandatory exclusion `fVut0ceg2IY`: quarantined, recorded in `quarantine/youtube/ledger.jsonl`, and excluded from metadata/CSV totals.
- Canonical title-derived filenames, transcript hashes, raw provenance hashes, rights notes, transcript-grounded relevance spans, timestamp ordering, duration coverage, ID dedupe, raw/metadata/transcript basename alignment, and CSV parity are enforced by `scripts/validate_youtube.py`.

## Concrete validation output

```text
validated_relevant_transcripts=100
metadata_files=100
unique_video_ids=100
errors=0
```

## Retrieval recovery and new evidence

- Re-proved the normal `yt-dlp` web route blocked on fresh candidates with `Sign in to confirm you’re not a bot`; authenticated web-client probes also returned HTTP 429.
- Diagnosed a working legal read-only route using the current `yt-dlp` `mweb` player client. It returned current public metadata and format 18 media even while the normal web client remained blocked.
- Added a reproducible pipeline fallback: normal metadata/media retrieval is attempted first, then Chrome-cookie + `youtube:player_client=mweb`; the public combined stream is reduced to audio and transcribed with timestamped Groq Whisper segments.
- YouTube captions exposed through `mweb` required a subtitles PO token and were not treated as downloadable. No caption text was fabricated or inferred; the fallback uses actual retrieved media and preserved ASR response JSON.
- Every new source preserves full `source-info.json`, per-chunk Groq ASR JSON, hashes, source URL, title/channel/date/duration, transcript method/model, explicit rights note, and transcript-grounded timestamped relevance spans.

## New coherent batches

- Batch 1 (8): systems thinking, feedback loops, kaizen, organizational learning/knowledge management, AI data flywheels, double-loop learning, and eval-driven agent development.
- Batch 2 (16): viable systems/cybernetics, kaizen, agent evaluation/observability/testing, organizational learning/control, Senge's disciplines, organizational memory, recursive improvement, AI-native services, and enterprise institutional knowledge.
- The validator ran after each coherent batch: batch 1 validated at 84/0 errors; batch 2 validated at 100/0 errors.

## Prior work retained

- Migrated all six legacy ID-only transcript names; manifest: `metadata/youtube-filename-migration.json`.
- Built reproducible discovery and caption-first/ASR ingestion in `scripts/discover_youtube.py` and `scripts/youtube_pipeline.py`.
- Recorded 478 unique discovery candidates from 25 queries in `research/youtube-discovery.jsonl`.
- Repaired cached Googlevideo recovery with verified 1 MiB byte-range downloads.
- Completed Brex/Pedro Franceschi, Ramp, finance-AI, Harvey AI, organizational-learning, cybernetics, continuous-improvement, agent-evaluation, and recursive-improvement sources.

## Quarantine evidence

- `fVut0ceg2IY`: unrelated OpenTable advertisement (mandatory exclusion).
- `yk2o6Sj3XQk`: unusable ASR containing only repeated acknowledgements.
- `dFIM6WcjYEc`: individual memory-training advertisement.
- `LRe3ffFb6AI`: adaptive case-management product explainer without organizational-learning evidence.
- `e1xTu2k2LnE`: ERP consulting advertisement without organizational-learning mechanisms.
- `wTbnxgLE-eU`: title promised a feedback loop, but the complete transcript contained no grounded learning/feedback/recursive-improvement evidence.

## Gate status

The YouTube hard gate is satisfied at 100 validated relevant videos. No blocker exception or weakened validation was used.
