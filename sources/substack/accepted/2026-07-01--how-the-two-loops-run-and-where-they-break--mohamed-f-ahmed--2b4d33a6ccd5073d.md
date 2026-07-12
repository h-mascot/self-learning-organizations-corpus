---
schema_version: 1
platform: substack
stable_id: 2b4d33a6ccd5073d
title: "How the Two Loops Run — And Where They Break"
publisher: "Mohamed F. Ahmed"
canonical_url: https://ainativefounder.substack.com/p/how-the-two-loops-run-and-where-they
published_date: 2026-07-01
content_type: article
status: accepted
relevance_status: relevant
provenance: "Jina Reader direct fetch of the canonical individual article"
rights_status: third-party
rights_holder: "Mohamed F. Ahmed"
content_sha256: 26127363d6963aed2f68155579e2e6b6a0b48fe1c90f108183af78bdc1f09f53
availability: metadata_only
raw_path: research/social/raw/substack/2b4d33a6ccd5073d.md
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["[![Image 1](https://substackcdn.com/image/fetch/$s_!tBb_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ae8c1d6-4734-4954-b57d-394faf7b8ec9_1584x672.jpeg)](https://substackcdn.com/image/fetch/$s_!tBb_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ae8c1d6-4734-4954-b57d-394faf7b8ec9_1584x672.jpeg)\n\nAndrej Karpathy has been tuning neural networks for a"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/substack/2b4d33a6ccd5073d.md.
---
# How the Two Loops Run — And Where They Break

## Verified source excerpt

[![Image 1](https://substackcdn.com/image/fetch/$s_!tBb_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ae8c1d6-4734-4954-b57d-394faf7b8ec9_1584x672.jpeg)](https://substackcdn.com/image/fetch/$s_!tBb_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ae8c1d6-4734-4954-b57d-394faf7b8ec9_1584x672.jpeg)

Andrej Karpathy has been tuning neural networks for about twenty years. He helped build the field. So when he wired up an agent to optimize the training of nanochat — his "best ChatGPT $100 can buy" — and let it run overnight, he expected it to teach him nothing. He'd already picked the good settings. He always picks the good settings.

He woke up to find the agent had run hundreds of experiments on a single GPU and found tunings he'd missed.

> "I let auto research go for like overnight and it came back with tunings that I didn't see… I shouldn't be a bottleneck, I shouldn't be running these hyperparameter search optimizations, I shouldn't be looking at the results. There's objective criteria in this case. You just have to arrange it so that it can just go forever" (No Priors, March 2026).

Sit with that. One of the most capable practitioners alive looked at a closed-loop result that beat his own twenty years of intuition and concluded: _I shouldn't be the bottleneck._ That's the whole shift in one sentence. Once the loop runs, the founder's job stops being "do the work" and becomes "arrange the loop, and review the diff."

Over three articles, I built up to this. The axis: conventional companies run as open loops, AI-native ones as closed loops. The architecture: two loops — one that runs the business, one that improves the product — sharing a single substrate. The substrate: four kinds of files in a folder that an agent can read and write. The substrate is built. This is the piece where the loops actually run. And because I promised in Article 2 that I wouldn't sell this clean, it's also the piece where I show you exactly where they break.

Let's use the repo from last week. Helpdesk Copilot: an assistant that answers customer questions from a company's own docs. Its substrate has `specs/`, `evidence/`, `decisions/`, `state/`, and two skills in `.claude/skills/`. Watch the business loop turn once.

**Evidence lands.** Forty support tickets come in this week and drop into `evidence/tickets/`. Raw, messy, real.

## Acquisition limits

This is a bounded span from a direct fetch of the individual article, not a complete copy.
