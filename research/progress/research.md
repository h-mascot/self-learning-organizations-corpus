# Research Lane Progress

Date: 2026-07-11  
Status: checkpoint committed after complete bounded research run

## Delivered

- Built a repeatable 200-query recursive research runner over 20 required taxonomy topics × 10 evidence facets.
- Executed 200 productive loops. Each returned at least one stable Crossref DOI/URL; 600 raw discovery records are preserved across 200 individual JSON artifacts and `research/loops/ledger.csv`.
- Built categorized source coverage for arXiv/academic, X, Reddit, Substack, blogs, podcasts, conferences, books, case studies, Pedro/Brex, Ramp, and actual implementations.
- Built a 12-company implementation index that separates operational evidence, first-party claims, secondary reports, and marketing/vision.
- Completed an actual OpenAI/GPT-5.4 deep web-research run through Codex native search. Full report, execution log, citations, preflight, and provider manifest are preserved.
- Attempted Perplexity sonar-deep-research after CLI/MCP/credential discovery. The endpoint returned HTTP 401; exact headers/body and recovery path are preserved.
- Ran authenticated GitHub benchmark queries and preserved raw JSON. No larger directly comparable repository was found, but evidence is insufficient for an unqualified “world’s largest” claim.
- Added validation for loop artifacts and required research deliverables.

## Platform counts

| Platform/lane | Count | Meaning |
|---|---:|---|
| Crossref academic discovery | 600 | Three DOI/URL records per productive loop; not automatically relevance-validated |
| Productive recursive loops | 200 | Unique taxonomy × evidence-facet queries with raw evidence |
| OpenAI deep-research reports | 1 | Complete GPT-5.4 native-web-search report |
| Perplexity reports | 0 | Blocked with exact HTTP 401 proof |
| arXiv/academic named foundations | 2+ | Named validated anchors plus 600 Crossref candidates |
| X live records | 0 | Authentication blocker; snippets excluded |
| Reddit live records | 0 | Authentication/no-result blocker; snippets excluded |
| Substack discovery records | 2 | Author-level discovery; item validation remains |
| Blogs | 8 | Mixed primary/independent sources |
| Podcasts | 10 | Discovery records; publisher claims need transcript validation |
| Conferences | 6 | Primary event/paper venues |
| Books | 9 | Bibliographic indexing only |
| Case studies | 9 | Company-reported outcomes labeled |
| Pedro/Brex | 7 | Primary/product/interview records |
| Ramp | 6 | Product, engineering, and customer records |
| Actual company implementations | 12 | Indexed with evidence posture |

## Honest limitations and next loops

- The 600 Crossref results are discovery candidates, not 600 validated relevant sources. A downstream relevance/dedupe/full-text-rights stage must review them before corpus inclusion.
- X and Reddit require authenticated browser/cookie state. They remain zero rather than being padded from search snippets.
- Perplexity requires a valid provider credential.
- The GitHub benchmark supports only “no larger directly comparable corpus found in the documented query set,” not a global superlative.
- This research lane does not complete the separate 100+ YouTube transcript, title-filename migration, CI, push, or live-GitHub gates owned by the overall goal manager.

## Validation

Run: `python3 scripts/validate_research.py`

Expected core result: 200 ledger rows, 200 productive loops, zero missing artifacts.
