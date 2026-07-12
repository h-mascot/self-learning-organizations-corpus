---
schema_version: 1
platform: x
stable_id: 2038132294817656978
title: "The reason autoresearch hit 42,000 GitHub stars in a week is that the architecture ports to anything"
publisher: "Aakash Gupta"
canonical_url: https://x.com/aakashgupta/status/2038132294817656978
published_date: 2026-03-29
content_type: post
status: accepted
relevance_status: relevant
provenance: "FxTwitter public API response for the canonical X resource"
rights_status: third-party
rights_holder: "Aakash Gupta"
content_sha256: 9e6964776cd03622056b0f7b4dba662e36325d4be1a19cd60a5b3ad182343ab8
availability: full_text
raw_path: research/social/raw/x/2038132294817656978.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["The reason autoresearch hit 42,000 GitHub stars in a week is that the architecture ports to anything with a score.\n\nKarpathy built it for ML training. http://train.py is the code the agent edits. val_bpb is the metric. program.md is the human's research direction. http://prepare.py is the locked eval harness. Git commit keeps winners, git reset reverts losers.\n\nI ported it to prompt engineering. The mapping took about ten minutes because every component has a direct equivalent.\n\nhttp://train.py "]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/x/2038132294817656978.json.
---
# The reason autoresearch hit 42,000 GitHub stars in a week is that the architecture ports to anything

## Complete source text

The reason autoresearch hit 42,000 GitHub stars in a week is that the architecture ports to anything with a score.

Karpathy built it for ML training. http://train.py is the code the agent edits. val_bpb is the metric. program.md is the human's research direction. http://prepare.py is the locked eval harness. Git commit keeps winners, git reset reverts losers.

I ported it to prompt engineering. The mapping took about ten minutes because every component has a direct equivalent.

http://train.py becomes your skill or system prompt file. val_bpb becomes a pass/fail checklist, 3-6 yes/no questions scored against every output. program.md becomes your instructions to the agent describing what to optimize and what constraints to respect. http://prepare.py becomes a locked eval script the agent builds once and can never touch again. Git works the same.

The architecture holds because Karpathy made one design choice that almost nobody discusses: he separated the system into exactly four roles. A file that changes. A metric that judges. A direction that guides. And a constraint that locks. Those four roles describe every functional optimization loop in existence. A/B testing. Clinical trials. Lean manufacturing. PDCA. The scientific method itself.

Most AI agent frameworks fail because they blur these boundaries. The agent that writes the code also evaluates the code. The system that sets the goal also measures progress toward it. Autoresearch works because the agent that mutates the file has zero control over how that mutation gets scored.

The prompt engineering version produces the same outputs Karpathy gets. An improved file saved separately, original untouched. A results log showing every round's score. A changelog explaining what the agent tried, what worked, and what didn't. ~12 iterations per hour. ~100 overnight. ~$25 in compute.

The locked eval is the piece most people will skip and the piece that makes everything else work. Without it, the agent optimizes the test instead of optimizing the prompt.

If you can define 3-6 binary criteria for what "good" looks like, you can run this loop on anything. Prompts, email sequences, landing page copy, onboarding flows, support scripts. The Karpathy loop is a universal optimization architecture disguised as an ML tool.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
