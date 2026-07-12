# Web/media acquisition checkpoint

## Status

COMPLETE FOR LANE — all six owned quotas and lane validators pass. Manager-owned integration/schema/global-statistics/CI work remains outside this branch.

## Scope

Owned lanes: blogs/company sites, podcasts, books, conferences, case studies, GitHub, and their lane-specific query/retrieval ledgers and validators.

## Baseline counts

| Lane | Accepted | Rejected | Blocked | Quota |
|---|---:|---:|---:|---:|
| Blogs | 77 | 3 | 6 | 75 |
| Podcasts | 32 | 1 | 0 | 30 |
| Books | 30 | 144 | 0 | 25 |
| Conferences | 34 | 0 | 0 | 30 |
| Case studies | 51 | 11 | 1 | 50 |
| GitHub | 35 | 150 | 0 | 30 |

Accepted artifact levels: 32 transcript and 227 metadata-only. No record claims full text or abstract. The five early markdown files were migrated to canonical accepted/rejected records and removed after replacement verification.

Ledgers: 90 query attempts and 646 retrieval/deduplication events. Query outcomes preserve 33 successes and 57 blockers; retrieval outcomes preserve successes, rejections, and technical blockers.

## Latest commits

- Baseline: `75e3dbe`.
- Lane commit: `ab91bed` (`feat: acquire validated web and media corpus lanes`).

## Tests

- `python3 scripts/validate_web_media.py` — PASS (77/32/30/34/51/35 accepted).
- `python3 -m unittest tests.test_web_media_validator -v` — PASS (4 tests).
- `make check` — PASS (14 tests plus corpus audit/generation diff gate).
- Deterministic rematerialization — PASS; final aggregate source-record hash unchanged (`d44e68e98c4fc706d8c00642fda0be69380bcfa6d9bdd632c685e01acd668f04`) before/after the checked run.
- Manual early/middle/late samples completed in all six lanes; manual findings (404 and transcript-span selection) were fixed and validator coverage added.

## Blockers

- Shared canonical schema/global statistics integration remains manager-owned. Lane records use the isolated v2 contract documented in `research/web-media-record-format.md`.
- `agent-reach` executable and update checker were unavailable on PATH; documented Exa, Jina, and GitHub backends were used directly.
- Google Books API returned HTTP 429 with daily quota configured to zero; all 11 attempts are preserved and Open Library public metadata was used instead.
- Exa free MCP search and Jina public-reader limits were exhausted after broad discovery; exact 429 evidence is preserved. Deterministic primary-URL catalogs plus direct publisher retrieval completed the unblocked lanes.
- Seven records remain blocked: six blog origins (publisher 403/timeout/TLS plus reader 429) and the OpenAI Endava case page (publisher 403 plus reader 429). They do not count toward quotas.

## Next action

Commit the verified lane batch and hand off to the manager for schema/global-statistics integration and merge review.
