# Notes: Web and media acquisition

## Baseline

- Branch: `goal/web-media-acquisition` at `75e3dbe`.
- Existing substantive-looking files: 3 blogs and 2 case studies; all use an early markdown format and require lifecycle/artifact/provenance migration.
- Empty lanes: podcasts, books, conferences, GitHub.
- `research/discovery-inventory.md` contains web/company, book/reference, podcast, case-study, and talk leads that must be recovered before broad discovery.
- Shared schema is manager-owned and still models only accepted/rejected with no artifact level or GitHub platform.

## Acquisition principles

- Public primary URLs first; citation chasing from source pages and early inventory.
- Store only metadata and bounded evidence/notes unless the rights basis permits full text or the publisher supplies a transcript.
- Record every query family and retrieval outcome, including HTTP/auth/rate-limit/paywall failures.
- Deduplicate by canonical URL, stable platform identifier, and normalized title/publisher.

## Source findings

- Existing recovery: canonical replacements were created for all five early markdown files. Brex's stale AI URL is rejected; Ramp Intelligence, YC/Pedro, Ramp Engineering, and Ramp customer stories are accepted with bounded evidence.
- Early inventory recovery additionally preserved the SAP podcast announcement as rejected because no episode transcript/timestamped notes were present, the Morning Star URL as rejected because retrieval could not substantiate it, and useful primary leads including Klarna, Duolingo/ZenML, Lean Blog/Amy Edmondson, Jim Collins, Holacracy, and Corporate Rebels.
- Blogs: publisher engineering posts cover experimentation, postmortems, feedback loops, organizational memory, agent evaluation, data flywheels, and adaptive operating practices.
- Podcasts: 31 Lenny's Podcast episodes have public timestamped transcript evidence traced to original video IDs; the Lean Blog/Amy Edmondson episode supplies a public transcript. Only bounded spans are stored.
- Books: Open Library supplied bibliographic metadata after Google Books returned a hard daily-quota-zero 429. Complete book text was not requested or stored.
- Conferences: primary InfoQ/QCon, LeadDev, Microsoft Build, and AWS re:Invent pages expose talk descriptions/evidence.
- Case studies: primary Microsoft, AWS, Google Cloud, OpenAI, Anthropic/Claude, GitHub, and other vendor/customer pages provide bounded first-party evidence. Vendor outcome claims remain first-party claims, not independent validation.
- GitHub: authenticated read-only GitHub search plus README retrieval yielded repositories for agent memory, evaluation, observability, and continual-improvement infrastructure. README evidence is bounded and repository license assertions are recorded when GitHub reports them.

## Final lane counts

Accepted: blogs 77; podcasts 32; books 30; conferences 34; case studies 51; GitHub 35. Accepted podcasts are `transcript`; all other accepted records are honestly `metadata_only` with bounded evidence except books, whose metadata-only acceptance is explicitly allowed by GOAL.md.

Preserved non-accepted records: 309 rejected and 7 blocked. The large rejected sets include surplus bounded discoveries, duplicates, wrong-lane results, false positives, and sources outside the review-bounded accepted sets.
