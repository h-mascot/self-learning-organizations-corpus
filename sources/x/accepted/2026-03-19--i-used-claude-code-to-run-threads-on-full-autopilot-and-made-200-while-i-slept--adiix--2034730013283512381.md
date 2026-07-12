---
schema_version: 1
platform: x
stable_id: 2034730013283512381
title: "I Used Claude Code to Run Threads on Full Autopilot and Made $200 While I Slept"
publisher: "AdiiX"
canonical_url: https://x.com/adiix_official/status/2034730013283512381
published_date: 2026-03-19
content_type: post
status: accepted
relevance_status: relevant
provenance: "FxTwitter public API response for the canonical X resource"
rights_status: third-party
rights_holder: "AdiiX"
content_sha256: b2fac9f753bd785f046a4582040f08f7d05615001d0ee1c52af8f07a339b5a8b
availability: full_text
raw_path: research/social/raw/x/2034730013283512381.json
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["So I had Claude Code running a Threads account completely automatically. Two weeks later, it had generated $200 in affiliate revenue. And honestly? My first reaction was: \"Is it really this easy?\"\n\nIt's still pretty rough  just a first draft, really. But with more refinement, I genuinely think this system could scale to $20,000 a month. Of course, it hasn't been all smooth sailing. In the process of getting this to full automation, I got one account banned. But more on that later.\n\nIn this artic"]
rights_note: Public source evidence retained for research provenance. retrieved 2026-07-12T12:00:00Z; preserved at research/social/raw/x/2034730013283512381.json.
---
# I Used Claude Code to Run Threads on Full Autopilot and Made $200 While I Slept

## Complete source text

So I had Claude Code running a Threads account completely automatically. Two weeks later, it had generated $200 in affiliate revenue. And honestly? My first reaction was: "Is it really this easy?"

It's still pretty rough  just a first draft, really. But with more refinement, I genuinely think this system could scale to $20,000 a month. Of course, it hasn't been all smooth sailing. In the process of getting this to full automation, I got one account banned. But more on that later.

In this article, I'm going to lay out everything transparently:

The system architecture I built

How I'm monetizing it

What each AI agent is doing

Why Threads?

Simple: Threads is the easiest platform to automate. (Also  I've made about $1.3M on Threads personally, I run 7 accounts with over 10k followers each, and my total follower count has crossed 150k. Threads is just my thing.)

On X, you need an established following to get any reach. Instagram demands Reels. TikTok requires video editing. But Threads? You can go viral with zero followers, just text.

One of my students gained 10,000 followers in a single day. Another hit 50,000 in a week. The algorithm actively pushes content to people outside your followers, so new accounts can actually grow.

And text-only means AI compatibility is insane. No images. No video. Just text  which is exactly what AI does best. "Research to post, fully automated" is most feasible on Threads. That's why it was the only choice.

What Is Claude Code?

Claude Code is an AI that runs inside your terminal. Unlike a regular chatbot that just returns answers, Claude Code actually does things. File operations, running commands, browser automation all of it.

You say "do this," and it does it. Writes code, runs it, hits an error, fixes itself, runs it again. Completely autonomous. And because it runs in the terminal, it connects to shell scripts, cron jobs, and every other existing automation tool. That's what makes it powerful.

The 6 AI Agents and What They Do

I'm running a career/job-hunting Threads account on full autopilot, with 6 AI agents each handling a distinct role.

The reason I split into 6 agents is simple: if you make one AI do everything, quality degrades. Researching while writing while analyzing something breaks. One agent, one job. Just like a company you wouldn't make one person handle sales, accounting, and engineering.

Agent ① Researcher - Content Sourcing

This agent automatically pulls fresh content ideas from YouTube and X. For a job-hunting account, it searches keywords like "why people fail interviews" or "salary negotiation mistakes," reads transcripts of relevant videos, extracts usable angles, and outputs them as structured JSON.

The key is a "theme tree" I built in advance  major categories like Interview Strategy, Salary Negotiation, Recruiter Tactics, Job Search Prep, each with subtopics hanging below. The Researcher looks at this tree, figures out which themes are running low on content, and focuses on filling those gaps. No human needed to decide "what should I research next?"

Agent ② Analyst - Performance Analysis

This agent reviews past post data  views, likes, replies pulled from the Threads API  and figures out what worked and what didn't. "This format tends to go viral." "This topic isn't getting traction anymore."

Here's the interesting part: it writes its analysis directly as instructions for the Writer. "Bold, declarative openers have been performing well lately  weight toward those in the next batch." "Recruiter-bashing content is getting stale  back off for now."

AI giving feedback to AI. A loop that runs without any human involvement.

Agent ③ Writer - Post Generation

This is the main engine. It reads the Researcher's content and the Analyst's feedback, then produces actual posts  5 to 10 per batch. But it doesn't just generate anything. It follows strict rules:

15+ post formats: Short-form, comment-bait, thread-style. Each subdivided further confessional, demand-test, list-based, etc. The Writer avoids whichever 3 formats were used most recently and auto-rotates.

Opening line library: I have 265+ opening lines from high-performing posts stored and referenced. The Writer studies the structure, then adapts it to the current topic. The first line is everything.

Self-scoring: After writing, it scores itself on 10 criteria hook strength, usefulness, specificity, rhythm, persona alignment 10 points each. If the average is below 7.0, it rewrites. Two failed rewrites and the post is rejected entirely.

Similarity check: Compared against the last 100 posts. Too similar? Rejected. Without this, you'll end up in hell. (More on that later.)

Agent ④ Poster - Publishing

Takes posts from the queue and publishes them via the Threads API. Cron-scheduled across 10 time slots - from 8 AM to 1 AM, roughly every 2 hours.

But it's not just posting. Behavior changes by post type. Comment-bait posts get an automated follow-up comment from the account itself. Thread-style posts link up as replies. Affiliate posts auto-place PR links in the comments. All of it, automatic.

Agent ⑤ Fetcher - Data Collection

About 24 hours after each post, this agent pulls metrics from the Threads API  views, likes, replies  and appends them to the post history. Without this, the Analyst has nothing to analyze. Low-key, but critical. No data, no improvement loop.

Agent ⑥ Supervisor - Monitoring

Watches for anomalies across the whole system. Three consecutive errors triggers an automatic shutdown. If posts aren't going out on schedule, it sends a notification. There's also a KILL_SWITCH  a single command to immediately halt all posting across all accounts, just in case.

How the Whole Thing Runs Daily

I run a single shell script in the morning. The Fetcher grabs yesterday's data. The Analyst runs its analysis. The Researcher tops up the content library. The Writer produces 10 posts. The Poster distributes them via cron throughout the day.

Monetization is affiliate marketing ASP-style. I considered selling my own products or notes, but affiliate is just easier. No product creation needed. Posts are regular helpful content, with PR links quietly placed in the comments. Writer and Poster handle that automatically.

4 Design Principles I Kept in Mind

① Agent Separation

One agent, one task. Non-negotiable. Mixing responsibilities degrades quality.

② Separate Knowledge from Logic

Tone of voice, banned words, post formats, persona info all stored in external files. The code has no hardcoded personality. Swap the knowledge file, and the same system runs for any niche: career, beauty, parenting, whatever. Adding a new account means copying the template and filling in the knowledge file.

③ State Management

Post history, queue, audience analysis  all tracked in JSON. The AI "remembers" what was posted yesterday, which topics are gaining traction, and what questions are showing up in comments. Without this, context resets and you get infinite loops of the same post.

④ Safety Guardrails

Quality score below 7.0 → auto-rejected. Similarity above 0.85 → rejected. Max 15 posts per day. Minimum 1-hour gap between posts. Emergency kill switch. "Delegating to AI" and "abandoning AI" are completely different things.

Disaster #1: 10 Posts in 1 Minute → Account Banned

Disaster #2: The Same Post, 30 Times in a Row

The fix was everything described in the Writer section  similarity checks, pattern rotation across 15+ formats, mandatory theme cycling every 3 posts.

Where Things Stand Now

After two disasters, the current setup:

3 accounts running in parallel (career, beauty, parenting/lifestyle, SNS strategy)

Swap the knowledge file, change the niche instantly

Automatic quality scoring anything below 7.0 gets rejected

Buzz-pivot: 3 follow-up posts auto-generated from any viral post

Comment and reaction analysis feeds directly into next post topics

Kill switch for immediate shutdown across all accounts

The only thing I do is make strategic decisions. "This account should go in this direction." "Add this type of content to the knowledge base." High-level calls, nothing else.

Writing, scheduling, quality control, performance analysis, iteration  all AI.

That's $200 from one account. What happens when the content quality improves? What happens when I run 10 accounts?

That's the game now.

The Future of Social Media Is Probably Here

I'll be straight: I believe the future of social media management is "AI handles the work, humans make the decisions."

Coming up with post ideas every day, writing them, publishing, checking numbers, iterating  the era of humans doing all of that is over. At least for me it is.

What humans should do: decide who you're trying to reach, what you want to say, and why it matters. Set the direction. Build the knowledge base. Think strategically.

Let AI handle the rest.

The $200 while sleeping is just step one of that experiment. It's far from perfect. But I'm not wrong about the direction.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
