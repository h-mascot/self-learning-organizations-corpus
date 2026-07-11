# YouTube lane progress

## Final validated checkpoint

- Validated relevant transcripts: **76**.
- Metadata files: **76**.
- Unique YouTube video IDs: **76**.
- Validator errors: **0**.
- Remaining hard-gate gap: **24** videos.
- Mandatory seed `I9c8STV7Hnw`: included with 1,062 timestamped ASR segments and raw chunk JSON.
- Mandatory exclusion `fVut0ceg2IY`: quarantined, recorded in `quarantine/youtube/ledger.jsonl`, and excluded from metadata/CSV totals.
- Canonical title-derived filenames, transcript hashes, raw provenance hashes, rights notes, transcript-grounded relevance spans, timestamp ordering, duration coverage, ID dedupe, raw/metadata/transcript basename alignment, and CSV parity: all enforced by `scripts/validate_youtube.py`.

## Concrete validation output

```text
validated_relevant_transcripts=76
metadata_files=76
unique_video_ids=76
errors=0
```

## Work completed

- Migrated all six legacy ID-only transcript names; manifest: `metadata/youtube-filename-migration.json`.
- Built reproducible discovery and caption-first/ASR ingestion in `scripts/discover_youtube.py` and `scripts/youtube_pipeline.py`.
- Recorded 478 unique discovery candidates from 25 queries in `research/youtube-discovery.jsonl`.
- Repaired cached Googlevideo recovery with verified 1 MiB byte-range downloads; this recovered both short and long sources that stalled under plain transfers.
- Completed long-form Brex/Pedro Franceschi, Ramp, finance-AI, and Harvey AI transcripts from preserved signed media and Groq Whisper chunks.
- Expanded transcript-grounded relevance vocabulary to cover recursive/self-modifying agents, automated eval lifecycles, and experiment loops from the required taxonomy.
- Quarantined title-only, advertising, and unusable-transcript false positives rather than counting them.

## Quarantine evidence

- `fVut0ceg2IY`: unrelated OpenTable advertisement (mandatory exclusion).
- `yk2o6Sj3XQk`: unusable ASR containing only repeated acknowledgements.
- `dFIM6WcjYEc`: individual memory-training advertisement.
- `LRe3ffFb6AI`: adaptive case-management product explainer without organizational-learning evidence.
- `e1xTu2k2LnE`: ERP consulting advertisement without organizational-learning mechanisms.
- `wTbnxgLE-eU`: title promised a feedback loop, but the complete transcript contained no grounded learning/feedback/recursive-improvement evidence.

## Exact hard external blocker

The repository still needs 24 additional accepted videos to reach the 100-video gate. Preserved local candidates are exhausted except `ZAY9D1Y95_Q`, whose signed audio URL is expired and returns HTTP 403.

The final fresh-candidate recovery probe used the available Chrome cookie database and yt-dlp's recommended EJS component against `tLek5ad_4PY`:

```text
WARNING: [youtube] tLek5ad_4PY: Unable to download webpage: HTTP Error 429: Too Many Requests
ERROR: [youtube] tLek5ad_4PY: Sign in to confirm you’re not a bot.
```

Other attempted read-only transports were also exhausted: direct signed caption URLs returned 429; Piped metadata worked but its subtitle/media proxy returned 502; the available Invidious API returned 403; Cobalt's hosted API requires authorization and its official documentation says there is no public pre-hosted API. The agent-reach wrapper is absent, so its documented direct YouTube backend (`yt-dlp`) was used.

Because no fresh YouTube metadata, captions, or audio can currently be retrieved from this environment, the remaining 24 complete timestamped transcripts cannot be produced without an external-state change (YouTube IP challenge clearing, a working authenticated/proxied retrieval path, or newly supplied raw media/captions). No prose claim of the 100-video gate is made.
