---
schema_version: 1
platform: reddit
stable_id: 1ruk4g4
title: "How are people actually testing agents before production?"
publisher: "HpartidaB"
canonical_url: https://www.reddit.com/r/AI_Agents/comments/1ruk4g4/how_are_people_actually_testing_agents_before/
published_date: 2026-03-15
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "HpartidaB"
content_sha256: 1f3d39526341ea25ae96a387b3a67e6ec92ff7cc050f784cf2466e704a04f9c1
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["I've been talking with several people building AI agents recently and one thing that keeps coming up is how hard it is to test them before deploying.\n\nMost of the tooling I see focuses on things like:\n- prompt evals\n- LLM-as-judge\n- trace analysis after the agent already ran\n\nBut many of the weird behaviors I've seen only appear when agents run through longer interactions.\n\nFor example when:\n- tools fail or return partial data\n- users change goals mid-task\n- multiple decisions accumulate across "]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# How are people actually testing agents before production?

## Complete source text

I've been talking with several people building AI agents recently and one thing that keeps coming up is how hard it is to test them before deploying.

Most of the tooling I see focuses on things like:
- prompt evals
- LLM-as-judge
- trace analysis after the agent already ran

But many of the weird behaviors I've seen only appear when agents run through longer interactions.

For example when:
- tools fail or return partial data
- users change goals mid-task
- multiple decisions accumulate across steps
- sessions become long and context starts drifting

In isolated tests everything looks fine, but after 5–7 steps things can get messy.

I'm curious how people here are approaching this.

Are you mostly:
A) running prompt/eval tests
B) replaying real traces
C) simulating scenarios (synthetic users, tool failures, etc.)
D) just discovering issues in production 😅

I'm exploring this space right now and trying to understand what people actually do in practice.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
