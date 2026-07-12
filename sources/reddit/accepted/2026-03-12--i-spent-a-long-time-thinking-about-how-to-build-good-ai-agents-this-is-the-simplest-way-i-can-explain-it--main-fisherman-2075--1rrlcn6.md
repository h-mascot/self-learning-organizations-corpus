---
schema_version: 1
platform: reddit
stable_id: 1rrlcn6
title: "I spent a long time thinking about how to build good AI agents. This is the simplest way I can explain it."
publisher: "Main-Fisherman-2075"
canonical_url: https://www.reddit.com/r/AI_Agents/comments/1rrlcn6/i_spent_a_long_time_thinking_about_how_to_build/
published_date: 2026-03-12
content_type: post
status: accepted
relevance_status: relevant
provenance: "Arctic Shift public Reddit archive record with exact post ID"
rights_status: third-party
rights_holder: "Main-Fisherman-2075"
content_sha256: f6418f2a3cdcb850eb602cb21b4c462e27b412c2bff776df61f863ade20bbcca
availability: full_text
raw_path: research/social/raw/reddit/selected-posts.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["For a long time I was confused about agents.  \n  \nEvery week a new framework appears:  \nLangGraph. AutoGen. CrewAI. OpenAI Agents SDK. Claude Agents SDK.  \n  \nAll of them show you how to run agents.  \nBut none of them really explain how to think about building one.  \n  \nSo I spent a while trying to simplify this for myself.  \n  \nThe mental model that finally clicked:  \n  \nAgents are finite state machines where the LLM decides the transitions.  \n  \nHere's what I mean.  \n  \nStart with graph theory"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/reddit/selected-posts.json.
---
# I spent a long time thinking about how to build good AI agents. This is the simplest way I can explain it.

## Complete source text

For a long time I was confused about agents.  
  
Every week a new framework appears:  
LangGraph. AutoGen. CrewAI. OpenAI Agents SDK. Claude Agents SDK.  
  
All of them show you how to run agents.  
But none of them really explain how to think about building one.  
  
So I spent a while trying to simplify this for myself.  
  
The mental model that finally clicked:  
  
Agents are finite state machines where the LLM decides the transitions.  
  
Here's what I mean.  
  
Start with graph theory. A graph is just: nodes + edges  
  
A finite state machine is a graph where:  
  
`nodes = states`  
`edges = transitions (with conditions)`  
  
An agent is almost the same thing, with one difference.  
  
Instead of hardcoding:  
  
`if output["status"] == "done":`  
`go_to_next_state()`  
  
The LLM decides which transition to take based on its output.  
  
So the structure looks like this:  
  
`Prompt: Orchestrator`  
`↓ (LLM decides)`  
`Prompt: Analyze`  
`↓ (always)`  
`Prompt: Summarize`  
`↓ (conditional — loop back if not good enough)`  
`Prompt: Analyze   ← back here`  
  
Notice I'm calling every node a Prompt, not a Step or a Task.  
  
That's intentional.  
  
Every state in an agent is fundamentally a prompt. Tools, memory, output format — these are all attachments \*to\* the prompt, not peers of it. The prompt is the first-class citizen. Everything else is metadata.  
  
Once I started thinking about agents this way, a lot clicked:  
  
\- Why LangGraph literally uses graphs  
\- Why agents sometimes loop forever (the transition condition never fires)  
\- Why debugging agents is hard (you can't see which state you're in)  
\- Why prompts matter so much (they ARE the states)  
  
But it also revealed something I hadn't noticed before.  
  
There are dozens of tools for \*\*running\*\* agents. Almost nothing for \*\*designing\*\* them.  
  
Before you write any code, you need to answer:  
\- How many prompt states does this agent have?  
\- What are the transition conditions between them?  
\- Which transitions are hardcoded vs LLM-decided?  
\- Where are the loops, and when do they terminate?  
\- Which tools attach to which prompt?  
  
Right now you do this in your head, or in a Miro board with no agent-specific structure.  
  
The design layer is a gap nobody has filled yet.  
  
Anyway, if you're building agents and feeling like something is missing, this framing might help. Happy to go deeper on any part of this.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
