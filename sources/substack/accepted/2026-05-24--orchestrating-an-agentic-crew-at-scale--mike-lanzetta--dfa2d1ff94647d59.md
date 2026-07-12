---
schema_version: 1
platform: substack
stable_id: dfa2d1ff94647d59
title: "Orchestrating an Agentic Crew at Scale"
publisher: "Mike Lanzetta"
canonical_url: https://innerloopai.substack.com/p/orchestrating-an-agentic-crew-at
published_date: 2026-05-24
content_type: article
status: accepted
relevance_status: relevant
provenance: "Jina Reader direct fetch of the canonical individual article"
rights_status: third-party
rights_holder: "Mike Lanzetta"
content_sha256: 858030d62c4ed7f9b60316d3924e2e90e57c47dea72f7556b3d43608eac2afd5
availability: metadata_only
raw_path: research/social/raw/substack/dfa2d1ff94647d59.md
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["A year ago, I proposed that engineering teams should “start slow” to build the foundations for AI integration. Since then, my personal limit-testing - pushing roughly 60,000 lines of code in a two-week sprint - has forced a total reassessment of the engineering “inner loop”.\n\nBefore this system, I was spending half my day context-switching, manually re-explaining architectural constraints to agents that had drifted from the project’s original intent. What I’ve landed on is a shift away from “pai"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/substack/dfa2d1ff94647d59.md.
---
# Orchestrating an Agentic Crew at Scale

## Verified source excerpt

A year ago, I proposed that engineering teams should “start slow” to build the foundations for AI integration. Since then, my personal limit-testing - pushing roughly 60,000 lines of code in a two-week sprint - has forced a total reassessment of the engineering “inner loop”.

Before this system, I was spending half my day context-switching, manually re-explaining architectural constraints to agents that had drifted from the project’s original intent. What I’ve landed on is a shift away from “pairing” toward managing an orchestrated system. I call this the **[hybrid v-team model](https://github.com/noodlefrenzy/vteam-hybrid)**: a framework where the human is the architect of intent, and a specialized crew of agents manages the mechanical labor of implementation.

In this system, I’ve moved past the generalist chatbot. I now operate with a consolidated roster of 18 specialized agents across four priority tiers: P0 Core, P1 Essential, P2 Regular, and Cloud Specialists.

I started with a roster of 32 agents which proved unreliable and unwieldy. The real breakthrough was the **“Absorbs” pattern**, where I merged 32 original personas into 18 capability-based agents to reduce coordination overhead, with a prioritized set and others only called in on-demand. This starts with **Coach Cam (P0)**, my human interface agent. Cam’s job is to pressure-test my vision via 5 Whys, inversion, and constraint surfacing before a single line is written. Only once the intent is clarified do I trigger the build-phase agents:

*   **Archie (Architecture + Data + API):** Absorbed Schema Sam and Contract Cass to own system boundaries, data modeling, and migration safety.

*   **Ines (DevOps + SRE + Chaos):** Owns everything between git push and production traffic.

*   **Pierrot (Security + Compliance):** Carries a dark-humored lens for vulnerabilities and SOC 2 compliance, with full veto power.

You: I want to build a CLI tool that converts markdown to PDF Cam: Let me explore that with you. Who’s the target user — developers or non-technical users? And what’s your priority: fidelity to the markdown spec, or speed of conversion? You: Developers, and speed matters more than perfect rendering. Cam: Got it. Let me probe a few more things before we commit to an approach...

## Acquisition limits

This is a bounded span from a direct fetch of the individual article, not a complete copy.
