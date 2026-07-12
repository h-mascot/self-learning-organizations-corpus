---
schema_version: 1
platform: reddit
stable_id: 1rbn18z
title: "Our agent passed every demo… then failed quietly after 3 weeks in production"
publisher: "Emma_4_7"
canonical_url: https://www.reddit.com/r/LLMDevs/comments/1rbn18z/our_agent_passed_every_demo_then_failed_quietly/
published_date: 2026-02-22
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "Emma_4_7"
content_sha256: 38787601ece6a9b5a7113803ecfdbd48ff1d1e2bb927671fb67d9066225a116f
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["We shipped an internal ops agent a month ago.\n\nFirst week? Amazing.  \nAnswered questions about past tickets, summarized Slack threads, even caught a small billing issue before a human did. Everyone was impressed.\n\nBy week three, something felt… off.\n\nIt wasn’t hallucinating. It wasn’t crashing.  \nIt was just slowly getting more rigid.\n\nIf it solved a task one way early on, it kept using that pattern even when the context changed.  \nIf a workaround “worked once,” it became the default.  \nIf a con"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# Our agent passed every demo… then failed quietly after 3 weeks in production

## Complete source text

We shipped an internal ops agent a month ago.

First week? Amazing.  
Answered questions about past tickets, summarized Slack threads, even caught a small billing issue before a human did. Everyone was impressed.

By week three, something felt… off.

It wasn’t hallucinating. It wasn’t crashing.  
It was just slowly getting more rigid.

If it solved a task one way early on, it kept using that pattern even when the context changed.  
If a workaround “worked once,” it became the default.  
If a constraint was temporary, it started treating it as permanent.

Nothing obviously broken. Just gradual behavioral hardening.

What surprised me most: the data was there.  
Updated docs were there.  
New decisions were there.

The agent just didn’t *revise* earlier assumptions. It kept layering new info on top of old conclusions without re-evaluating them.

At that point I stopped thinking about “memory size” and started thinking about “memory governance.”

For those running agents longer than a demo cycle How are you handling belief revision over time?  
Are you mutating memory? Versioning it? Letting it decay?

Or are you just hoping retrieval gets smarter?

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
