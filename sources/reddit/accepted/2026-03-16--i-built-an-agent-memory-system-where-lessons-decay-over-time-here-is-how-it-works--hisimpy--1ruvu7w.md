---
schema_version: 1
platform: reddit
stable_id: 1ruvu7w
title: "I built an agent memory system where lessons decay over time. Here is how it works."
publisher: "HiSimpy"
canonical_url: https://www.reddit.com/r/webdev/comments/1ruvu7w/i_built_an_agent_memory_system_where_lessons/
published_date: 2026-03-16
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "HiSimpy"
content_sha256: daa78f269e83fbe3f5958f472eab92dc4d7cb459c436f72b7f9c1e1e77e367f7
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["I am building a tool that reads GitHub and Slack to surface project state for dev teams. The interesting frontend challenge was visualizing how the agent thinks across runs, specifically the graph view that shows connections between every block of context the agent has ever read or generated.\n\nEvery piece of information in the system is a block. There are five types: agent runs, decisions, context signals, notes, and GitHub snapshots. Each block has a priority score from 0 to 100 and a set of co"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# I built an agent memory system where lessons decay over time. Here is how it works.

## Complete source text

I am building a tool that reads GitHub and Slack to surface project state for dev teams. The interesting frontend challenge was visualizing how the agent thinks across runs, specifically the graph view that shows connections between every block of context the agent has ever read or generated.

Every piece of information in the system is a block. There are five types: agent runs, decisions, context signals, notes, and GitHub snapshots. Each block has a priority score from 0 to 100 and a set of connections to other blocks that informed it or that it recommended.

I used React Flow to build the graph view. Each node is a block, each edge is a connection. You can filter by time range, block type, top priority only, or search by keyword. Clicking a node shows the full block content, its priority score, its domain, and all its connections.

The interesting part is the memory system underneath. After each run the agent generates lessons:
```typescript
{
  lesson: "Stale PRs with unmergeable state indicate dependency hygiene is not enforced",
  confidence: 0.58,
  impactScore: 68,
  appliesTo: ["stale", "unmergeable", "dependency", "security"],
  appliedCount: 0
}
```

Confidence increases as a lesson proves useful. Confidence decays as it becomes stale. The graph starts to look different over time as the agent learns which signals your project actually cares about.

The public demo runs on the real Supabase repo at ryva.dev/demo, no signup required. Built with Next.js, Convex, React Flow, and Clerk.

Happy to talk through the React Flow implementation if anyone has built something similar.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
