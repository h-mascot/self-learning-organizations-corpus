# Categorized Source Index

This index is a research map, not a redistribution claim. Third-party text remains with its rights holder. “Primary” means authored by the company, researcher, publisher, or event responsible; it does not make a performance claim independently verified. Raw Exa discovery output is preserved in `research/raw/exa/`; the Crossref matrix remains discovery evidence in `research/loops/artifacts/`; qualifying dependent-loop evidence is in `research/recursive-loops/artifacts/`.

| Platform | Validated/indexed | Representative sources | Evidence posture |
|---|---:|---|---|
| arXiv / academic | 600 Crossref discoveries + 200 relevance-gated recursive records | [March, exploration/exploitation](https://doi.org/10.1287/orsc.2.1.71); [Cohen & Levinthal, absorptive capacity](https://doi.org/10.2307/2393553); dependent OpenAlex DAG | The 200 canonical records include preserved abstract/title spans and pass a topical gate; metadata still does not imply peer-review or full-text rights |
| X | 0 live records | Search attempted with `twitter-cli` | Blocked: no authenticated cookies; do not count web snippets as verified posts |
| Reddit | 0 live records | OpenCLI route attempted | No authenticated result; do not count search-engine snippets as verified threads |
| Substack | 2 discovery records | [One Useful Thing](https://www.oneusefulthing.org/); [Import AI](https://importai.substack.com/) | Author commentary; verify individual claims against primary evidence |
| Blogs | 11 | [Pedro/YC transcript](https://www.ycombinator.com/library/RB-the-ceo-must-be-the-chief-ai-officer); [Ramp Intelligence](https://ramp.com/intelligence); [GitHub Copilot context](https://github.blog/ai-and-ml/github-copilot/how-github-copilot-is-getting-better-at-understanding-your-code/) | Mixed primary and independent commentary; Brex stale-link contradiction preserved |
| Podcasts | 10 discovery records | [SAP Autonomous Enterprise](https://news.sap.com/2026/06/introducing-autonomous-enterprise-podcast-series/); [AI Native Dev](https://ainativedev.io/podcast) | Publisher descriptions are marketing until transcript/outcome validation |
| Conferences | 6 | [NeurIPS](https://neurips.cc/); [ICLR](https://iclr.cc/); [ACM FAccT](https://facctconference.org/); [Lean Enterprise Institute events](https://www.lean.org/events-training/) | Event/paper primary records; relevance requires per-item review |
| Books | 9 | *The Fifth Discipline*; *The Knowledge-Creating Company*; *The Toyota Way*; *High Output Management*; *The Fearless Organization*; *The Knowing-Doing Gap*; *Reinventing Organizations*; *Team of Teams*; *Thinking in Systems* | Bibliographic/summary indexing only; no full-book redistribution |
| Case studies | 11 | [Ramp engineering index](https://engineering.ramp.com/); [Ramp customer stories](https://ramp.com/customers); [Klarna AI assistant](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) | Company-reported metrics labeled as such unless independently reproduced |
| Pedro / Brex | 8 records including contradiction | [Pedro/YC transcript](https://www.ycombinator.com/library/RB-the-ceo-must-be-the-chief-ai-officer); YC videos; stale Brex AI URL audit | Pedro/YC claims are first-person evidence; current Brex `/product/ai` 404 is not counted as substantive product evidence |
| Ramp | 9 | [Ramp Intelligence](https://ramp.com/intelligence); [Ramp engineering](https://engineering.ramp.com/); [Ramp customer stories](https://ramp.com/customers) | Directly inspected first-party spans added; product/customer metrics remain vendor claims pending audit |
| Actual company implementations | 12 companies | YC, Brex, Ramp, Klarna, GitHub, Duolingo, Spotify, Toyota, Morning Star, Every, WorkOS, SAP | See `research/company-index.md`; implementation status and claim class separated |

## Inclusion rules

1. A URL is a discovery record until title, publisher, date, topical relevance, rights status, and stable ID are checked.
2. “Implemented” requires a primary description of an operating workflow, not a generic product announcement.
3. “Verified outcome” is reserved for independently reproducible/audited evidence. Company-reported numbers remain `marketing/company claim` even when accurately quoted.
4. Social results are not counted when authentication prevents opening the original post/thread.

The earlier hand-curated cross-platform inventory remains at `research/discovery-inventory.md`; it contains 45 rows and detailed transcript/right-status notes. Counts above deliberately avoid treating inaccessible X/Reddit snippets or failed Exa queries as sources.
