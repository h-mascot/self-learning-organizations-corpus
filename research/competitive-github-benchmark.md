# Competitive GitHub Corpus Benchmark

> Superseded for cross-web comparison by the deterministic [public competitor benchmark](benchmark/public-competitor-benchmark.json). This file remains the GitHub discovery log, not the basis for a largest claim.

## Method

Authenticated GitHub repository search was run on 2026-07-11 with exact and adjacent query families: `learning organization corpus`, `self-learning organizations`, `AI-native company corpus`, `organizational learning dataset`, `recursive improvement organization`, and `autonomous enterprise corpus`. Evidence is preserved in `research/benchmark/github-search.json`.

The exact query `learning organization corpus` returned only this repository. Adjacent queries surface organizational-learning software, academic reading lists, generic AI-agent repositories, and datasets, but no clearly equivalent provenance-first cross-platform corpus was established during this run.

A corrective rerun added `self learning organization corpus`, `organizational learning dataset`, and `AI native company research`; raw results are in `research/benchmark/github-search-corrective.json`. It returned three repositories total: this corpus, `jeremy9682/ai-native-company-research`, and `Elainewangyuyan/yy-gtm-lens`. Manual description review found the latter two to be respectively public research notes and a report-generating skill, not a larger provenance-first cross-platform source corpus.

## Claim boundary

The evidence supports only this wording: **“No larger directly comparable public GitHub corpus was found in the documented search set on 2026-07-11.”** It does not prove a world-largest claim: GitHub search is index- and query-limited; private, non-GitHub, differently named, and non-English corpora may exist. Current corpus size is also too small for an unqualified superlative.

## Competitive dimensions

| Dimension | This corpus | Common adjacent repositories |
|---|---|---|
| Unit of collection | Organizations, implementations, claims, transcripts | Papers, code, prompts, or generic agent examples |
| Provenance/right status | Explicit design requirement | Often absent or repository-license only |
| Cross-platform taxonomy | Required | Usually one medium or topic |
| Recursive loop evidence | 200 dependent artifacts, 197 DAG edges, ledger, relevance gate | Not exposed in the two closest current results |
| Outcome claim labeling | Verified vs company/marketing claim | Inconsistent |

The appropriate next benchmark is a manually reviewed top-50 result set per query family with false-positive labels and repository content counts—not star counts alone.
