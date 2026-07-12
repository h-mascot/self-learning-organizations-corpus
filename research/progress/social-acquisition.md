# Social acquisition independent-review correction

Status: lane validator and quotas pass on resource-level source evidence; manager-owned generated files remain untouched.

## Honest accepted counts

| Platform | Accepted | `full_text` | `metadata_only` |
| --- | ---: | ---: | ---: |
| X | 50 | 50 | 0 |
| Reddit | 25 | 25 | 0 |
| Substack/newsletters | 25 | 0 | 25 |
| **Total** | **100** | **75** | **25** |

`full_text` means the complete X post/X Article or Reddit self-post body returned by the named public resource endpoint is retained. Newsletter records remain honestly `metadata_only`: each contains a substantial bounded span from a direct fetch of an individual `/p/...` article, not a complete redistributed article.

## Independent-review corrections

- Audited all 100 accepted resources rather than accepting quota arithmetic.
- Replaced all publication-homepage newsletter records with individual article URLs.
- Removed generic synthesized descriptions and thin search-only evidence.
- Recovered exact X authors, canonical IDs/redirects, UTC dates, and complete post/X Article text through the FxTwitter public read API.
- Replaced Reddit snippets and unknown authors/dates with exact canonical IDs, authors, `created_utc`, permalinks, and complete self-post bodies from the Arctic Shift public archive.
- Removed all `0001-01-01` sentinels and year-1 filenames.
- Rejected 60+ superseded, thin, homepage-only, or off-topic resources in `research/social/rejected.jsonl`.
- Preserved raw responses under `research/social/raw/` and precise queries/endpoints in `research/social/query-log.jsonl`.

## Verification

- `python scripts/validate_social_lane.py`: `{'x': 50, 'reddit': 25, 'substack': 25}`
- `python -m unittest discover -s tests -v`: 17 tests pass.
- `python tools/corpus.py audit`: `validated 201 sources`.
- `make check`: tests, audit, and generation pass; the final generated-artifact diff gate fails because it expects updates to manager-owned `README.md` and `metadata/{sources.csv,statistics.json}`. Those generated changes were deliberately restored and are not part of this branch.

## Remaining blockers

- `agent-reach doctor` is unavailable in this environment (`command not found`).
- Authenticated first-party X/Reddit CLIs remain unavailable; public read/archive sources were used and their raw responses preserved.
- Manager must regenerate and commit shared README/metadata after merging this lane.
