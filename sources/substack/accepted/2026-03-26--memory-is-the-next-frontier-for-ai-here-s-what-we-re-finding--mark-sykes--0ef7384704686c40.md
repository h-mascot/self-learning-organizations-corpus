---
schema_version: 1
platform: substack
stable_id: 0ef7384704686c40
title: "Memory Is the Next Frontier for AI. Here’s What We’re Finding."
publisher: "Mark Sykes"
canonical_url: https://enterprisecontextmanagement.substack.com/p/memory-is-the-next-frontier-for-ai
published_date: 2026-03-26
content_type: article
status: accepted
relevance_status: relevant
provenance: "Jina Reader direct fetch of the canonical individual article"
rights_status: third-party
rights_holder: "Mark Sykes"
content_sha256: ff72ea6f5a913da32de6625372f1abbf0d3fc552a131c60c1f57381f66bbe24a
availability: metadata_only
raw_path: research/social/raw/substack/0ef7384704686c40.md
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["Memory is one of the next major frontiers for AI. Models are increasingly capable, but they don’t retain anything between invocations. An agent can’t learn from yesterday’s execution to improve today’s. It can’t accumulate skill with a tool that’s used a hundred times. The industry knows this. What’s less clear is how to solve it.\n\nAt AI One, we’ve been tackling this “memory problem” for large enterprises. We’ve created a Memory Engine with three asynchronous pipelines that create a feedback loo"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/substack/0ef7384704686c40.md.
---
# Memory Is the Next Frontier for AI. Here’s What We’re Finding.

## Verified source excerpt

Memory is one of the next major frontiers for AI. Models are increasingly capable, but they don’t retain anything between invocations. An agent can’t learn from yesterday’s execution to improve today’s. It can’t accumulate skill with a tool that’s used a hundred times. The industry knows this. What’s less clear is how to solve it.

At AI One, we’ve been tackling this “memory problem” for large enterprises. We’ve created a Memory Engine with three asynchronous pipelines that create a feedback loop between agent execution and agent learning. Each pipeline captures a different class of knowledge from each run and injects it into the next. These are early findings, not final answers. But they suggest structured memory may be a more consequential lever than model sophistication or prompt engineering.

[![Image 1](https://substackcdn.com/image/fetch/$s_!4ujv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27986ed0-8281-406c-9d41-06e147f1f74b_4368x3144.png)](https://substackcdn.com/image/fetch/$s_!4ujv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27986ed0-8281-406c-9d41-06e147f1f74b_4368x3144.png)

Every serious engineering system has a feedback loop. Gas pipelines have PID controllers (Proportional, Integral, and Derivative). In machine learning, gradient descent makes training observable, debuggable, and repeatable. Software teams have CI/CD. The dominant agentic frameworks have none. Every invocation is independent. Context is assembled fresh each time: conversational history, tool definitions, and retrieved documents are appended into a single payload that grows until it hits the token limit. Nothing carries forward.

The consequences are many. An agent queries a technology catalog where the same vendor is listed as “IBM” in one system and “International Business Machines Corp.” in another. The agent fails on entity resolution. It failed on the same resolution yesterday. It will fail again tomorrow. An agent calls an API that returns 15,000 tokens, consuming budget that should go to reasoning. Another agent violates a business rule. Nothing stops it from repeating the same mistakes over and over.

The LLM isn’t the problem. The problem is the absence of a feedback loop to retain important learnings, discard what’s irrelevant, or compound skills over time.

Our approach consists of three asynchronous pipelines. Each handles a different class of learned knowledge: episodic, procedural, and semantic. Their design is guided by the idea that agents need to remember different kinds of things; each requires distinct storage, retrieval, and update mechanisms. All three run in parallel with the main [agent loop](https://enterprisecontextmanagement.substack.com/p/stop-building-agent-chains-start).

Every agent execution produces a trace: reasoning steps, tool calls, and outcomes. Episodic memory pipelines review these traces, cluster similar activities, and identify “golden trajectories” — execution paths that represent best practices for a given task class.

## Acquisition limits

This is a bounded span from a direct fetch of the individual article, not a complete copy.
