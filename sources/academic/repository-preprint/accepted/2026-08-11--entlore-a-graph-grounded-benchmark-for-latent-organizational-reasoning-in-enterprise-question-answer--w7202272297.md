---
academic_schema_version: 1
stable_id: "openalex:W7202272297"
openalex_id: "W7202272297"
doi: "10.48550/arxiv.2608.10679"
arxiv_id: "2608.10679"
title: "ENTLORE: A Graph-Grounded Benchmark for Latent Organizational Reasoning in Enterprise Question Answering"
authors: ["Akrin Zheng", "Alexander Wu", "Alaia Liu"]
publisher: "arXiv"
published_date: "2026-08-11"
canonical_url: "https://arxiv.org/abs/2608.10679"
source_type: "repository-preprint"
lifecycle: "accepted"
relevance_status: "relevant"
relevance_reason: "Refresh-window primary academic source on organization-memory, enterprise QA, decision systems, benchmark."
relevance_terms: ["organization-memory", "enterprise QA", "decision systems", "benchmark"]
artifact_level: "abstract"
rights_status: "third-party-metadata-and-abstract"
rights_holder: "Akrin Zheng, Alexander Wu, Alaia Liu"
retrieved_at: "2026-10-09T11:18:05+00:00"
provenance: "OpenAlex W7202272297 API metadata/abstract plus arXiv publication-date receipt at research/refresh-20261009/evidence/source-receipts/academic-W7202272297.json."
open_full_text_url: "https://arxiv.org/pdf/2608.10679"
duplicate_of: null
rejection_reason: null
legacy_path: null
legacy_sha256: null
content_sha256: "d6f86ac367658c01c67c92f8e2bbddfa23de1c8a96c785d2575bfac32b8a6a75"
---
# ENTLORE: A Graph-Grounded Benchmark for Latent Organizational Reasoning in Enterprise Question Answering

## Relevance decision

This refresh-window preprint is relevant because it provides primary academic evidence about organization-memory, enterprise QA, decision systems, benchmark for long-horizon organizational or agent memory systems. It is theory/tooling evidence rather than an organization case study.

## Preserved OpenAlex abstract

Enterprise question answering is framed as retrieving internal documents and generating grounded answers. Routine enterprise records, however, are work by-products in which required organizational relations remain implicit across heterogeneous sources. Existing benchmarks provide realistic multi-source evidence, but often materialize a predefined answer path and therefore test the composition of stated facts rather than recovery of a target relation absent from the corpus. We call the latter capability latent organizational reasoning. We introduce ENTLORE, a graph-grounded benchmark construction framework that reconstructs an audited enterprise world from routine documents, authoritative organizational tables, and operational records. Versioned organizational conventions certify derived relations in a truth graph, enabling complete golden answers and proof certificates. The aligned anonymized release exposes only the document corpus while withholding private structure and target relations. ENTLORE contains 2,341 documents from three source types and 907 questions spanning explicit lookup, cross-source composition, and latent organizational reasoning, evaluated across 56 model and access configurations. Structuring the released world as an induced entity graph or navigable knowledge base gives the strongest deployable results. Yet supplying gold documents still leaves 30.4% of latent questions unanswered, versus 12.6% and 6.2% for explicit and compositional questions. Enterprise QA therefore depends not only on document recall, but also on whether implicit organizational relations become usable. The benchmark, data, and code are publicly available at https://github.com/scitix/entlore .

## Publication-date receipt

OpenAlex reports publication_date `2026-08-11` for `W7202272297` and DOI `https://doi.org/10.48550/arxiv.2608.10679`. arXiv reports `2608.10679v2` with v1 published timestamp `2026-08-11T09:00:43Z` and page marker `11 Aug 2026 (`. These agree at day precision. Compact receipt: `research/refresh-20261009/evidence/source-receipts/academic-W7202272297.json`.

## Artifact and rights honesty

Artifact level: `abstract`. The corpus retains OpenAlex/arXiv metadata and the exact OpenAlex abstract only. It does not claim that the full arXiv paper text is stored in the corpus.
