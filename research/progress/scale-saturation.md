# Scale and Saturation Checkpoint

## 2026-07-12 cross-channel round set

The canonical accepted corpus was preserved unchanged. Thirty-three live discovery
rounds (three per channel) used three distinct families: bounded doctrine,
mechanism language, and citation/named-entity chasing. GitHub used its authenticated
CLI/API; the remaining lanes used Bing's public RSS search because `agent-reach`
is absent from `PATH` and Exa's earlier ledgered attempts hit its free-tier 429.

Search results are not evidence. Exact known URLs and obvious channel/query drift
were rejected; plausible new URLs remain blocked until a human-grade primary-source
review establishes relevance, provenance, rights, and—where claimed—an implemented
organization mechanism.

| Channel | Results | Accepted | Rejected | Blocked | Round net-new accepted rates | Saturated? |
|---|---:|---:|---:|---:|---|---|
| academic | 27 | 0 | 20 | 7 | 0.0%, 0.0%, 0.0% | No |
| blogs | 24 | 0 | 15 | 9 | 0.0%, 0.0%, 0.0% | No |
| books | 30 | 0 | 30 | 0 | 0.0%, 0.0%, 0.0% | No |
| case-studies | 30 | 0 | 26 | 4 | 0.0%, 0.0%, 0.0% | No |
| conferences | 30 | 0 | 28 | 2 | 0.0%, 0.0%, 0.0% | No |
| github | 0 | 0 | 0 | 0 | 0.0%, 0.0%, 0.0% | No |
| podcasts | 30 | 0 | 28 | 2 | 0.0%, 0.0%, 0.0% | No |
| reddit | 30 | 0 | 30 | 0 | 0.0%, 0.0%, 0.0% | No |
| substack | 30 | 0 | 30 | 0 | 0.0%, 0.0%, 0.0% | No |
| x | 30 | 0 | 30 | 0 | 0.0%, 0.0%, 0.0% | No |
| youtube | 30 | 0 | 30 | 0 | 0.0%, 0.0%, 0.0% | No |

The numerical rates are recorded but **not eligible saturation rounds**. Twenty-four
discoveries remain blocked, and the search backend showed substantial query drift.
Zero automatic acceptance cannot prove diminishing returns. GitHub returned zero
results for the intentionally organization-specific compound searches; that is a
completed negative search, not saturation evidence.

## Integrity boundary

- The 222 accepted GitHub records are tooling/reference artifacts. They may support
  mechanism discovery, implementation recipes, or recursive citation chasing.
- A generic eval, memory, observability, or agent repository does not establish that
  its owner—or any user organization—is a self-learning organization.
- Only primary or independently corroborated implementation evidence belongs in the
  company index. Vendor/customer outcome claims retain their attribution.

## Artifacts and next gate

- `research/saturation/rounds.jsonl`: round backend, query, counts, rates, errors,
  and eligibility decision.
- `research/saturation/candidates.jsonl`: deduplicated result-level disposition.
- `research/saturation/summary.json`: aggregate checkpoint.
- `scripts/run_saturation_search.py`: repeatable, non-mutating collector.
- `scripts/validate_saturation.py`: count, round-family, and eligibility checks.

Next, review the 24 blocked discoveries against publisher pages and then rerun three
rounds on a higher-precision backend. A channel can be marked saturated only after
three consecutive eligible rounds remain under 5% net-new accepted unique sources.
