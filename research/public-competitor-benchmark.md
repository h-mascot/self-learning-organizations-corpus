# Public Competitor Benchmark

Measured 2026-07-12. The machine-readable source of truth is [`benchmark/public-competitor-benchmark.json`](benchmark/public-competitor-benchmark.json); its validator is part of `make check`.

## Result

No public collection in the documented search set is presently proven comparable on a strict organization-evidence basis. The benchmark therefore **does not permit a largest claim**.

The strict unit is a unique named organization with public evidence of an operating feedback, evaluation, memory, experimentation, decision, failure-learning, specialized-agent, workflow-adaptation, knowledge-curation, or governance loop. AI deployments, tools, theoretical material, and vendor stories without such an organization-level loop are excluded.

| Collection | Public raw count | Strict count proven | Why the raw count is not like-for-like |
|---|---:|---:|---|
| [Evidently ML/LLM system design](https://www.evidentlyai.com/ml-system-design) | 800 case studies | 0 | Application and system-design use cases; no row-level organization-loop audit in the retrieved index |
| [Enterprise AI Case Studies](https://case-studies.ai/) | 67 published cases | 0 | AI deployment/use-case records, including reference architectures and technical optimization |
| [Case Ledger](https://caseledger.ai/) | 4,217 claimed verified cases | 0 | Homepage counter was not publicly enumerable; unit is an AI workflow/use case |
| [CaseStudies.com](https://www.casestudies.com/companies) | 928,650+ claimed stories | 0 | Generic B2B vendor/customer stories across non-AI and AI topics |
| [Talented Learning directory](https://talentedlearning.com/ads/basic-member-case-study-directory/) | 100+ cases | 0 | LMS adoption/customer-success evidence, not organizational self-improvement evidence |
| [ai-native-company-research](https://github.com/jeremy9682/ai-native-company-research) | 19 content files | 0 | Closest topical neighbor, but files are patterns, analyses, blueprints, and source notes rather than normalized organization cases |

Here, zero means “no qualifying unit proven by the stated measurement,” not “the collection can never contain a qualifying example.” This conservative rule prevents inaccessible records and topical adjacency from inflating the benchmark.

## Measurement and limitations

Counts are publisher-stated exact counts, explicit lower bounds, or deterministic GitHub-tree counts as labeled in the JSON artifact. Retrieval evidence records the public page/API method, observed scope/schema, update date (or explicit unknown), exclusions, and count method for every row.

Discovery used public web search, public page rendering, and the GitHub API. The preferred Agent Reach health check was unavailable because its executable is not installed. Search indexes are query-limited; private, paywalled, non-English, and differently named collections may remain undiscovered. A future largest claim requires both broader discovery and row-level strict audits of plausible competitors.
