---
schema_version: 1
platform: reddit
stable_id: 1q785ld
title: "From support chat to sales intelligence: a multi-agent system with shared long-term memory"
publisher: "nicolo_memorymodel"
canonical_url: https://www.reddit.com/r/LangChain/comments/1q785ld/from_support_chat_to_sales_intelligence_a/
published_date: 2026-01-08
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "nicolo_memorymodel"
content_sha256: 889a754421c027a3f42856c08a1f36b8049b390ca56ffdd5b69b1eef0ebe985e
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["Over the last few days, I’ve been working on a small open-source project to explore a problem I often encounter in real production-grade agent systems.\n\nSupport agents answer users, but valuable commercial signals tend to get lost.\n\nSo I built a reference system where:\n\n\\- one agent handles customer support: it answers user questions and collects information about their issues, all on top of a shared, unified memory layer\n\nhttps://preview.redd.it/8h3ltzywo3cg1.jpg?width=1384&format=pjpg&auto=web"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# From support chat to sales intelligence: a multi-agent system with shared long-term memory

## Complete source text

Over the last few days, I’ve been working on a small open-source project to explore a problem I often encounter in real production-grade agent systems.

Support agents answer users, but valuable commercial signals tend to get lost.

So I built a reference system where:

\- one agent handles customer support: it answers user questions and collects information about their issues, all on top of a shared, unified memory layer

https://preview.redd.it/8h3ltzywo3cg1.jpg?width=1384&format=pjpg&auto=webp&s=ecaf91c3ee957faeedbb05f55be69932dfdc7419

\- a memory node continuously generates user insights: it tries to infer what could be sold based on the user’s problems (for example, premium packages for an online bank account in this demo)

\- a seller-facing dashboard shows what to sell and to which user

https://preview.redd.it/f28dq9fzo3cg1.jpg?width=1600&format=pjpg&auto=webp&s=05f63061a9c0098cab06d340995fe1cf399a33de

On the sales side, only structured insights are consumed — not raw conversation logs.

This is not about prompt engineering or embeddings.

It’s about treating memory as a first-class system component.

I used the memory layer I’m currently building, but I’d really appreciate feedback from anyone working on similar production agent systems.

Happy to answer technical questions.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
