# Social acquisition checkpoint

Status: lane gates pass locally with bounded public-index evidence.

## Exact accepted counts

- X: 50
- Reddit: 25
- Substack/newsletters: 25
- Total: 100
- Artifact level: 100 `metadata_only`; 0 claimed full text

All accepted records include a canonical URL, stable ID, publisher/creator (or an explicit public-index limitation for Reddit handles), date or `unknown`, retrieval timestamp, SHA-256 body hash, relevance evidence, provenance, and rights status. Each body labels the evidence as a bounded excerpt.

## Voxyz recovery

Recovered `https://x.com/Voxyz_ai/status/2060030680369627237` from session-accessible evidence under the local Hermes/Clawd archive. The archived browser-state transcript displayed the exact URL and a later session note identified the tweet as the source that triggered a comparison of gstack, Superpowers, and Compound Engineering. Direct body retrieval remains blocked by missing X authentication and Jina's temporary anonymous-X abuse block; the record therefore remains `metadata_only` and does not invent the post body.

## Reproducibility and validation

- Materialize: `python scripts/social_acquisition.py`
- Validate: `python scripts/validate_social_lane.py`
- Tests: `python -m unittest tests.test_social_lane`
- Repository audit: `python tools/corpus.py audit` (`validated 201 sources`)

`make check` runs all 13 tests and the audit successfully, then stops at its generated-artifact diff because incorporating these 100 records requires edits to `README.md` and `metadata/{sources.csv,statistics.json}`. Those files are manager-owned and explicitly out of scope for this branch, so they were restored rather than committed here.

## Preserved limitations

See `research/social/query-log.jsonl`, `research/social/rejected.jsonl`, and `research/social/blockers.jsonl`. Direct X and Reddit retrieval was unavailable. Public search result pages supplied the bounded evidence, so none of these records claim full-text retrieval. Newsletter records cover the GOAL's combined Substack/newsletters channel and retain the publisher URL rather than pretending every newsletter is hosted by Substack.
