# Academic Recovery Lane Checkpoint

## Status

Academic GOAL gate passes locally. The lane audited and dispositioned every one of the 200 legacy OpenAlex-derived records without editing manager-owned shared schema, statistics, README, corpus tooling, or global status files.

## Exact accounting

- Legacy inputs audited: **200/200**
- Canonical academic records: **200**
- Accepted relevant, deduplicated records: **186** (academic minimum: 150)
- Rejected records: **14**
  - Duplicate records: **9**
  - Topically irrelevant records: **5**
- Unaccounted legacy records: **0**
- Records honestly classified as arXiv: **0** (none has a proven arXiv identifier or canonical arxiv.org URL)

### Actual source type

| Source type | All | Accepted | Rejected |
| --- | ---: | ---: | ---: |
| Journal article | 148 | 139 | 9 |
| Conference paper | 28 | 27 | 1 |
| Book/chapter | 10 | 8 | 2 |
| Repository/preprint | 13 | 11 | 2 |
| Thesis | 1 | 1 | 0 |
| arXiv | 0 | 0 | 0 |
| Other academic | 0 | 0 | 0 |

### Artifact level

| Artifact level | All | Accepted | Rejected |
| --- | ---: | ---: | ---: |
| Full text | 13 | 12 | 1 |
| Abstract | 164 | 152 | 12 |
| Metadata only | 23 | 22 | 1 |

Only OpenAlex reconstructed abstracts count as `abstract`. Legacy citation/evidence spans remain preserved but do not promote citation-only records above `metadata_only`. A `full_text` claim requires an explicitly reusable license, successful bounded retrieval, successful text extraction or strict full-article HTML checks, a matching hash, and exact preserved text.

## Retrieval and rights

- Explicitly reusable-license full-text candidates attempted: **18**
- Verified full text retrieved: **13**
  - Direct PDF plus text extraction: **7**
  - Jina publisher-page fallback passing title, length, introduction, and references checks: **6**
- Failed explicitly licensed retrievals: **5**
- Remaining non-full-text records: **187**
  - No direct open PDF URL in audited metadata: **156**
  - Public PDF URL without an explicit reusable license: **26**
  - Explicitly licensed retrieval/extraction remained blocked: **5**

The exact HTTP, redirect, DNS, and document-structure failures are preserved in `research/academic/full-text-attempt-ledger.csv`; all non-full-text dispositions are preserved in `research/academic/blocker-ledger.csv`. No unavailable text is fabricated or claimed.

## Determinism and evidence

- `scripts/academic_recovery.py` snapshots the original 200 files with SHA-256 hashes, fetches OpenAlex metadata in four bounded logged batches, classifies source type, reconstructs abstracts, deduplicates by DOI/OpenAlex ID/canonical URL/normalized title, applies explicit relevance rules, writes records/ledgers, and validates the lane.
- Rerunning migration from the preserved snapshot/cache produced the identical SHA-256 tree digest twice: `67f79a487d0f9ae3b90db6c43a50cc4aa11fe89959b62076d2646e8951052f9b` across 205 generated records/CSV ledgers.
- `research/academic/audit-ledger.csv` has exactly one disposition for every legacy path and OpenAlex ID.
- `research/academic/query-ledger.jsonl` preserves all four successful OpenAlex audit batches and all 200 requested IDs.
- `research/academic/rejection-ledger.csv`, `retrieval-ledger.csv`, `full-text-attempt-ledger.csv`, and `blocker-ledger.csv` preserve academic-specific decisions and failures.

## Manual sampling

Early, middle, and late sorted records were inspected, as was at least one record from every populated source type and both accepted/rejected states. This caught and corrected classification precedence for repository preprints, a handbook-chapter edge case, abstract inflation from legacy citation spans, and false rejection of theory/review papers centered on absorptive capacity.

## Commits

- `43ee3c7` — deterministic academic recovery pipeline and unit tests
- `d0946df` — migrated corpus, legal full-text evidence, all academic ledgers, strengthened validator, and checkpoint

## Blockers outside this lane

- The repository-wide schema/statistics/README and `tools/corpus.py` do not yet understand the academic-specific directory/fields. Those files are manager-owned and intentionally untouched. The academic validator independently proves this lane until manager integration.
- Five explicitly licensed full-text candidates remain technically blocked; exact retryable evidence is in the full-text attempt ledger. Their abstract/metadata artifacts remain honest and accepted/rejected independently of full-text availability.
- `agent-reach` CLI was unavailable (`command not found`); the documented public API and Jina reader fallbacks were used and logged instead.
