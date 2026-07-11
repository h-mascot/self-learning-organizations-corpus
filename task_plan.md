# Task Plan: YouTube corpus lane

## Goal
Build and prove a reproducible corpus of 100 validated, relevant, timestamped YouTube transcripts with complete provenance and rights notes.

## Phases
- [x] Phase 1: Audit repository, ingest required seed, quarantine unrelated seed, and migrate filenames
- [x] Phase 2: Build reproducible discovery, ingestion, cleaning, and validation tooling
- [ ] Phase 3: Discover and ingest relevant videos in coherent batches
- [ ] Phase 4: Run full validation, checkpoint exact results, and commit proof

## Key Questions
1. Which existing transcripts meet the complete metadata, timestamp, and relevance gates?
2. Which caption sources are usable, and which videos require ASR fallback?
3. Can all 100 sources be deterministically rebuilt and validated?

## Decisions Made
- Count only sources passing automated naming, metadata, timestamp, hash, relevance, and quarantine checks.
- Preserve raw caption evidence separately from cleaned Markdown transcripts.
- Use YouTube captions first and document ASR fallback attempts.

## Errors Encountered
- `agent-reach` executable is not installed or not on PATH; followed its documented YouTube route directly with `yt-dlp` and will record this tooling limitation.
- Initial `yt-dlp` launcher was broken (`ModuleNotFoundError: yt_dlp`); repaired with isolated `pipx install --force yt-dlp`.
- YouTube caption CDN returned HTTP 429; pipeline invoked Groq Whisper ASR fallback.
- Groq enforces 7,200 audio-seconds/hour per Whisper model; pipeline now rotates both available models and uses short-form batches.
- Cached Googlevideo audio stalled on a plain full-file request (16 KB after several minutes); explicit `Range: bytes=0-` retrieved the same complete 1.9 MB object immediately, so cached resume now uses a bounded ranged download.
- YouTube escalated to HTTP 429 plus “Sign in to confirm you’re not a bot”; Chrome cookies and the recommended EJS component did not recover page access.
- Cached signed-media recovery later suffered repeated TLS connection resets; explicit ranged downloads recovered the usable cached short-form sources.

## Status
**Currently in Phase 3** — 70 transcripts pass the strengthened canonical-name, provenance, rights, relevance, dedupe, timestamp-order, duration-coverage, seed, quarantine-ledger, and CSV-parity gates; seven cached long-form candidates are being exhausted before final blocker assessment.
