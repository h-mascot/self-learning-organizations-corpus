---
schema_version: 1
platform: reddit
stable_id: 1rzpvfd
title: "I built a persistent memory system for AI agents because I got tired of them forgetting everything over time"
publisher: "Salty-Asparagus-4751"
canonical_url: https://www.reddit.com/r/openclaw/comments/1rzpvfd/i_built_a_persistent_memory_system_for_ai_agents/
published_date: 2026-03-21
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "Salty-Asparagus-4751"
content_sha256: 7c22b922a12efd2040d219a7843fa8b3cba96d74951fab93e57c972c303d8045
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["I've spent thousands of dollars on API costs running Claude Code and OpenClaw heavily over the past year, and the same problem kept killing productivity: **the agent forgets everything when the session ends**.\n\nYou tell your agent to restructure your portfolio on Monday, explain your risk tolerance, walk through the rationale. Wednesday it asks your risk tolerance again from scratch. 20 minutes and 30K+ tokens gone on something you already discussed.\n\nI tried the standard fixes:\n\n- **MEMORY.md**"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# I built a persistent memory system for AI agents because I got tired of them forgetting everything over time

## Complete source text

I've spent thousands of dollars on API costs running Claude Code and OpenClaw heavily over the past year, and the same problem kept killing productivity: **the agent forgets everything when the session ends**.

You tell your agent to restructure your portfolio on Monday, explain your risk tolerance, walk through the rationale. Wednesday it asks your risk tolerance again from scratch. 20 minutes and 30K+ tokens gone on something you already discussed.

I tried the standard fixes:

- **MEMORY.md** — overflows after a week. You're constantly pruning.
- **RAG / vector search** — great if you know what to search for. But "do I already have context on database migrations?" isn't a search query — it's an awareness question. The agent doesn't know what it knows.
- **Large context windows** — attention degrades, token bill explodes.
- **Hosted memory services** — another API key, another dependency, another bill.

None of them solved the core issue: **the agent can't tell "I know this" from "I've never seen this" without loading everything or searching for something specific.**

So I built **Hipocampus**. The key idea is a compaction tree.

### How it works

Your conversation history compresses through 5 levels: **raw → daily → weekly → monthly → root**.

The root level is a topic index called ROOT.md. Here's a reconstructed example based on my actual usage (~2 months of daily OpenClaw sessions as a personal assistant):

```
## Active Context (recent ~7 days)
- 2026-03-18: FOMC recap briefed, portfolio rebalancing options drafted, 2 email replies sent
- 2026-03-17: Tokyo flight comparison saved (3 options), hotel vs Airbnb analysis done
- 2026-03-16: Morning briefing flagged earnings miss on watchlist stock, spending alert triggered
- 2026-03-15: Weekly expense report auto-generated, dentist appointment rescheduled
  ...

## Recent Patterns
- Checks portfolio + market news every morning — pre-generate briefing before 8am
- Travel planning active (Tokyo trip Apr 1-5) — expect follow-ups on itinerary, restaurants, JR pass
- Email tone preference: direct, short, no corporate fluff — mirror this in all drafts
- Dining spending trending up — nudge if weekly total > $150
- Tends to forget follow-ups with contacts met at events — auto-remind after 2 weeks
- Weekend = personal errands + language study. Weekday = work + investing
  ...

## Historical Summary
- 2026-03 W3: FOMC monitoring, Tokyo trip planning, Q1 expense analysis, 2 networking follow-ups, car insurance renewal research
- 2026-03 W2: earnings season alerts (4 holdings reported), weekly meal prep plan started, dentist/doctor appointments booked, apartment lease renewal negotiation draft
- 2026-03 W1: monthly portfolio review, competitor monitoring report for side project, JLPT N3 mock test (68% — grammar weak), tax docs sent to CPA
- 2026-02 W4: apartment search finalized (signed lease), morning briefing format v2 (added calendar preview), Valentine's dinner reservation, 3 networking follow-ups
- 2026-02 W3: apartment search (5 viewings, 2 shortlisted), tax document collection (W-2, 1099s), habit tracking setup (exercise 3x/week, water intake)
- 2026-02 W2: portfolio restructuring (tech→dividend pivot), set up stock alerts + earnings calendar, flight deal monitoring for spring trip
- 2026-02 W1: morning briefing system established (8am daily), personal CRM setup (imported 40+ contacts), budget categories defined, JLPT N3 study plan created

## Topics Index
daily-briefing: morning-news, portfolio-summary, calendar-preview, pending-follow-ups, ...
investing: portfolio-monitoring, stock-alerts, watchlist, earnings-tracking, sector-analysis, ...
macro: fomc, fed-speakers, rate-decisions, cpi-ppi, jobs-report, ...
travel: flight-search, hotel-comparison, airbnb, itinerary, restaurant-recs, transport-passes, ...
email: inbox-triage, draft-replies, tone-matching, auto-rules, priority-senders, ...
finance: expense-tracking, budget-categories, spending-alerts, monthly-report, savings-goal, ...
personal-crm: contact-notes, meeting-history, follow-up-reminders, event-connections, ...
calendar: task-management, reminders, appointment-booking, weekly-review, time-blocking, ...
housing: apartment-search, lease-negotiation, neighborhood-comparison, move-planning, ...
language: jlpt-n3, vocab-quiz, grammar-drills, mock-tests, progress-tracking, ...
health: habit-tracking, exercise-log, water-intake, medical-appointments, meal-prep, ...
tax: document-collection, cpa-communication, capital-gains-summary, filing-deadline, ...
shopping: deal-alerts, price-comparison, reservation-monitoring, wishlist, ...
side-project: competitor-monitoring, market-research, user-feedback-tracking, ...
insurance: car-renewal, plan-comparison, coverage-review, ...
(... 70+ topics across 15 categories)
```

That's ~2 months. The agent reads this at session start (~3K tokens) and immediately knows what it has context on, when it last dealt with each topic, and where to drill down. No blind file exploration.

When the agent needs more detail, it drills down into the compaction tree. Here's what a monthly summary looks like (truncated):

```
# Monthly Summary: 2026-02

## Key Themes

### 1. Portfolio Restructuring (investing)
Shifted from growth/tech-heavy to 40% dividend + 30% value + 30% growth.
Triggered by rising rate environment. Earnings calendar alerts set up for
all 12 holdings. Weekly rebalancing check every Monday morning.

### 2. Morning Briefing System (daily-briefing)
8am daily: portfolio moves, macro news weighted by interest, yesterday's
pending follow-ups. v2 update (late Feb): added calendar preview for the
day + weather. FOMC/Fed events highlighted separately when active.

### 3. Apartment Search → Signed (housing)
5 viewings over 2 weeks. Shortlisted 2 (Brooklyn vs Jersey City).
Final: Jersey City — PATH access + $400/mo cheaper. Lease signed Feb 25.
Move-in checklist created, utilities setup tracked.

### 4. Personal CRM Setup (personal-crm)
Imported 40+ contacts from phone + LinkedIn. Tagged by context (work,
investor, friend, event). Auto-remind for follow-ups if no contact in
14 days. 3 follow-ups completed, 2 new connections from conference.

### 5. Tax Season Prep (tax)
W-2, 1099s, Blockchain tx history collected. CPA meeting scheduled Mar 5.
Capital gains/losses summary: trade losses offset stock gains by ~$2K.

  ... (+ habit tracking setup, flight deal monitoring, budget categories, language study plan, insurance review)

## Major Decisions
- Dividend pivot over growth — rate environment (2026-02-05)
- Briefing at 8am not 7am — never reads before 8 (2026-02-10)
- Jersey City over Brooklyn — PATH + price (2026-02-22)
- JLPT N3 target: July exam (2026-02-01)

## Carried Forward
- Tokyo trip — dates confirmed, flights/hotel not booked
- JLPT N3 — daily vocab active, grammar drills starting March
- CPA meeting — Mar 5, final doc review needed
- Meal prep plan — starting March (goal: cook 4x/week)
```

ROOT.md gives the bird's-eye view. Monthly/weekly summaries give the detail. Raw logs are always preserved — nothing is ever lost, just compressed.

### Why not just RAG?

They're complementary, not competing:

- **RAG** answers: "find me everything related to my investment portfolio" (semantic similarity)
- **ROOT.md** answers: "do I already know about this?" (awareness — no query needed)
- **Compaction tree** answers: "what did we discuss last week?" (time-based browsing, hierarchical drill-down)

Hipocampus supports both — optional hybrid search via qmd (BM25 + vector) for when you need semantic retrieval.

### How it compares

**vs. cloud/enterprise solutions (Mem0, Letta, Mengram)** — they're solving a different problem: multi-user memory, knowledge graphs, framework integrations. Great if you need that. Hipocampus is for **any AI agent that needs persistent memory with zero overhead**.

| | Hipocampus | Mem0 | Letta | Mengram |
|---|---|---|---|---|
| Setup | `npx hipocampus init` | pip + API key + vector DB | Docker + Postgres + ADE | API key + SDK |
| Infrastructure | None (just markdown) | Server or cloud | Server required | Cloud API |
| Cost | Free (MIT) | $19-249/mo | Cloud pricing | $0-99/mo |
| Memory awareness | ROOT.md (constant cost) | Query-dependent (RAG) | Query-dependent | Query-dependent |
| Temporal drill-down | Compaction tree | No | No | No |
| Data ownership | Your filesystem | Their cloud (or self-host) | Your server | Their servers |
| Context pollution | Subagent isolation | Inline extraction | Inline extraction | Inline extraction |

**vs. local-first alternatives (Hmem, Mneme)** — these are the closest to what Hipocampus does. Honest comparison:

| | Hipocampus | Hmem | Mneme |
|---|---|---|---|
| Storage | Markdown files | SQLite (.hmem file) | Plain text files |
| Memory structure | 5-level compaction tree | 5-level hierarchy | Flat (facts + task state) |
| Search | BM25 + vector + LLM rerank (via qmd) | Lazy-loaded drill-down | No search (explicit structure only) |
| Cross-tool portable | CLI (`npx` init) | MCP server (Cursor, Windsurf, etc.) | Session-based |
| Session start cost | ~3K tokens (ROOT.md) | ~20 tokens (L1 summary) | Varies |
| Human-editable | Yes (markdown) | No (SQLite binary) | Yes (text files) |
| Compaction | Auto (raw→daily→weekly→monthly→root) | Manual hierarchy | No compaction |
| Hybrid search | Yes (optional qmd) | No | No |

### Quick details

- **3-tier memory**: hot (always loaded), warm (on-demand), cold (searchable archive)
- **Subagent memory writes** — memory operations run in background, zero context pollution in your main session
- **Pre-compaction hooks** — automatically preserves memory before context window compression
- **Works with Claude Code and OpenClaw** — MIT licensed, zero dependencies

### Try it

```
npx hipocampus init
```

Creates the full memory structure, installs agent skills, sets up hooks. ~30 seconds.

GitHub: https://github.com/kevin-hs-sohn/hipocampus

Built from real pain, tested heavily. Happy to answer questions about the compaction algorithm or how it works in practice.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
