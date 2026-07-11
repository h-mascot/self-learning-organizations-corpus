# Notes: Engineering/QA Corpus Lane

## Repository inventory

- Six ID-only YouTube Markdown transcripts with flat front matter and timestamped bodies.
- Five sources are relevant; `fVut0ceg2IY` is an unrelated 20-second OpenTable ad explicitly identified by GOAL.md and research notes.
- `metadata/videos.csv` is the only legacy inventory. No validator, tests, schema, package dependencies, or CI existed.
- Research prose links to public YouTube URLs, not local transcript filenames, so path migration does not require prose link rewrites.

## Contract decisions

- Canonical path: `sources/<platform>/<accepted|rejected>/<date>--<title>--<publisher>--<stable-id>.md`.
- Flat YAML front matter is intentionally parseable with the Python standard library while the JSON Schema remains the declarative contract.
- Accepted transcripts must be non-empty, timestamped, and reach at least 80% of declared duration.
- Rejected sources remain in discovery and rejection counts but never validated-relevant or complete-transcript counts.

## Verification evidence

- Initial and post-migration unit runs: 10/10 tests passed.
- Audit: 6/6 source records valid.
- Generated counts: 6 discovered, 5 validated relevant, 5 complete timestamped transcripts, 1 rejected.
- Manifest contains whole-file pre-migration SHA-256 and preserved-body SHA-256 for every migrated source.
