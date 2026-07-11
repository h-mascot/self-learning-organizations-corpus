# Self-Learning Organizations Corpus

Open research corpus about self-learning, self-improving, AI-native organizations and recursive organizational feedback loops.

## Contents
- `transcripts/youtube/` — timestamped source transcripts
- `raw/youtube/` — immutable caption/ASR evidence and source metadata
- `metadata/youtube/` — per-source provenance, hashes, relevance spans, and rights notes
- `metadata/videos.csv` — source inventory
- `scripts/youtube_pipeline.py` — caption-first ingestion with ASR fallback
- `scripts/validate_youtube.py` — corpus completion gate
- `research/` — taxonomy, reports, synthesis, and source notes

## Principles
Preserve provenance. Separate verbatim transcripts from analysis. Record licenses/usage constraints per source. Never imply transcript copyright ownership.

## Status
YouTube expansion is underway. Run `python3.11 scripts/validate_youtube.py` for the exact validated count.
