# Engineering/QA lane checkpoint

## Delivered

- Canonical source layout: `sources/<platform>/<accepted|rejected>/` with ten supported platform names.
- Canonical source contract: `schema/source.schema.json` plus standard-library enforcement in `tools/corpus.py`.
- Deterministic title-derived filenames: `<date>--<normalized-title>--<publisher>--<stable-id>.md`.
- Collision-safe, two-phase legacy migration with `metadata/migration-manifest.csv`; all six transcript bodies were retained exactly and hashed.
- Canonical YouTube URL normalization and stable-ID consistency checks.
- SHA-256 content hashes, stable-ID and URL dedupe, provenance/rights requirements, date/duration checks, transcript completeness gates, and relevance/counting gates.
- `fVut0ceg2IY` preserved in the rejected tree and generated rejection log, excluded from relevant/transcript totals.
- Generated canonical inventory, rejected-source log, statistics, and README.
- Dependency-free unit tests and GitHub Actions CI (`make check`).
- Legacy `metadata/videos.csv` preserved at `metadata/legacy/videos.csv` for audit history.

## Verification

- `python3 -m unittest discover -s tests -v`: 10 tests passed.
- `python3 tools/corpus.py audit`: 6 sources validated.
- `python3 -m compileall -q tools tests`: passed.
- `python3 -m json.tool schema/source.schema.json`: passed.
- Generated totals: 6 discovered, 5 validated relevant, 5 complete timestamped transcripts, 1 rejected.

## Remaining incompatibilities and out-of-lane gates

- The corpus currently has 5 validated relevant videos, not the north-star gate of 100+.
- Required seed `I9c8STV7Hnw` is not present in this worktree and was not invented or fetched in the engineering lane.
- Non-YouTube platform directories have no source records yet; the schema and generated zero-count table are ready for ingestion.
- Research-loop, competitive benchmark, Ramp, deep-research artifact, credential recovery, GitHub push, and live-GitHub verification gates remain for their respective lanes/manager. This lane did not push, per worker instructions.
- Legacy CSV paths intentionally remain historical evidence; consumers must use generated `metadata/sources.csv`.
