---
academic_schema_version: 1
stable_id: "openalex:W7214043592"
openalex_id: "W7214043592"
doi: "10.48550/arxiv.2609.24971"
arxiv_id: "2609.24971"
title: "DolphinBench: Mapping the Pareto Frontier of Agent Memory"
authors: ["Soumil Rathi", "Deshraj Yadav", "Taranjeet Singh"]
publisher: "arXiv"
published_date: "2026-09-21"
canonical_url: "https://arxiv.org/abs/2609.24971"
source_type: "repository-preprint"
lifecycle: "accepted"
relevance_status: "relevant"
relevance_reason: "Refresh-window primary academic source on agent-memory, evals, task-completion, benchmark."
relevance_terms: ["agent-memory", "evals", "task-completion", "benchmark"]
artifact_level: "abstract"
rights_status: "third-party-metadata-and-abstract"
rights_holder: "Soumil Rathi, Deshraj Yadav, Taranjeet Singh"
retrieved_at: "2026-10-09T11:18:05+00:00"
provenance: "OpenAlex W7214043592 API metadata/abstract plus arXiv publication-date receipt at research/refresh-20261009/evidence/source-receipts/academic-W7214043592.json."
open_full_text_url: "https://arxiv.org/pdf/2609.24971"
duplicate_of: null
rejection_reason: null
legacy_path: null
legacy_sha256: null
content_sha256: "1b0ce6230503d95d5dbeed3f53a3d7308638ed4956c1e6b50ad44717fa46aba6"
---
# DolphinBench: Mapping the Pareto Frontier of Agent Memory

## Relevance decision

This refresh-window preprint is relevant because it provides primary academic evidence about agent-memory, evals, task-completion, benchmark for long-horizon organizational or agent memory systems. It is theory/tooling evidence rather than an organization case study.

## Preserved OpenAlex abstract

Agents today often take real-world actions that depend on long-term memory and context recall over time. However, most current memory benchmarks are built for a conversational question-answer format, where the question itself signals that some fact must be retrieved, and often which one. Moreover, benchmarks rarely require anything beyond accuracy from submissions, allowing memory systems to make unreasonable cost/time tradeoffs to achieve higher scores. We present DolphinBench, a benchmark that evaluates memory directly through an agent's task completion. DolphinBench includes three knowledge-work personas with roughly 500k tokens of user messages per persona and evaluates agents on tasks that depend on information from that history. We verify all 200 tasks per persona by running an agent with and without the relevant history, requiring success with it and failure without it. Finally, we require all evaluations to report total cost and latency alongside accuracy, which enables us to evaluate agent memory systems holistically. No existing memory benchmark combines all three. The dataset and evaluation code are available at https://dolphinbench.ai.

## Publication-date receipt

OpenAlex reports publication_date `2026-09-21` for `W7214043592` and DOI `https://doi.org/10.48550/arxiv.2609.24971`. arXiv reports `2609.24971v2` with v1 published timestamp `2026-09-21T17:54:35Z` and page marker `21 Sep 2026 (`. These agree at day precision. Compact receipt: `research/refresh-20261009/evidence/source-receipts/academic-W7214043592.json`.

## Artifact and rights honesty

Artifact level: `abstract`. The corpus retains OpenAlex/arXiv metadata and the exact OpenAlex abstract only. It does not claim that the full arXiv paper text is stored in the corpus.
