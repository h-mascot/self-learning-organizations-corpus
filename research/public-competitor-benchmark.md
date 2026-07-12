# Public Competitor Benchmark

Measured 2026-07-12. The machine-readable source of truth is [`benchmark/public-competitor-benchmark.json`](benchmark/public-competitor-benchmark.json); its validator is part of `make check`.

## Result

Two public collections in the documented search set are genuinely comparable on a strict organization-evidence basis: the completely audited IHI report contains 10 qualifying organizations and the completely audited Lean Enterprise Institute page contains 2. The benchmark still **does not permit a largest claim** because the broader public universe and large adjacent collections have not been audited exhaustively.

The strict unit is a unique named organization with public evidence of an operating feedback, evaluation, memory, experimentation, decision, failure-learning, specialized-agent, workflow-adaptation, knowledge-curation, or governance loop. AI deployments, tools, theoretical material, and vendor stories without such an organization-level loop are excluded.

| Collection | Public raw count | Strict count proven | Why the raw count is not like-for-like |
|---|---:|---:|---|
| [Evidently ML/LLM system design](https://www.evidentlyai.com/ml-system-design) | 805 use cases | Unknown | Application and system-design use cases; no row-level organization-loop audit in the retrieved index |
| [Enterprise AI Case Studies](https://case-studies.ai/) | 67 published cases | Unknown | AI deployment/use-case records, including reference architectures and technical optimization |
| [AI Trace](https://www.aitrace.org/) | 278 companies / 1,602 practices | 0 in 6-company freshness sample | Named-company AI-use evidence, but the sample did not establish organization-level improvement loops |
| [World Bank AI Repository](https://airepository.worldbank.org/cases) | 111 use cases | 0 in first-5 deterministic sample | Development AI implementations and tools rather than organization-learning records |
| [Case Ledger](https://caseledger.ai/) | 4,217 claimed verified cases | Unknown | Homepage counter was not publicly enumerable; unit is an AI workflow/use case |
| [CaseStudies.com](https://www.casestudies.com/companies) | 928,650+ claimed stories | Unknown | Generic B2B vendor/customer stories across non-AI and AI topics |
| [Talented Learning directory](https://talentedlearning.com/ads/basic-member-case-study-directory/) | 100+ cases | Unknown | LMS adoption/customer-success evidence, not organizational self-improvement evidence |
| [Lean Enterprise Institute](https://www.lean.org/training-consulting-for-organizations/case-studies/) | 8 case-study cards | 2 unique named organizations (complete audit) | Genuinely comparable but smaller: five conservative exclusions and one duplicate were audited explicitly |
| [IHI: 100 Million Healthier Lives](https://www.ihi.org/library/publications/100-million-healthier-lives-case-studies-around-globe) | 10 organization cases | 10 unique named organizations (complete audit) | Genuinely comparable: all ten cases document a measurement, testing, feedback, learning, adaptation, or scaling loop |
| [ai-native-company-research](https://github.com/jeremy9682/ai-native-company-research) | 19 content files | Unknown | Closest topical neighbor, but files are patterns, analyses, blueprints, and source notes rather than normalized organization cases |

Here, `Unknown` means no row audit supports a numeric strict result. Zero is used only for an audited sample or complete audit in which no qualifying unit was found; it does not mean the unaudited remainder can never contain a qualifying example. This prevents inaccessible records and topical adjacency from being silently converted to zero or used to inflate the benchmark.

## Measurement and limitations

Counts are publisher-stated exact counts, explicit publisher floors, enumerable directory counts, or deterministic GitHub-tree counts as labeled in the JSON artifact. Retrieval evidence records the stable public page/API method, observed scope/schema, retrieval and update dates (or explicit unknown), exclusions, and count method for every row.

Audit coverage is explicit rather than implied. `complete` means every raw unit has a decision; `sample` records a reproducible selection rule and every sampled row URL; `scope_only` requires a `null` strict count because its like-for-like result is unknown. The validator recomputes strict counts from unique included organizations, checks that complete audits cover the raw count, and rejects malformed audit decisions, count relations, and numeric scope-only results.

Discovery used public web search, public page/PDF rendering, and the GitHub API. The preferred Agent Reach health check was unavailable because its executable is not installed. Search indexes are query-limited; private, paywalled, non-English, and differently named collections may remain undiscovered. The IHI collection is dated to its stated publication year (2020), represented as `2020-12-31` with `year` precision rather than a fabricated day. A future largest claim requires both broader discovery and row-level strict audits of plausible competitors.
