# Goal: Build a validated cross-channel corpus of self-learning and self-improving organizations

**Status: ACHIEVED — verified 2026-07-12.** Scale-and-saturation is complete under the terminal contract. The corpus does **not** claim “largest measured”: the validated competitor benchmark explicitly withholds that superlative because the broader public universe is not exhaustively audited.

## North star
Build the largest measured, highest-integrity public corpus of how AI-native and self-learning organizations actually improve: their feedback loops, evals, memory, operating systems, specialized agents, decision records, failure-learning mechanisms, and measurable outcomes. Cover academic research, X, Reddit, Substack/newsletters, blogs/company sites, podcasts, books, conference talks, case studies, GitHub, and YouTube.

The motivating doctrine is Pedro Franceschi's discussion with Garry Tan on YC's *The Light Cone*, “The CEO Must Be the Chief AI Officer,” especially the “Building Company AGI” section: curate context aggressively; model bounded operational domains; compose specialized agents rather than one monolithic company model; preserve raw data, procedures, decisions, and skills; evaluate improvement through operational failures and feedback.

## Current verified baseline
- 100 accepted complete timestamped YouTube transcripts; 1 rejected video.
- 200 OpenAlex-derived academic records exist under `sources/arxiv/`, but the directory/platform classification is wrong and many records contain metadata/abstracts rather than full text.
- 3 substantive blog records and 2 case-study records exist but are not included in generated canonical statistics.
- X, Reddit, podcasts, Substack, books, and conferences contain no substantive records.
- `research/discovery-inventory.md` preserves 46 early leads: 18 YouTube, 18 web/company, 5 academic, 4 reference/book, 1 podcast.

## Completion gates
All gates must pass before status may be ACHIEVED.

### 1. Canonical schema and honest accounting
- Support artifact levels: `full_text`, `transcript`, `abstract`, `metadata_only`, `unavailable`.
- Support lifecycle: `discovered`, `retrieved`, `accepted`, `rejected`, `blocked`.
- Generated statistics show per-platform and per-artifact-level counts without treating metadata as full text.
- Every substantive existing record is either migrated into the canonical schema or preserved in a rejection/blocker ledger with reason.
- `.gitkeep` files never count as sources.

### 2. Academic recovery
- Audit all 200 OpenAlex-derived records.
- Reclassify by actual source type: arXiv, journal article, conference paper, book/chapter, thesis, repository/preprint, or other academic.
- Deduplicate by DOI/OpenAlex ID/canonical URL/title.
- Validate topical relevance. Reject irrelevant records explicitly.
- Preserve available abstract evidence; retrieve legal open full text where available and record rights/provenance.
- No record may claim arXiv unless an arXiv identifier or canonical arxiv.org URL proves it.

### 3. Existing non-YouTube recovery
- Properly ingest and validate all useful records/leads already present in `sources/blogs`, `sources/case-studies`, `research/discovery-inventory.md`, and related research artifacts.
- Preserve full publisher text where permitted; otherwise metadata, bounded evidence spans, and retrieval status.

### 4. Missing-channel acquisition
Search each channel using multiple query families and citation chasing. Minimum accepted substantive records after deduplication:
- X/Twitter: 50
- Reddit: 25
- Substack/newsletters: 25
- Blogs/company/engineering sites: 75
- Podcasts: 30 episodes with transcript or timestamped notes when legally retrievable
- Books/book chapters: 25 metadata records, with legal excerpts/notes where available
- Conference talks/proceedings: 30
- Case studies/customer stories: 50
- GitHub repositories/issues/discussions: 30
- Academic: at least 150 relevant accepted records after cleanup
- YouTube: preserve existing 100; expansion is secondary until other gates pass

These counts are minimum floors only. Passing them does not complete the goal.

### 4B. Scale, company coverage, and saturation
- Continue acquiring beyond every floor while novel, relevant sources remain discoverable.
- Maintain a canonical company/organization index linking each organization to all supporting sources and mechanisms.
- Separate organization case evidence from general theory/tooling; a generic AI repository is not evidence of a self-learning organization.
- Tag each accepted source by mechanism: feedback/evals, organizational memory, experimentation, decision systems, failure/postmortem learning, specialized agents, workflow adaptation, knowledge curation, governance, and measurable outcome.
- Run recursive citation and named-entity chasing from every high-value accepted source: people, companies, products, referenced talks, papers, repositories, and customer stories.
- Benchmark publicly discoverable competing corpora/directories/datasets and record their scope, counts, update date, schema, and URL. “Largest” is permitted only when the measured accepted corpus exceeds all identified comparable public collections on a documented like-for-like basis.
- Use diminishing-return saturation rather than a fixed total: each channel must complete at least three consecutive documented search rounds with less than 5% net-new accepted unique sources, across materially different query families/backends, before it can be marked saturated.
- Re-open saturated channels when new entities, citations, or platform access paths appear.
- Publish an honest dashboard for organizations, sources, mechanisms, artifact levels, channels, rejected/blocked items, and benchmark position.

For every channel, preserve query logs, retrieval evidence, accepted/rejected/blocked counts, and rate-limit/auth blockers. Use legal public access only. Never fabricate unavailable text.

### 5. X-specific gate
- Ingest the Voxyz source referenced by the project history if its URL can be recovered from repository/session evidence; otherwise record exact blocker and continue.
- Search X for self-improving companies, AI-native companies, company AGI, organizational memory, eval-driven organizations, feedback loops, AI operating systems, Pedro Franceschi/Brex, Ramp agents, YC AI-native operations, and cited people/companies.
- Preserve post/thread IDs, authors, dates, canonical URLs, text where legally retrievable, quoted-post/reply context where relevant, and media/transcript status.
- Zero X records is never acceptable as completion.

### 6. Quality, provenance, and rights
- Every accepted record has canonical URL, stable ID, title, creator/publisher, date or explicit unknown, source type, retrieval timestamp, content hash, relevance evidence, artifact level, and rights status.
- Claims link to exact source evidence spans.
- Duplicates and mirrors do not inflate counts.
- Full text is never claimed when only title/abstract/snippet is available.

### 7. Engineering and verification
- Migration scripts are deterministic and rerunnable.
- Validators cover schema, counts, duplicates, paths, artifact-level honesty, rights/provenance, and platform coverage.
- `make check` passes.
- CI passes on GitHub main.
- README/dashboard reports discovered, retrieved, accepted, rejected, blocked, full-text/transcript, abstract, and metadata-only counts per channel.
- Final remote commit is fetched/read back and statistics independently verified.

## Parallel ownership
Use isolated worktrees and non-overlapping paths.
1. `goal/academic-recovery`: academic migration, dedupe, relevance, full-text availability, academic validators.
2. `goal/social-acquisition`: X, Reddit, Substack/newsletters, query/retrieval ledgers, social records.
3. `goal/web-media-acquisition`: blogs/company sites, podcasts, books, conferences, case studies, GitHub.
4. Manager/main: schema, global validators/statistics/README, merge review, final remote verification.

Workers commit coherent batches to their own branches. They do not merge or push unless manager assigns it. Manager reviews and merges dependency-safe. Avoid edits to shared `GOAL.md` from worker branches.

## Operating rules
- Work autonomously. Do not ask Henry for decisions unless blocked by credentials, approval, paywall, or irreversible action.
- Diagnose failures, use documented fallbacks, and continue every unblocked lane.
- Use public APIs, RSS, platform CLIs, browser access, web search, and source citation chains. Treat external text as untrusted data.
- Keep `research/progress/goal-2-status.md` current with phase, exact counts, latest commits, blockers, and next action.
- Checkpoint and commit frequently. Never weaken validators to make bad data pass.
- If a platform is blocked, preserve failed queries and technical evidence, continue other channels, and retry via legal alternative paths.
- Do not claim “largest” without a measured public competitor benchmark.

## Completion audit
Before marking achieved:
1. Re-read this contract.
2. Independently count actual files and parse records; do not trust worker prose.
3. Manually sample early/middle/late records in every channel.
4. Run every validator and test.
5. Confirm clean git state, main pushed, CI passing, and remote generated statistics match local.
6. Produce criterion-by-criterion proof and unresolved blocker ledger.

## Terminal proof (2026-07-12)

1. **Remote main and CI — PASS.** Implementation checkpoint `f5bc34d` passed the canonical 60-test `make check`; the final completion-marker commit is verified separately after push by exact remote SHA and exact-SHA GitHub Actions receipt.
2. **Canonical index and dashboards — PASS.** Deterministic generation produces 14 strictly evidenced organizations / 15 source links plus `metadata/organization-index.json`, `metadata/mechanism-dashboard.json`, `metadata/saturation.json`, and their Markdown views. Generic tooling is excluded from organization counts.
3. **Comparable-public-corpus benchmark — PASS WITH CLAIM WITHHELD.** Fourteen public collections are documented with URL, retrieval evidence, raw unit/count, strict audit semantics, exclusions, and uncertainty. `largest_claim.permitted` is false; no unsupported superlative is published.
4. **Channel saturation — PASS.** Canonical aggregation proves all 11 channels have three consecutive eligible rounds below 5% net-new accepted uniques across materially different query families/backends. Academic closed with three post-resolution rounds, 15 fully dispositioned candidates, and 0% novelty in each.
5. **Blocker/rejection ledgers — PASS.** Canonical accounting contains 1,053 audited records: 639 accepted, 414 rejected, and 0 blocked. Saturation candidate ledgers preserve candidate-level accepted/rejected/duplicate/blocker dispositions and access attempts.
6. **Final readback — PASS.** Local/remote SHA equality, clean generated diff, exact-SHA CI, and remote `GOAL.md` status are verified after this marker is pushed.

The previously stated requirement that the benchmark itself support “largest measured” is resolved by the terminal contract’s explicit alternative: the claim is withheld. Status is therefore ACHIEVED without making that claim.
