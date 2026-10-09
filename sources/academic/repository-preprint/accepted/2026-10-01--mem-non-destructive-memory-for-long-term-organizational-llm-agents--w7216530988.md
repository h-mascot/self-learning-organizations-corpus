---
academic_schema_version: 1
stable_id: "openalex:W7216530988"
openalex_id: "W7216530988"
doi: "10.48550/arxiv.2610.02002"
arxiv_id: "2610.02002"
title: "Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents"
authors: ["Ahmad Yehia", "Aly O. Abdelkareem", "Islam Ahmed", "Hesham Omran", "Khaled Alashmouny", "Christian Claudel", "Abduallah Mohamed"]
publisher: "arXiv"
published_date: "2026-10-01"
canonical_url: "https://arxiv.org/abs/2610.02002"
source_type: "repository-preprint"
lifecycle: "accepted"
relevance_status: "relevant"
relevance_reason: "Refresh-window primary academic source on organization-memory, supersession, evals, benchmark."
relevance_terms: ["organization-memory", "supersession", "evals", "benchmark"]
artifact_level: "abstract"
rights_status: "third-party-metadata-and-abstract"
rights_holder: "Ahmad Yehia, Aly O. Abdelkareem, Islam Ahmed, Hesham Omran, Khaled Alashmouny, Christian Claudel, Abduallah Mohamed"
retrieved_at: "2026-10-09T11:18:05+00:00"
provenance: "OpenAlex W7216530988 API metadata/abstract plus arXiv publication-date receipt at research/refresh-20261009/evidence/source-receipts/academic-W7216530988.json."
open_full_text_url: "https://arxiv.org/pdf/2610.02002"
duplicate_of: null
rejection_reason: null
legacy_path: null
legacy_sha256: null
content_sha256: "ff4cd30aa11fbf8bf307ee027fceb0cf86abd114a16ffd9e6e0c5d141f8dc9c9"
---
# Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents

## Relevance decision

This refresh-window preprint is relevant because it provides primary academic evidence about organization-memory, supersession, evals, benchmark for long-horizon organizational or agent memory systems. It is theory/tooling evidence rather than an organization case study.

## Preserved OpenAlex abstract

Large Language Model (LLM) agents now take part in organizational work, where many authors record decisions across documents over months. Because a revised decision arrives as a new document rather than an edit, answering a question requires knowing which version held at a given time. However, most memory systems compress the record at write time. By distilling each document into facts, notes or graph edges, these methods fix what can be answered before any question is asked. To address this, we propose Mem++, a non-destructive memory framework shifting from write-time distillation to read-time selection. Mem++ stores every document whole with its date and author, and it calls no generative model at write time. At read time, it retrieves only documents dated up to the time a question asks about and fuses lexical and semantic rankings. Unlike systems that overwrite older versions, Mem++ keeps them and leaves the choice to the answering model. Evaluations on the organizational benchmark OrgMemBench demonstrate that Mem++ surpasses the strongest memory system baseline by 8.0 to 13.1 points across two answering models. With gpt-4.1-mini, it also achieves the best overall score, 2.6 points above RAG. In addition, Mem++ achieves the best average LLM-judge score on LoCoMo and ranks second on LongMemEval-S, behind only its entity-graph variant. Code for benchmark evaluation is available at https://github.com/AIDAChip-Inc/mem-plus-plus.

## Publication-date receipt

OpenAlex reports publication_date `2026-10-01` for `W7216530988` and DOI `https://doi.org/10.48550/arxiv.2610.02002`. arXiv reports `2610.02002v1` with v1 published timestamp `2026-10-01T16:32:38Z` and page marker `1 Oct 2026]`. These agree at day precision. Compact receipt: `research/refresh-20261009/evidence/source-receipts/academic-W7216530988.json`.

## Artifact and rights honesty

Artifact level: `abstract`. The corpus retains OpenAlex/arXiv metadata and the exact OpenAlex abstract only. It does not claim that the full arXiv paper text is stored in the corpus.
