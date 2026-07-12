# Web/media acquisition checkpoint

## Status

CORRECTED AFTER INDEPENDENT REVIEW — all six owned substantive floors and the hardened lane validator pass. Manager-owned integration/schema/global-statistics/CI work remains outside this branch.

## Scope

Owned lanes: blogs/company sites, podcasts, books, conferences, case studies, GitHub, and their lane-specific query/retrieval ledgers and validators.

## Baseline counts

| Lane | Accepted | Rejected | Blocked | Quota |
|---|---:|---:|---:|---:|
| Blogs | 78 | 4 | 6 | 75 |
| Podcasts | 30 | 3 | 0 | 30 |
| Books | 30 | 144 | 0 | 25 |
| Conferences | 30 | 23 | 0 | 30 |
| Case studies | 50 | 12 | 1 | 50 |
| GitHub | 30 | 184 | 0 | 30 |

Accepted artifact levels: 248 metadata-only. Podcast records separately assert transcript availability and retain only timestamped transcript excerpts; none claims a retained complete transcript. No record claims full text, transcript, or abstract.

Ledgers: 90 query attempts and 646 retrieval/deduplication events. Query outcomes preserve 33 successes and 57 blockers; retrieval outcomes preserve successes, rejections, and technical blockers.

## Latest commits

- Baseline: `75e3dbe`.
- Acquisition commit: `3ffa11e` (`feat: acquire validated web and media corpus lanes`).
- Checkpoint pointer update: committed immediately after the acquisition commit.

## Tests

- `python3 scripts/validate_web_media.py` — PASS (78/30/30/30/50/30 accepted).
- `python3 -m unittest discover -s tests -v` — PASS (20 tests), including sponsor-ad rejection, separated podcast-span enforcement, and generic-repository rejection.
- `python3 tools/corpus.py audit` and `python3 scripts/validate_youtube.py` — PASS (101 sources; 100 relevant complete YouTube transcripts).
- Deterministic accepted-record audit — PASS; 248 accepted web/media records hash to `7985083d02011daa2dae36616a34fe511b49e1d9bcedcbb42f09a0ddb58bcda1` in sorted filename order.
- Manager-owned generated README/statistics files were intentionally not modified on this worker branch.

## Blockers

- Shared canonical schema/global statistics integration remains manager-owned. Lane records use the isolated v2 contract documented in `research/web-media-record-format.md`.
- `agent-reach` executable and update checker were unavailable on PATH; documented Exa, Jina, and GitHub backends were used directly.
- Google Books API returned HTTP 429 with daily quota configured to zero; all 11 attempts are preserved and Open Library public metadata was used instead.
- Exa free MCP search and Jina public-reader limits were exhausted after broad discovery; exact 429 evidence is preserved. Direct primary publisher retrieval and the authenticated GitHub API completed the unblocked lanes.
- Seven records remain blocked: six blog origins (publisher 403/timeout/TLS plus reader 429) and the OpenAI Endava case page (publisher 403 plus reader 429). They do not count toward quotas.

## Next action

Commit the verified lane batch and hand off to the manager for schema/global-statistics integration and merge review.
