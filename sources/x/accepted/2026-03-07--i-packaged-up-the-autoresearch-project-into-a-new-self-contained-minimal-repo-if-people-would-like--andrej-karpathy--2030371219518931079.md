---
schema_version: 1
platform: x
stable_id: 2030371219518931079
title: "I packaged up the \"autoresearch\" project into a new self-contained minimal repo if people would like"
publisher: "Andrej Karpathy"
canonical_url: https://x.com/karpathy/status/2030371219518931079
published_date: 2026-03-07
content_type: post
status: accepted
relevance_status: relevant
provenance: "FxTwitter public API response for the canonical X resource"
rights_status: third-party
rights_holder: "Andrej Karpathy"
content_sha256: 32ed96f7e14901e4f455b529b7962f6232a27a9f9ea6af440466a633f3de7f84
availability: full_text
raw_path: research/social/raw/x/2030371219518931079.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["I packaged up the \"autoresearch\" project into a new self-contained minimal repo if people would like to play over the weekend. It's basically nanochat LLM training core stripped down to a single-GPU, one file version of ~630 lines of code, then:\n\n- the human iterates on the prompt (.md)\n- the AI agent iterates on the training code (.py)\n\nThe goal is to engineer your agents to make the fastest research progress indefinitely and without any of your own involvement. In the image, every dot is a com"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/x/2030371219518931079.json.
---
# I packaged up the "autoresearch" project into a new self-contained minimal repo if people would like

## Complete source text

I packaged up the "autoresearch" project into a new self-contained minimal repo if people would like to play over the weekend. It's basically nanochat LLM training core stripped down to a single-GPU, one file version of ~630 lines of code, then:

- the human iterates on the prompt (.md)
- the AI agent iterates on the training code (.py)

The goal is to engineer your agents to make the fastest research progress indefinitely and without any of your own involvement. In the image, every dot is a complete LLM training run that lasts exactly 5 minutes. The agent works in an autonomous loop on a git feature branch and accumulates git commits to the training script as it finds better settings (of lower validation loss by the end) of the neural network architecture, the optimizer, all the hyperparameters, etc. You can imagine comparing the research progress of different prompts, different agents, etc.

https://github.com/karpathy/autoresearch
Part code, part sci-fi, and a pinch of psychosis :)

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
