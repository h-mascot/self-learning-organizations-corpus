# Task Plan: Web and media acquisition lane

## Goal

Meet or exceed the accepted substantive quotas for blogs, podcasts, books, conferences, case studies, and GitHub with deduplicated, provenance-first records, honest artifact levels, preserved blocked/rejected evidence, lane validation, tests, and coherent commits.

## Phases

- [x] Phase 1: Read the goal, skill instructions, branch state, and existing lane artifacts.
- [x] Phase 2: Define the lane record/ledger format and deterministic validator without changing manager-owned schema or tooling.
- [x] Phase 3: Recover and classify existing discovery leads and five early source files.
- [x] Phase 4: Search multiple query families across public web/RSS/podcast/company/GitHub sources and citation chains.
- [x] Phase 5: Retrieve legal evidence, deduplicate, classify artifact/rights/lifecycle honestly, and preserve failures.
- [x] Phase 6: Validate quotas, metadata, hashes, paths, duplicates, evidence, and ledgers; manually sample every channel.
- [x] Phase 7: Run repository checks, commit coherent batches, re-read GOAL.md, and report exact counts, tests, commits, and blockers.

## Key Questions

1. Which canonical record shape can remain lane-local while the manager updates the shared schema?
2. Which public primary sources expose enough evidence for substantive acceptance without copying protected full text?
3. Which podcast episodes have publisher transcripts or sufficiently detailed timestamped public notes?
4. Can each quota be met without mirrors or duplicate index/detail records inflating counts?

## Decisions Made

- Keep all planning, acquisition, and validation artifacts lane-specific; do not edit manager-owned files listed in the task.
- Treat metadata-only records as substantive only for the books quota, as explicitly permitted by GOAL.md; all other accepted lane records require bounded evidence, transcript, timestamped notes, abstract, or legal full text.
- Prefer primary publisher/company/repository sources and use search results only as discovery provenance.

## Errors Encountered

- The shared schema at baseline lacks artifact levels, expanded lifecycle states, and a GitHub platform. Resolution: leave it untouched and validate the lane contract independently pending manager integration.
- The first Exa batch returned a response truncated inside a UTF-8 code point, raising `UnicodeDecodeError` before any artifacts were written. Resolution: decode subprocess output with explicit UTF-8 replacement and retain bounded clean text only.
- Exa's JSON presentation wrapper truncated long results into invalid JSON and Google Books returned HTTP 429 with a configured daily quota of zero. Resolution: use Exa's documented text presentation and fall back to the public Open Library Search API while preserving all Google Books blockers.
- Exa and the Jina public reader later exhausted free HTTP 429 limits. Resolution: preserve every blocked query/retrieval and use deterministic, previously audited primary-URL citation catalogs with direct-origin fallback.
- A canonicalization pass initially stripped meaningful YouTube `v=` parameters and collapsed podcast episodes. Resolution: retain identity query parameters and strip tracking parameters only; add a regression test.
- Manual samples found one stale Red Hat 404 and several podcast spans that did not retain the matched timestamped passage. Resolution: reject missing-page titles, select transcript spans anchored to real timestamps, and add validator gates.

## Status

**Complete** — lane gates pass; final verification and handoff are recorded.
