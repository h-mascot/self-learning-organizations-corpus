# Self-Learning Organizations Corpus

Open research corpus about self-learning, self-improving, AI-native organizations and recursive organizational feedback loops.

## Corpus status

- Accounted canonical/evidence records: **1054**
- Accepted relevant sources: **640**
- Retrieved records (including accepted/rejected): **1054**
- Rejected records: **414**
- Blocked retrieval records: **0**
- Complete timestamped YouTube transcripts: **101**

| Platform | Discovered | Retrieved | Accepted | Rejected | Blocked | Artifact levels | Rights statuses | Provenance coverage |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| youtube | 102 | 102 | 101 | 1 | 0 | transcript: 102 | third-party: 102 | 102 records / 5 distinct values |
| academic | 201 | 201 | 187 | 14 | 0 | abstract: 165, full_text: 13, metadata_only: 23 | open-license: 27, third-party-metadata-and-abstract: 174 | 201 records / 201 distinct values |
| x | 50 | 50 | 50 | 0 | 0 | full_text: 50 | third-party: 50 | 50 records / 1 distinct values |
| reddit | 25 | 25 | 25 | 0 | 0 | full_text: 25 | third-party: 25 | 25 records / 1 distinct values |
| substack | 25 | 25 | 25 | 0 | 0 | metadata_only: 25 | third-party: 25 | 25 records / 1 distinct values |
| blogs | 87 | 87 | 80 | 7 | 0 | metadata_only: 80, unavailable: 7 | bounded-public-evidence: 82, retrieval-evidence-only: 5 | 87 records / 9 distinct values |
| podcasts | 51 | 51 | 30 | 21 | 0 | metadata_only: 30, unavailable: 21 | bounded-public-evidence: 50, retrieval-evidence-only: 1 | 51 records / 50 distinct values |
| conferences | 53 | 53 | 30 | 23 | 0 | metadata_only: 30, unavailable: 23 | bounded-public-evidence: 53 | 53 records / 2 distinct values |
| books | 174 | 174 | 30 | 144 | 0 | metadata_only: 30, unavailable: 144 | metadata-only: 174 | 174 records / 174 distinct values |
| case-studies | 63 | 63 | 51 | 12 | 0 | metadata_only: 51, unavailable: 12 | bounded-public-evidence: 53, retrieval-evidence-only: 10 | 63 records / 4 distinct values |
| github | 223 | 223 | 31 | 192 | 0 | metadata_only: 31, unavailable: 192 | bounded-public-evidence: 14, open-license: 209 | 223 records / 223 distinct values |

| Artifact level | Records |
| --- | ---: |
| abstract | 165 |
| full_text | 88 |
| metadata_only | 300 |
| transcript | 102 |
| unavailable | 399 |

| Lifecycle | Records |
| --- | ---: |
| accepted | 640 |
| rejected | 414 |

| Rights status | Records |
| --- | ---: |
| bounded-public-evidence | 252 |
| metadata-only | 174 |
| open-license | 236 |
| retrieval-evidence-only | 16 |
| third-party | 202 |
| third-party-metadata-and-abstract | 174 |

## Layout and contracts

- `sources/youtube/<lifecycle>/` contains strict canonical transcript records.
- `sources/academic/<source-type>/<lifecycle>/` contains academic metadata, abstract, or legally available full-text records.
- Web/media platform directories contain strict JSON acquisition records; social and legacy evidence may use canonical Markdown. Dispatch is by record format and path, not schema version alone.
- `schema/source.schema.json` documents the canonical cross-platform contract and academic specialization.
- `metadata/sources.csv`, `metadata/rejected-sources.csv`, and `metadata/statistics.json` are deterministic generated views.
- `research/recursive-loops/` contains the separate 200-loop dependent research DAG; its artifacts are not double-counted as corpus sources.

Canonical validation rejects duplicate stable IDs and normalized URLs globally. Markdown body hashes are also deduplicated; web/media evidence-array hashes are integrity checks because empty or shared bounded evidence is not a source identity. Placeholder `.gitkeep` files and `sources/README.md` are never records. Run `make check` before committing; it verifies regeneration is clean and preserves the dedicated lane gates.

## Human review UI

Run the stdlib HTTP server from the repository root:

```bash
make review
# equivalent: python3 review-ui/review.py serve --host 0.0.0.0 --port 8765
```

Open `http://100.106.69.9:8765/` on the tailnet (or `http://127.0.0.1:8765/` locally). The UI indexes every canonical record in `sources/`, supports platform and Ada-category tabs, search, pagination, pending-only review, safe bulk actions, and Accept / Maybe / Reject decisions with comments. Accept emits a positive “find more like this” seed; Reject emits a negative “avoid similar” seed. Decisions persist as versionable overlays in `review-ui/data/decisions.json`; similarity seeds, category preferences, and the future-research queue are regenerated in `review-ui/data/feedback.json`. Reviewing never changes canonical sources.

Useful commands:

```bash
python3 review-ui/review.py report                 # decisions + feedback queue
python3 review-ui/review.py report --json          # machine-readable report
python3 review-ui/review.py export-feedback        # refresh feedback.json
python3 review-ui/review.py apply                   # dry-run plan (default)
python3 review-ui/review.py apply --yes             # explicitly apply moves/metadata changes
```

`apply` is deliberately dry-run unless `--yes` is present. Inspect and commit the overlay data first, run the dry-run, then use `--yes` only when intentionally promoting review decisions into `sources/`. Run `make check` after any real apply.

## Counting and rights policy

Only `accepted` + `relevant` records count as validated sources. Artifact levels distinguish full text, transcripts, abstracts, excerpts, metadata-only records, unavailable artifacts, and failed retrieval evidence. Statistics retain platform, lifecycle, artifact, rights-status, and provenance dimensions. A URL to full text does not itself make a record `full_text`; the preserved body must contain it. Third-party content remains subject to the declared rights holder and source terms, and inclusion transfers no ownership.

_This README is generated by `python3 tools/corpus.py generate`._
