---
schema_version: 1
platform: youtube
stable_id: EN7frwQIbKc
title: "How To Build A Company With AI From The Ground Up"
publisher: "Y Combinator"
canonical_url: https://www.youtube.com/watch?v=EN7frwQIbKc
published_date: 2026-04-24
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube captions retained from the original repository seed"
rights_status: third-party
rights_holder: "Y Combinator"
content_sha256: 60f46320599df96af85b1e2aa2e1109e9ed57444eb01208db3929a872ef5e600
duration_seconds: 627
transcript_source: youtube captions
---

# How To Build A Company With AI From The Ground Up

0:09 Hi, I'm Diana and I'm a partner at YC.
0:12 Over the past few months, it's become
0:14 clear to me that AI is not just going to
0:16 change how quickly software gets built
0:19 or what workflows get automated. It's
0:21 going to fundamentally change the way
0:22 startups should be run from what roles
0:25 it will exist to what products are
0:27 possible to build. In this episode, I'm
0:29 going to discuss how founders should
0:31 think about building an AI native
0:33 company. What roles their team should
0:35 have and what concrete internal
0:37 practices they can adopt right now to
0:39 move much faster. Currently, most people
0:41 talk about AI in terms of productivity.
0:44 They'll talk at length about how it can
0:46 make engineers more productive or say we
0:48 need to add copilot to existing
0:50 workflows and ship more features. This
0:53 framing misses the shift we're currently
0:56 seeing which is less about productivity
0:58 boost than entirely new capabilities.
1:01 The right person with AI tools can now
1:03 build features that used to require an
1:05 entire team or were just impossible.
1:08 Thinking about AI in terms of new
1:10 capabilities has several implications
1:12 for how founders should run their
1:14 companies. At a high level, the way to
1:16 think about AI is that it should not be
1:19 a tool your company just uses. It should
1:22 be the operating system your company
1:25 runs on. Every workflow, every decision,
1:28 and every process should flow through an
1:30 intelligent layer that is constantly
1:32 learning and improving. What this means
1:35 concretely is every important process in
1:37 your company should be captured by an
1:39 intelligent closed loop. A closed loop
1:41 captures information, feeds it back into
1:43 an intelligent systems, and improves the
1:45 process over time. If you've ever
1:47 studied control systems, you'll be
1:49 familiar with the difference between an
1:51 open loop and a closed loop system. Open
1:53 loops are control systems without
1:55 feedback loops. In the old world,
1:57 companies basically ran as open loops.
2:00 You made a decision, executed it, and
2:02 didn't always systematically measure the
2:05 outcome, and adjust the process.
2:07 Open loops are inherently lossy. A
2:10 closed loop, on the other hand, is
2:11 self-regulating.
2:13 It continuously monitors its output and
2:15 adjust its process to better meet the
2:18 stated goal. Closed loops are extremely
2:20 powerful for correctness and stability.
2:22 With self-improving agents, your company
2:24 should run as a closed loop. To build
2:26 these closed loops, you will need to
2:28 make your entire company queryable. In
2:32 other words, the whole organization
2:33 should be legible to AI. Every important
2:36 action should produce an artifact that
2:38 the intelligence at the center of the
2:40 company can learn from and use to
2:42 self-improve.
2:44 This means recording your meetings with
2:46 an AI note-taker, minimizing DMs and
2:48 emails, and embedding agents throughout
2:50 communication of all channels. It also
2:52 means building custom dashboards with
2:54 everything in the company: revenue,
2:56 sales, engineering, hiring, ops,
2:59 everything. Here's a concrete example of
3:01 how it could work. Take engineering
3:03 management and sprint planning. If you
3:05 have an agent that has access to your
3:08 linear tickets, all your Slack
3:09 engineering channels, all customer
3:11 feedback from emails or tools like Pylon
3:14 and GitHub, high-level plans in a Notion
3:16 or Google Doc, sales calls and
3:18 recordings from daily stand-ups, then
3:21 the agent can analyze what was actually
3:23 shipped in your previous sprint and how
3:26 well they met customers' needs for real.
3:29 From there, you can go a step further.
3:31 With full visibility into what shipped,
3:34 what worked, and what didn't, agents can
3:36 start looking ahead. They can propose
3:38 sprint plans for engineers that are way
3:40 more predictable and accurate and on
3:42 track. The days of eng manager status
3:44 roll-ups that are super lossy are gone.
3:47 Having managed engineering teams myself,
3:49 and now seeing this across multiple YC
3:52 companies. This is a game changer. What
3:55 used to require constant coordination
3:58 becomes legible and queryable by
4:00 default. I've seen teams that do this
4:03 cut their engineering sprint time in
4:04 half and get close to 10x more done in
4:08 that time. The overarching principle
4:10 here is that to get their full
4:12 capabilities, you need to provide models
4:14 with as much context as you would
4:16 provide an employee. When you do this,
4:18 your company stops operating as an open
4:20 loop where information is fragmented and
4:22 manually interpreted. It becomes instead
4:25 a closed-loop system. Status, decisions,
4:28 and outcomes are continuously captured
4:30 and fed back into this intelligence
4:32 layer. The result is a system that
4:34 always has an up-to-date view of what's
4:37 actually happening. There's also a new
4:40 paradigm emerging for how the highest
4:42 velocity companies build product.
4:45 AI software factories. If you're
4:48 familiar with the test-driven
4:50 development or TDD,
4:51 this is the next evolution of that. With
4:54 software factories, humans write a spec
4:57 and a set of tests that define success.
5:00 And then AI agents generate the
5:03 implementation
5:04 and code and iterate until the test
5:07 pass.
5:09 The human defines what to build and
5:10 judges the output. The actual code is
5:13 the agent's job. Some companies have
5:15 already pushed this to the point where
5:17 the repos contain no hand-written code,
5:21 just specs and test harnesses.
5:24 Strong DM's EI team is an example of how
5:27 to do this. Their end goal was a system
5:29 that essentially eliminated the need for
5:31 a human to write or review code. And so,
5:35 they built their own software factory
5:37 where specs and a scenario-based
5:38 validations drive agents to write, test,
5:41 and iterate on code until it meets a
5:44 probabilistic satisfaction threshold.
5:46 And it works. This is how you achieve
5:49 the 1000 X engineer that Steve Yegge
5:52 talked about by surrounding a single
5:55 engineer with a system of agents that
5:57 enable them to build things they would
5:59 have never been able to build before.
6:02 The era of the 1000 or even 10,000 X
6:06 engineer is here. One implication of
6:08 building your company this way with AI
6:10 loops everywhere, a queryable
6:12 organization and software factories, is
6:14 that the classic management hierarchy no
6:16 longer makes sense. In the old world,
6:19 you needed middle managers and
6:20 coordinators to route information
6:23 inefficiently up and down an
6:25 organization.
6:27 In the new world, the intelligence layer
6:29 serves that purpose. If your company is
6:32 queryable, artifact-rich, and legible to
6:35 an AI, you should have almost no human
6:39 middleware. This matters because your
6:41 company's velocity is only as fast as
6:44 its information flow.
6:46 Every layer of human routing you can
6:48 remove is a direct speed gain.
6:52 A great example is what Jack Dorsey is
6:54 doing over at Block. After going deep on
6:57 the tools, he's come to the same
6:59 conclusion many have.
7:01 This is about more than just incremental
7:04 productivity gains. His view is that if
7:06 you keep the same org chart and
7:08 management structure, you'd miss the
7:10 shift entirely. The company itself has
7:12 to be rebuilt as an intelligence layer
7:15 with humans at the edge guiding it
7:16 rather than routing information through
7:18 it. Going forward, Jack suggests every
7:21 company will have three employee
7:23 archetypes. The first is the individual
7:25 contributor or IC. Basically, the
7:27 builder operator. This is someone who
7:29 directly makes and runs things. In an
7:32 AI-native company, this is not limited
7:34 to engineers. Everyone builds.
7:37 Eng, ops, support, sales.
7:40 Everyone comes to meetings with working
7:42 prototypes, not pitch decks. Second, is
7:45 the DRI, the directly responsible
7:47 individual. Focus on strategy and
7:50 customer outcomes. This is not a classic
7:52 manager, is the person with a clear
7:54 responsibility for the result. One
7:57 person, one outcome, no hiding. The
7:59 third is the AI founder type. This
8:02 person still builds, still coaches and
8:05 leads by example. If you're the founder,
8:08 this needs to be you at the forefront.
8:10 Showing your team what massive
8:12 capability gains look like, not
8:14 delegating your AI strategy to someone
8:16 else. With this structure, companies
8:19 will be able to get outsized results
8:21 with much smaller teams. Maximizing
8:23 token usage, not headcount, will be the
8:26 critical shift. The best companies will
8:28 be the ones that are token maxing. Think
8:30 of the trade-off this way. One person
8:32 with AI tools can be the equivalent of
8:35 what used to take a large engineering
8:37 team at a pre-AI company. That means
8:40 dramatically leaner engineering, design,
8:43 HR, and admin teams. And so, you should
8:46 be willing to run an uncomfortably high
8:48 API bill. Because it's replacing what
8:51 would have taken a far more expensive
8:53 and inflated headcount. But,
8:56 don't just take my word for any of this.
8:59 You cannot outsource your conviction on
9:01 the power of these tools. You need to
9:04 develop it yourself by actually sitting
9:06 with coding agents and using them until
9:08 you start to break your own priors about
9:10 what is now possible to build. If you
9:12 are an early-stage founder, you have a
9:14 huge advantage in getting ahead on this.
9:17 You don't have legacy systems,
9:19 entrenched org charts, or thousands of
9:20 people to retrain. You are small enough
9:22 to build your company right from day
9:25 one. The opposite is the case for
9:27 existing companies. They have to
9:29 maintain and grow a live product while
9:32 unwinding years of standard operating
9:35 procedures and core assumptions about
9:37 how software gets built. Some companies
9:39 can achieve this by spinning up small
9:41 internal skunkworks teams that can build
9:43 AI native systems from scratch, separate
9:45 from the core business. Mutiny is a
9:47 great example of this. But, for most,
9:50 every change to their core processes
9:52 risk breaking something that already
9:54 works. So, by their nature, these large
9:57 companies will have a much harder time
10:00 going AI native. Startups don't have
10:03 that constraint,
10:05 and that's a major edge to take
10:06 advantage of.
10:07 You can design your systems, workflows,
10:09 and culture around AI from the start,
10:12 and as a result, operate 1,000 times
10:15 faster than the incumbents.
