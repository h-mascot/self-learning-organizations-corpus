---
schema_version: 1
platform: youtube
stable_id: B246K_G7mHU
title: "Inside YC's AI Playbook"
publisher: "Y Combinator"
canonical_url: https://www.youtube.com/watch?v=B246K_G7mHU
published_date: 2026-05-27
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via legacy-youtube-captions"
rights_status: third-party
rights_holder: "Y Combinator"
content_sha256: 9d439e50cb6fe35ded44e207bae53e236ca6d3cb7786b322839d5d4a0807a7e3
duration_seconds: 2790
transcript_source: legacy-youtube-captions
availability: public-at-ingestion
license: null
caption_error: null
segment_count: 1318
relevance_categories: ["ai-native-company","agent-operations","named-lanes"]
relevance_evidence: ["agents","ai native","ai-native","ramp","y combinator"]
relevance_spans: [{"category":"ai-native-company","phrase":"ai native","text":"how to build that AI native","timestamp":"25:14"},{"category":"ai-native-company","phrase":"ai-native","text":"how to build AI-native companies that","timestamp":"1:19"},{"category":"agent-operations","phrase":"agents","text":"for kind of YC specific agents","timestamp":"2:50"},{"category":"named-lanes","phrase":"ramp","text":"it could just like trample on anything?","timestamp":"6:50"},{"category":"named-lanes","phrase":"y combinator","text":"again. Y Combinator Startup School is","timestamp":"18:05"}]
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"legacy-transcript.md":"6b168ddae88ee6297fbe8a1132ca960b2a779a844e16bfb700fb3087bcf38162","source-info.json":"7fa05795db9e202664b5c9ec38a03e70e1a64e7dc7f32e5cc7a08dd02ac433a7"}
raw_path: raw/youtube/2026-05-27--inside-yc-s-ai-playbook--y-combinator--B246K_G7mHU
---

# Inside YC's AI Playbook

0:00 How do you build superintelligence
0:01 inside a company? Part of the key thing
0:03 is not to just use AI as a co-pilot.
0:06 This is the the thing where you use it
0:09 as the building layer for everything.
0:11 And you need to start recording all the
0:13 artifacts. It's like a shared
0:15 organizational brain. It's like the
0:17 closest thing to us being able to like
0:18 connect our brains.
0:19 >> If you frame this as a way for everyone
0:21 in an organization to get better at what
0:24 they do using the like collective skill
0:27 and instinct of the people they work
0:29 with, it's incredibly powerful.
0:39 Today we have a real treat.
0:41 Uh we have a special guest, general
0:43 partner at YC, our partner,
0:46 Pete Koomen. He created Optimizely,
0:48 which was one of the first and one of
0:50 the best ways to do AB testing for apps
0:53 and websites. And since then, he has
0:56 gone on to create all of our agent
0:59 infrastructure at YC. So literally all
1:01 of our harnesses and how we use AI
1:04 internal to YC. Pete, welcome to the
1:07 Light Code.
1:07 >> Thanks, Garry. For the last few years
1:09 since ChatGPT, YC has been funding
1:12 mainly AI companies. And we've been
1:14 we've gone through like many different
1:16 like versions of advice for them about
1:19 how to build AI-native companies that
1:20 build like mainly AI
1:22 products. And we've
1:24 gone on a crazy journey with them
1:26 learning all of this. I think a lot of
1:27 people don't realize that internally YC
1:31 is actually building and using a lot of
1:33 the same stuff that we're helping our
1:35 startups build and use themselves. And
1:38 it's been I think a very powerful
1:41 symbiotic relationship for us to
1:42 actually be adopting these tools and
1:44 like transforming our own organization,
1:47 which was started way way pre-AI into a
1:49 super AI-native organization ourselves.
1:52 And Pete has really been leading the
1:53 charge for that. And so I'm really
1:56 excited about this episode because I've
1:57 actually been wanting to talk publicly
1:59 about all the stuff that we built
2:00 internally and this is the first thing
2:01 that we're doing it. So, Pete, perhaps
2:03 to start off, you sort of go back to the
2:05 beginning and like talk about like there
2:07 was a particular like moment when we
2:09 really started adopting these AI tools
2:12 internally. It was really you who got us
2:14 started down that path.
2:15 >> Sure. I'm happy to happy to tell the
2:17 story here and it's I like framing it
2:19 that way because it was a project that I
2:23 and a few engineers got started about a
2:25 year ago, maybe a little more, but that
2:27 has since snowballed into just a whole
2:29 infrastructure layer that's made it
2:31 possible for us to use AI internally at
2:33 YC in lots of different ways. And And
2:35 that's actually been one of the neatest
2:36 parts about this is watching the whole
2:39 engineering team and and many partners
2:41 also just dive in and contribute to this
2:44 this infrastructure layer. We started
2:46 building our own harness inside of YC
2:50 for kind of YC specific agents
2:53 about a year ago. And
2:55 uh the original impetus for the project
2:58 was some of the work that I and a and a
3:01 few of the software engineers at YC were
3:03 doing with our finance team. Just for a
3:05 bit a bit of backstory, so YC has for as
3:08 long as it's existed, as far as I'm
3:09 aware, run mostly on our own software.
3:12 And this era has just given us a huge
3:15 advantage, right? And so, with that
3:17 context, back to this this moment, maybe
3:19 a year ago, we were sitting down with
3:21 the finance team talking through a set
3:24 of tools that we were going to build for
3:27 them uh just to help them run through
3:29 some of their finance workflows. Booking
3:31 journal entries, uh logging priced
3:33 rounds, like all the sorts of things
3:35 that that make YC run, really. I was
3:38 seeing kind of two things at once. Like
3:40 on one hand, uh we, you know, we had
3:43 this sort of loop going internally,
3:45 right? Where we'd sit down with the
3:46 finance team, the finance team would
3:48 describe to our software engineers how,
3:51 you know, this complicated financial
3:53 workflow worked and then software
3:54 engineers would go and build some
3:56 purpose-built software where there was a
3:58 deterministic workflow encapsulating
4:00 everything that they had been told and
4:02 then hand it back to the finance team
4:03 and so on. And it felt really
4:05 inefficient. And then at the same time,
4:07 this was right around the time when
4:09 agentic tools were really agentic coding
4:11 tools were really catching hold, right?
4:13 And so you had uh kind of the first
4:16 generation uh Windsurf and Cursor that
4:18 were well-established by this point. I
4:20 think this is right around when Claude
4:21 Code was was introduced. It felt like
4:23 this was giving me superpowers, right?
4:26 Um and then kind of watching this sort
4:27 of old classical way of building
4:29 software in YC and then watching how I
4:31 was doing things on my own machine, this
4:33 it just felt like a bigger and bigger
4:35 divide between those things. And so the
4:37 original impetus was, "Why don't we try
4:40 to build some tools at YC that we could
4:42 use to run agents that would give the
4:44 finance team control over their own
4:47 software, right? Like remove the
4:49 software engineers from this crazy loop
4:51 where they have to sort of understand
4:53 these complicated workflows and give the
4:55 finance team the tools that they could
4:57 use to encode their own workflows, not
4:59 not as, you know, not as Ruby, uh but as
5:02 as English with prompts, right?"
5:03 >> I mean, what's interesting is like uh we
5:06 all funded companies like maybe even
5:08 like two or three years ago when LLMs
5:10 were out, but like agentic coding wasn't
5:12 the thing yet. And so the first thing
5:14 actually was not agentic coding, it was
5:16 LLMs for writing SQL queries.
5:18 >> Yes.
5:19 >> So that's what I remember from like the
5:20 first versions of what you built was uh
5:22 how like good it was and how basically
5:26 it rhymed with like these other failed
5:28 startups that we had funded like each of
5:30 us probably funded one at some point,
5:33 you know, here it was, it was working
5:34 and it worked so well that non-technical
5:36 people, uh granted very smart people
5:39 from finance, but with no engineering
5:41 background, could use these tools to ask
5:43 real questions. I I really surprised,
5:45 too, to be honest. And and so that we
5:48 started with this kind of purpose-built
5:50 thing for finance and then rewrote it to
5:52 be more of a general agent loop, right?
5:55 And it and it's this is now you see
5:57 these all over the place now, but
5:59 I the first kind of magical moment that
6:01 I had was we had this agent loop and we
6:04 had a tool registry, a shared tool
6:06 registry for kind of YC specific tools.
6:08 And the first tool that really was an
6:11 unlock for me was I think a tool looking
6:13 back that you actually built, Jared. It
6:16 gave these agents the ability to run
6:18 read-only SQL queries against our
6:20 database.
6:21 >> Right? It was two tools actually. One
6:23 was was running queries against our
6:25 database and the other one was the
6:27 ability to read our model files. I
6:29 remember I built those tools and I felt
6:31 a little bit like I was breaking the
6:33 rules cuz initially we started with very
6:37 limited tools that had very
6:40 narrowly scoped domains and I kept
6:42 getting frustrated because they weren't
6:43 powerful enough to do the things that I
6:45 wanted. And so I was like, what if we
6:46 just gave the thing like access complete
6:49 access to the production database where
6:50 it could just like trample on anything?
6:53 >> [laughter]
6:54 >> And I started to like
6:56 surreptitiously pushed it out maybe late
6:58 at night. And it worked. And it worked,
7:00 yeah. It worked extremely well, right?
7:02 >> Yeah, perhaps foreshadowing, you know,
7:04 subsequent things like open claw where
7:06 it turns out that like the thing that
7:08 was hampering the world was being
7:10 worried about security and privacy and
7:11 all the things that could go wrong. And
7:13 when you like worry a bit less, you're
7:15 like, "Oh my god, these things are
7:16 unbelievably powerful." It's it's
7:17 another really good example of this
7:19 weird split between I'm at work and I'm
7:22 kind of operating in this really narrow
7:24 box and I'm at home using Claude coder
7:27 or whatever like open claw hermie and I
7:30 can do anything, right? And and and
7:32 trying to trying to narrow that gap. So
7:35 why was this so useful? This ability to
7:37 run SQL queries against our database. It
7:39 sounds really simple. Well, I think this
7:41 is where it's important to talk about
7:42 one of the big advantages that I think
7:44 YC had coming into this experiment uh
7:47 which is that we run on our own software
7:49 and all of that software sits on one
7:52 Postgres database that has everything
7:55 that's important to YC's world in it.
7:57 You know, every company that we funded,
7:59 there's a company's table, there's a
8:01 there's a founder's table, right?
8:02 There's tables for our financial
8:05 transactions, there's tables for the
8:06 notes that I leave in our little
8:08 internal CRM, right? All of these
8:10 functions that I think a lot of other
8:11 companies farm out to third-party SaaS
8:14 tools, we've built our own. And as a
8:16 result, we have this database with every
8:18 important piece of context that I can
8:21 now ask questions like, "Hey, show me
8:23 all of the investors who invested in a
8:26 space-related company in the last four
8:28 batches." Right? It just turns out when
8:30 when all of that context is in one place
8:32 with a little bit of additional
8:34 uh information about how the schema is
8:35 laid out, an agent can go and ask any or
8:38 answer arbitrary questions about about
8:40 our business.
8:41 >> That was a magic moment for sure when I
8:42 first saw that.
8:43 >> Yeah. The cool thing for me is that it
8:45 didn't just make it easier to answer
8:47 questions, it
8:49 dramatically increased the number of
8:50 questions that we would ask and
8:52 dramatically increased the the scale and
8:53 complexity of the questions that we
8:55 would dare to ask. Where like, you know,
8:57 in the in the old days back when we were
8:58 using like BI tools
9:00 to ask to ask a question like that, you
9:02 know, like, "What investors have
9:04 invested like in space-related
9:05 companies?" That would be like several
9:06 hours of writing SQL. And so like,
9:08 unless it was really important, you just
9:09 wouldn't bother. It's just example of
9:12 the you know, the this instance of
9:14 Jevons paradox that you get when you
9:17 remove the amount of back and forth uh
9:19 between different teams in order to get
9:21 a thing done, right? If if in order to
9:23 ans- ask some kind of complex question
9:25 about YC, I have to go and knock on on,
9:29 you know, the data science team's door
9:31 and wait for them to get it through, you
9:32 know, their backlog, uh I'm just going
9:34 to ask far fewer questions. I mean,
9:36 there are people out there watching this
9:38 who work in places that still use it.
9:40 The majority of people live in that
9:42 world still, and it's 2026, which is a
9:44 little
9:45 unfathomable, actually. There's a long
9:47 way to go, I think, which is which is
9:49 really exciting. My guess is one
9:50 question is how do companies that live
9:52 in that old world could
9:54 get sort of wings to move so quickly?
9:57 Because our the magic for us was as you
9:58 said, everything was the context is in
10:01 one place that made it easy. You know,
10:03 if you think about um
10:05 data science uh historically, one of the
10:07 first things that the Googlers had to
10:09 figure out was a big table, right? And
10:11 big table was, you know, instead of
10:13 schema you and joins, you have one big
10:17 table that um can be map reduced. Yes.
10:20 And so, I think that that's happening
10:22 again, and I would argue that that's
10:24 happening now with um
10:25 Karpathy style knowledge LLM wikis uh
10:30 with Gbrain.
10:31 >> [laughter]
10:32 >> I mean, that's what I'm seeing anyway.
10:33 Like, you know, obviously I have I have
10:34 an Open Claw. It has uh access to lots
10:37 of lots of systems, and then I'm
10:39 normalizing it to my own schema that's
10:42 relevant to me and the things that I
10:43 care about. And it is like
10:45 denormalization. It's you're taking data
10:47 and you're putting it into a format that
10:49 uh is more or less optimized for Open
10:52 Claw or Hermes agent. Like, that
10:54 particular type of harness to be able to
10:55 ask questions. And it needs retrieval,
10:57 it needs rag, it needs graph rag, it
10:59 needs uh you know, hybrid RRF. Like,
11:02 there's reranking in there. Like, you
11:04 know, all the things that everyone has
11:05 learned about retrieval uh is now inside
11:07 Gbrain. And then, when you give the
11:10 agents a soul,
11:12 and it and you give it uh the data, and
11:15 it knows you and what you care about,
11:16 like suddenly these things have insane
11:19 wings. Like, I just kind of can't
11:21 believe how it sees around corners. And
11:24 you might ask a question, and it'll even
11:27 you sort of interpret what your question
11:29 was about, and like give you a thing
11:31 that uh frankly like it would take a
11:33 human who really knows you well
11:35 to answer.
11:36 Um all that's possible now. And so, you
11:39 know, your question is like all the data
11:40 is everywhere. My answer from like the
11:43 Open Claw Hermes experience with G brain
11:44 is like, yeah, you basically have to
11:46 take that you're going to denormalize it
11:48 and you're going to put it in a format
11:49 that is optimized for agent retrieval
11:52 and understanding. You could wrap it in
11:54 an MCP, but for whatever reason I just
11:57 like intuitively I'd be worried like
12:00 it's still so you know, these things are
12:02 really good at working with MCP and CLI.
12:04 Like they're a little even better with
12:05 CLI. It seems like you have to
12:07 denormalize and do the big table thing,
12:09 but you know, specifically for the
12:11 agent. Looking back over the the last
12:13 year and a half,
12:14 uh it feels like we're still kind of in
12:16 the single player era of agents where
12:19 the harnesses that have gotten really
12:20 popular, right? Uh Claude Code, Codex,
12:24 Pi, Open Claw, Hermes. They're all
12:27 designed to be used by a single human
12:29 running on a single machine. And it
12:32 makes a lot of sense.
12:34 Right? Because in that environment these
12:36 these agents can do just about anything,
12:38 right? And they they make you incredibly
12:40 powerful. It's it's they're a lot of fun
12:42 to use. I think one of the big problems
12:44 uh that I don't think has been solved
12:46 well yet by anybody is the multiplayer
12:49 Mhm. harness, right? It's it's enabling
12:51 that kind of superpower but on a team or
12:54 an organizational level, right? And and
12:57 and that's I think
12:58 been the interesting thing to explore
13:00 with the infrastructure that we've built
13:01 at YC is watching which primitives that
13:05 we've created that have enabled
13:07 individuals and teams to use agents. You
13:10 asked the question about if you're
13:12 working inside of a kind of a legacy
13:14 organization, which is like anyone who's
13:15 more than two years old,
13:17 >> [laughter]
13:18 >> uh what are the things that you can
13:19 focus on uh in order to to help enable
13:22 everybody at your org to use AI to to to
13:25 more. Uh and
13:27 we talked about kind of this common
13:28 context layer, right? And so, a data
13:31 warehouse where it just as much of your
13:33 internal important context lives, it
13:36 just turns out is extremely useful.
13:38 There are many tools for connecting
13:39 individual agent harnesses to uh you
13:43 know, other MCP tools, other other
13:45 sources of truth. But just like
13:48 a coding agent inside a mono repo just
13:50 tends to be much more efficient,
13:52 watching our agents operating on our
13:56 single database that has everything in
13:58 one schema tells me that there's a lot
14:00 of value at least in getting all of the
14:02 context into one place. Having an
14:05 internal tool registry, this is I think
14:07 the other really important thing that we
14:08 built. So, in the beginning, like we
14:10 were talking about, it was just the
14:12 whole system was really simple. It was
14:13 like an agent loop and a simple tool
14:16 registry and you know, a few other
14:18 pieces, right? Like a model router
14:19 underneath. The tool registry is where
14:22 most of the like YC specific
14:25 stuff lives, right? Like tool registry
14:27 is what turns these agents into
14:29 something that's useful at work. And we
14:31 had like 20 tools at the beginning
14:33 including this magical ability to query
14:35 our SQL database, but over time teams
14:38 have added more and more tools. Every
14:40 time we kind of come upon some piece of
14:42 work at YC that we think could be
14:45 improved with an agent, we can just add
14:47 tools and there's more than 350 today. I
14:49 just checked, right? Every team is
14:51 adding their own tools. You know, I can
14:53 do things like manage my office hours.
14:55 Our finance team can
14:57 uh you know, can book journal entries,
14:58 right? We can help manage the events
15:00 that we run. Uh there's tools for all of
15:02 the important work that we do at YC. And
15:04 now, once these all exist in in in in
15:07 one place, you can make them available
15:09 to these internal agents that we built,
15:12 but you can also make them available to
15:14 cloud code, you know, running running on
15:16 on on on our individual machines. So,
15:18 those things above all, I think, were
15:19 the important pieces that we built that
15:22 if I were working in any other
15:24 organization I would focus on building.
15:26 I mean honestly inspired by what you
15:27 guys did with tools like this idea of
15:29 skillify in open claw and then actually
15:32 the most important the last part of
15:34 skillify skillify is like this meta
15:36 skill that I made in open claw where
15:38 it's like you just do anything in
15:40 open claw and Hermes. Hermes actually
15:42 already has skillify they call it
15:44 something as like it makes skills
15:45 automatically. But the most important
15:47 thing I I think is actually like
15:49 plugging into the resolver which is like
15:51 your agents.md with like the list of
15:53 things that the agents can do and then
15:56 like it links to the markdown entry
15:58 point that like lets you use a tool
16:00 basically. And so like this thing keeps
16:03 coming up in all these different
16:04 contexts like cloud code has a skill.
16:07 The skill registry in cloud code is
16:09 actually a resolver. Our tool registry
16:12 is actually a resolver. And then the
16:14 weird thing that you have to do on top
16:15 of that is actually um
16:17 I have a meta skill called check
16:19 resolvable that I call all the time. So
16:21 I'm always like I do something that's
16:23 new or different in
16:25 uh in my agent and then after it does it
16:28 and I like it I say skillify it and then
16:30 it becomes basically like a tool call or
16:32 method call and then I run check
16:34 resolvable which is like you know look
16:36 at all of the other skills and
16:38 tools that exist and is it you know dry
16:41 don't don't repeat yourself and is it
16:44 MECE which is you know I'm embarrassed
16:46 to say a McKinsey term for um
16:49 the consultants use it for making really
16:51 good slide decks mutually exclusive
16:54 collectively exhaustive. That's like how
16:56 you're supposed to do slides if you're a
16:58 McKinsey consultant but it's useful
17:01 because it's like an additional layer on
17:03 top of don't repeat yourself dry.
17:05 And like the models just seem to know
17:07 what those things are and so if you have
17:09 a dry and MECE resolver table anywhere
17:14 it's actually like the optimal resolver.
17:18 Like it's bad to have 10 skills that do
17:19 all the same thing. It's good to have
17:21 one skill or one tool that has
17:23 parameters that then let you call them.
17:26 So, I don't know. I think it's like this
17:28 is like the wildest time to be alive as
17:30 like an applied computer scientist cuz
17:32 it's like simultaneous like discovery of
17:35 the same useful applied concepts over
17:37 and over again. And I wonder if like
17:40 when people were, you know, developing
17:41 the first versions of Unix or something
17:43 is like discovering a stack and a
17:45 >> heaps. It feels like we're right at that
17:46 moment
17:47 >> Yeah. today. Like we're just coming up
17:48 with the new primitives for what an
17:50 agentic system actually is. And you can
17:53 see it in the parallel sort of
17:55 development of like we're just trying to
17:56 do a thing and it might be in cloud code
17:58 or it might be in our own internal
18:00 harness or it might be in open claw, it
18:02 might be in Hermes. Like these things
18:03 just keep coming back over and over
18:05 again. Y Combinator Startup School is
18:07 back. We're hand-selecting the most
18:09 promising builders in the world and
18:11 flying them out to San Francisco for
18:13 July 25th and 26th to discuss the
18:16 cutting edge of tech and startups. Apply
18:19 now for your spot. Yeah, it's really
18:21 interesting to look at how some of the
18:23 other companies that are building this
18:24 stuff
18:26 have built their infrastructure because
18:27 you see a lot of these same primitives
18:29 in in each of them, right? Like there's
18:31 the agent loops, there's tool
18:32 registries, there's skill registries.
18:34 Looking at at at the way that we're
18:36 using skills now YC, so if you think of
18:39 skill as a simple abstraction layer over
18:41 tools, we have a handful of sort of
18:44 shared skills uh that that we all have
18:47 access to uh through this through this
18:49 agent system. And it's been interesting
18:52 to watch. I think you've talked about
18:53 this where this progression of like in
18:55 the beginning you were kind of writing
18:56 your own system prompts and then skills
18:58 emerged, so you started writing your own
19:00 skills and then you would start uh meta
19:02 prompting where you where you know,
19:03 you'd do it again. Write a skill.
19:05 Exactly. Improve the prompt. Yes.
19:07 Automatically. Yeah.
19:08 >> Yes. Seeing us kind of do the same
19:09 progression internally where we have a
19:11 couple skills and now we've gotten to
19:13 the point where we have these sort of
19:16 autonomous self-improving loops, right?
19:18 Uh you know, and so uh
19:20 >> Auto research from Karpathy again, you
19:22 know, yeah. Or slash goal now in Codex.
19:24 Like they've they've incorporated it,
19:26 too. We have this general agent that
19:28 every night will go and read through all
19:30 of the agent conversations that
19:32 employees have had and look for uh
19:35 things it could have done better and
19:36 pieces of context that if it had up
19:39 front, it would have done more
19:40 efficiently. This is Open Crow's dream
19:42 cycle and G brain also has a dream
19:44 cycle. This is a um
19:46 a a skill improvement dream cycle, but
19:49 it could also potentially um
19:52 read all the transcripts and then write
19:55 them back into the internal
19:57 uh DB into the internal CRM on like what
20:00 we know about people and companies.
20:02 Indeed. And
20:03 we we there are cool examples of using
20:06 transcripts actually to make these
20:08 skills more effective as well. One of
20:10 the shared skills that we have uh is a
20:13 skill that that partners at YC use to
20:16 help our companies uh write what we call
20:19 two sentence descriptions, right?
20:20 Everybody here has written hundreds of
20:23 these.
20:23 >> We should probably explain what a two
20:24 two sentence description actually is,
20:26 yeah.
20:26 >> Sure. So, a two sentence description is
20:28 a concise way of explaining what your
20:30 company does in natural language that
20:32 anyone will understand and why it's
20:34 interesting. Sounds easy, but it's
20:36 surprisingly hard for founders to
20:37 actually And also no one does it.
20:39 Weirdly. Weirdly like even the most
20:40 experienced founders like forget because
20:43 they have perfect context.
20:45 Interestingly, uh I now realize YC
20:47 itself is uh a context engineering uh
20:51 sort of process in that like people we
20:54 would frequently teaching people, you
20:56 have perfect context about what's going
20:57 on in your brain, but great
20:59 communication is replicating that same
21:01 context in someone else's brain. And
21:04 that's what a two sentence pitch is.
21:05 Like what is it? Like I don't even know
21:07 what the heck this is. And then second
21:09 part is like, is it interesting or
21:11 valuable? What you know, is it worth my
21:13 time? And so that you know, when I when
21:15 I teach two sentence pitches, that's my
21:17 favorite way to do it. It's like, do I
21:19 even know what the heck this is? Because
21:21 if you don't know what it is, you can't
21:23 even ask a question about it. It's like,
21:25 something about computers, I guess,
21:26 whatever. What What time is lunch again?
21:29 And then the second part is equally
21:31 important, which is like, if I've heard
21:32 that you know, there are like 20
21:34 companies. Like, there are five other
21:36 companies in this room that do X. Like,
21:39 and then I don't understand like why
21:40 this is noteworthy. Like, again, I'm
21:42 like thinking about my pastrami sandwich
21:44 again, right? [laughter] So So the two
21:46 sentence pitch like viscerally is
21:48 important for founders. And it's it's a
21:51 it's a simple kind of atomic thing that
21:53 every partner at YC has
21:56 practiced over and over and over again.
21:58 I think Tom,
22:00 uh one of the one of the partners here,
22:02 wrote a skill that teaches an agent how
22:05 to
22:07 uh take some context about a company and
22:08 can and condense that into a two
22:10 sentence description. And so that was
22:12 his sort of handwritten prompt or skill
22:14 about how that was done. And one of the
22:17 cool things that happened in the last
22:18 month or two was that a couple of the
22:19 other partners took a meeting that they
22:23 had with a a group office hours they had
22:25 with a bunch of the companies in the
22:26 spring batch and just went through and
22:29 had every founder try their hand at at a
22:32 two sentence description and kind of
22:33 gave them feedback and input. And so
22:35 kind of the knowledge that lives in a
22:37 partner's head about how to do this
22:39 effectively was exchanged back and
22:42 forth, right? And and and now lived in
22:44 the context of of that meeting
22:47 transcript. And handing that back to the
22:49 agent and saying, given, you know, what
22:52 you've learned by reading through this
22:53 context, improve the two sentence
22:55 description skill. And they got
22:57 noticeably better after that. Like, this
22:59 thing is now better than I am, I would I
23:01 would argue at writing those. This is
23:03 how super intelligence happens inside
23:04 organizations. [laughter]
23:06 I mean, this two-sentence pitch thing
23:07 sounds like something kind of small, but
23:10 embedded in it is actually something
23:12 very powerful. I'm sure you guys have
23:14 heard Jack Dorsey talk about what he's
23:16 doing with Block. He basically is trying
23:18 to turn Block into a mini AGI around
23:22 helping people in the world make
23:23 payments to one another, right? Uh and
23:26 then this is actually
23:28 the micro mechanism by which he's going
23:31 to do that, right? Like you can look at
23:34 the operation of any organization as
23:37 the aggregate of you know, I mean, the
23:39 two-sentence pitch at YC is that's sort
23:41 of one of like thousands of things that
23:43 I would argue we do for founders.
23:46 But you know, we just walk through a
23:48 very concrete way where someone wrote a
23:50 prompt, used it, used a bunch more,
23:53 other people used it, a bunch of
23:55 artifacts came off of that around
23:57 literally like the transcript of using
23:59 it becomes a thing that can be used to
24:02 meta prompt and improve in an automated
24:04 fashion on a daily basis the operation
24:07 of that one skill. And then suddenly
24:10 that one skill, you just said it. That
24:12 skill is now better than any of us
24:13 individually
24:15 than be you know, when before we
24:16 actually had access to that. And so this
24:19 is like a particular like needle pin
24:22 prick in the fabric of like how any
24:24 organization does things. And then how
24:27 do you build super intelligence inside a
24:29 company? You do that on everything you
24:32 do. And it's not more complicated than
24:34 that. Like you literally just compose
24:35 everything that you do and any given
24:37 thing that any given person can do, you
24:40 combine that in aggregate and in this
24:43 particular process and like you have a
24:45 super organization. It's possible now.
24:48 Like every single person watching this
24:50 can do this at any company, at their own
24:52 company, they can do it at their job. I
24:54 mean, the interesting thing is that's
24:55 why you should start a startup Cuz
24:57 people are going to be trapped in
24:58 organizations with people running
25:01 organizations that are very powerful and
25:03 have all these resources and all this
25:04 capital that do not believe what we just
25:07 said.
25:07 >> Because they keep all the context locked
25:09 down.
25:09 >> Right, because it's unsafe. Unsafe. This
25:12 is one of those things that we talk
25:13 about um
25:14 how to build that AI native
25:15 organization, right? Part of the key
25:17 thing is not to do just use AI as a
25:20 co-pilot. I think that's very 2020
25:23 three, four, right?
25:25 This is the the thing where you use it
25:27 as a really
25:29 the the building layer for everything.
25:32 And you need to start recording all the
25:34 artifacts. Like people wouldn't have
25:36 thought of a meeting recordings and this
25:38 is one of those reasons why all these uh
25:40 meeting recorders have been taking off.
25:42 People have been finding them with
25:43 coaching them on the meetings, but it's
25:45 not just that. You could take that and
25:47 improve all the output for you
25:50 that you do, like writing emails,
25:52 communication, planning. You have the
25:55 whole context of everything. It's funny
25:56 to say I remember the Dario essay where
25:58 it's like there's some of the blockers
26:00 on just the rate of progression of AI
26:02 are not technical, they're just sort of
26:03 like social, cultural things. Things
26:05 kind of like a really interesting
26:06 example. Two years ago it would have
26:07 seemed to I just remember like it felt
26:09 odd to just like record a meeting or
26:11 like there was just like people trying
26:12 to figure out what the like social
26:13 etiquette around it was and like how
26:16 intrusive it was. And today I just feel
26:18 like it's almost like default assumed
26:20 that like most meetings are being
26:22 recorded, especially if they're on Zoom,
26:24 but just in general like everyone
26:25 started recording things now. It's a
26:27 little scary, but I think if you frame
26:29 this as a way for everyone in an
26:31 organization to get better at what they
26:33 do using the like collective skill and
26:37 instinct of of the people they work
26:39 with, it's incredibly powerful. Having a
26:43 canonical two-sentence description skill
26:45 is not just a way to like generate a a
26:48 snippet of text for a a
26:50 It's a way to help me get better at
26:52 understanding what makes for effective
26:55 founder communication, right? Because
26:56 now I can tap into everything that Diana
26:58 and Hardt and you two have learned over
27:01 the many years you've done this job,
27:02 which are now kind of baked into this
27:04 skill through the conversations that
27:06 you've had.
27:06 >> It's like a shared organizational brain.
27:08 Yes. It's like the the closest thing to
27:10 us being able to like connect our
27:11 brains, right? Yeah.
27:13 >> It totally is, right? And I I can have
27:14 an agent now come and I can do practice
27:17 sessions with it, right? I can have it
27:19 critique. Like there there are so many
27:21 possibilities once you get all of this
27:23 knowledge into a place where an agent
27:26 can can work with it. It's a It's a very
27:29 empowering thing for every human in the
27:31 organization. There's some subtle
27:32 interesting things around here that
27:33 like, you know, other people might get
27:35 wrong that like, I feel like we've
27:36 gotten right. I mean, one of them is by
27:39 default the agent conversation is
27:41 actually
27:43 globally viewable by any full-time
27:45 employee at YC. You know, we sort of
27:48 weren't sure about that decision. I
27:50 mean, it felt right and it felt like
27:52 living in the future, but it did not
27:55 come easily. I feel like we had a lot of
27:57 conversations about like, "Well, then
27:59 everyone sees everything. Is that okay?"
28:01 And like, you know, "What is not okay?"
28:03 And then I'm glad we made the choice to
28:05 keep it open, actually, cuz I agree.
28:07 >> people learned how to use it from
28:09 watching how other people used it.
28:10 >> Yes. We used that transparency to solve
28:12 several problems at the same time.
28:15 One, every agent conversation, as you
28:18 mentioned, was broadcast internally to a
28:20 Slack channel. And anybody could join
28:22 that Slack channel and look and learn,
28:25 right? And I remember this is another
28:27 kind of big unlock moment was when you
28:28 started using it really heavily. You
28:30 were like super creative with with the
28:32 things you were doing with it. And a lot
28:33 of us watched that. It was like, "Oh,
28:35 wow. I didn't even occur to me to to
28:37 >> to to to use it that way, right? It
28:39 allows you to be a little more lenient
28:42 on internal security, right? One of the
28:44 things we talked about earlier was this
28:46 trade-off where these agents are at
28:48 their most powerful when they are given
28:50 unrestricted access to lots of context,
28:53 which runs counter to the way more most
28:55 organizations work. It turns out that by
28:57 defaulting to public broadcast for these
29:00 conversations, you kind of institute a
29:02 bit of a social control on what people
29:04 can do with it. Uh that as we learned, I
29:07 think has been like reasonably effective
29:10 uh inside of this high-trust environment
29:12 at keeping private information private.
29:15 Yeah, what's interesting is um it it
29:17 betrays two traits of uh truly agentic,
29:20 like 1,000x superintelligent
29:22 organizations that I would not have
29:24 necessarily guessed would exist, but are
29:26 now like must exist if you want to
29:29 create this type of organization. You
29:31 have to be relatively egalitarian, and
29:33 you also have to be trust by default.
29:35 And then neither of those things uh
29:37 actually are most organizations in the
29:39 world. If you're the founder of an
29:41 organization, you actually have to have
29:42 those at the core of what you're doing.
29:44 And I think like that kind of
29:45 environment honestly works best at
29:47 startups, right? When it's a small group
29:49 of people that are all aligned and and
29:52 and and operating in a high-trust
29:54 environment.
29:54 >> The other thing you have to do is be
29:55 willing to spend like 10 to 100,000 a
29:57 year on tokens. But if you're willing to
30:00 do it and you invest in the skills and
30:02 you like actually do everything in an
30:04 open way with your team that way, like
30:07 basically what I realize is it allows
30:08 you to live in 2028, right? Like what
30:12 you spend 100,000 or a million dollars a
30:14 year on now, it will be commonplace like
30:17 in in 2 years, right? It'll it won't
30:20 cost 100,000 in a year, it'll cost
30:22 10,000, and the year after that it'll be
30:24 like a couple hundred bucks, right? And
30:26 everyone will do it. And we'll call it
30:28 like this is how companies are now. So,
30:30 basically there's a one-time time warp
30:33 where you can leapfrog every incumbent,
30:35 all Fortune 500s, all startups that
30:38 exist
30:39 by doing this. Like I'm imagining in the
30:42 '90s, I wonder if it felt similarly when
30:44 companies started buying computers for
30:46 their employees.
30:47 >> Yeah. They were probably very expensive
30:48 and probably only certain companies
30:50 really invested in buying these like
30:52 expensive, flaky computer systems for
30:54 their employees, but like what a
30:56 superpower to have a computer when your
30:58 competitors like don't have computers. I
31:00 think more tactically how I've seen this
31:02 affect uh YC has been raising the the
31:05 floor. The floor. The floor in a sense.
31:07 What I mean by that is that you could
31:09 have a new employee joining and maybe
31:11 would have taken them 6 months to ramp
31:13 up, but with this it's sort of like they
31:15 automatically get a lot of the context
31:17 from the company working and they know
31:18 how the best people on the star players
31:21 in your organization do things
31:24 by apprenticeship automatically with AI
31:26 instead of uh because partner time is
31:28 expensive or sometimes the best people
31:30 in our org they're very busy, right? And
31:32 you get to kind of run the simulation of
31:34 what it's like to be like Pete when he
31:36 does like a awesome job coaching
31:38 founders on sales or like Gary when he's
31:41 like talking to founders and giving very
31:43 specific advice.
31:44 I think it helps all the new
31:46 new entrants in the organization just be
31:50 a mini version of you a lot faster. One
31:52 of the first things that I appreciated
31:54 about being able to use a coding agent
31:56 was that all of the dumb questions I was
31:58 too embarrassed to ask, I had no trouble
32:01 asking asking the agent. And it this is
32:03 kind of that same thing but at an
32:05 organizational level, right? You're a
32:06 brand new employee, you're embarrassed
32:08 to ask, you don't want to bug Harj with
32:10 with a question and now you don't have
32:12 to, right? You and which on that means a
32:14 lot more questions get asked and
32:16 answered and people ramp up much more
32:18 quickly. After you had built all of this
32:21 agent infrastructure at YC, it inspired
32:23 you to write this essay "Horseless
32:25 Carriages" that went like pretty viral
32:26 on the internet. Maybe you can like
32:28 explain the ideas behind horseless
32:30 carriages. I think they're still very
32:31 relevant now. It was a critique of a lot
32:33 of the the AI software that I saw being
32:36 built at the time. And
32:38 to be totally honest, I think a lot of
32:40 it still falls into this
32:41 >> It's still like that. Yeah, it didn't
32:42 change.
32:43 >> Yes. I just saw a lot of examples of uh
32:47 companies building software and adding
32:49 AI features by sort of slotting a little
32:52 bit of AI inside of a lot of software,
32:54 right? And And the example that I used
32:56 at the time was the the kind of email
32:58 writer that uh the the Gmail uh
33:02 team had had shipped. But the the real
33:04 idea underneath was this kind of that
33:06 the the the potential for AI is to shift
33:08 control of software from the developer
33:12 to the user, right? And And the the
33:14 simple example I started with was
33:15 basically that all of these kind of like
33:18 AI as a little feature
33:20 kept a bunch of prompt context about how
33:23 the AI should do a job locked away and
33:25 hidden from the user, which is just this
33:27 classic example of like, well, it's the
33:29 developer's job to figure out how all of
33:31 this stuff should work. So, the
33:33 developer should write that, and we
33:34 should protect the user from that kind
33:36 of complexity.
33:37 >> Safetyism, I hate it.
33:38 >> Right. And And you know, and it And it's
33:39 just again going back to this contrast
33:41 between watching
33:43 the way that some of these tools work
33:45 and what it was like to use a coding
33:48 agent on my computer that could do
33:50 anything, right? And feeling feeling
33:52 like I I had superpowers. I think the
33:54 conclusion that this essay points to is
33:57 that as we get better at building
34:00 AI-native software, it's going to look a
34:03 lot more like the agent wrapping
34:06 software deterministic tools rather than
34:09 deterministic software wrapping an AI,
34:12 right? And we've done our best to expose
34:15 that to internal employees with some of
34:17 these primitives that we built.
34:19 Um but we have a lot we have a long way
34:20 to go. The chat as the interface, I just
34:22 feel something There's like I things
34:24 going around right now about how there's
34:25 a need to build new interface for like
34:27 AI and what does that look like. And I
34:29 think that just comes from people who
34:30 haven't like touched and felt it yet.
34:32 Chat is actually pretty good because
34:34 like you trust the agent, you
34:36 increasingly trust the agent to do more
34:37 of the work, and you trust its
34:38 decisions, and you don't actually need
34:40 to like have too much of a UI to go in
34:43 and like review the things it's it's
34:45 doing. I feel like it's time for a
34:46 just-in-time software.
34:47 >> Yeah, basically, right? Like yes,
34:49 occasionally you want it to present you
34:50 like maybe you like a specific view of
34:53 something, but
34:54 >> And it could make the software and build
34:56 it as a single-page JavaScript just
34:58 purposely built for you at that moment.
35:01 Yeah. And it could be a skill file that
35:02 could be like called anytime you want. I
35:04 was thinking a lot about this because I
35:06 used to be in the camp that oh, when
35:08 ChatGPT came out and it was 2023, that
35:10 perhaps chat was not going to be the UI
35:12 for all these AI applications.
35:15 And I've definitely changed my mind.
35:17 Part of it is that after experiencing
35:18 all these tools, and I think the more I
35:20 reflect upon it, why chat is probably
35:22 the better interface is because it's the
35:25 closest thing to human language, and
35:26 human language and writing is basically
35:29 the closest thing to expression of
35:31 thinking.
35:32 >> Mhm. So, chat is the closest stepping
35:34 stone to clear intelligence.
35:36 >> Yeah. So, you can't just
35:39 put it in a box. I think it just
35:40 constrain us too much to have a very
35:42 specific box.
35:44 So, that's why I thought it was like,
35:45 okay,
35:46 all in with chat interfaces. I used to
35:48 be in the other camp, and it's like I
35:49 just multi-modal. I know we've talked
35:51 about like Telegram is not ideal, but I
35:53 actually really Yeah, it's pretty good.
35:54 Yeah, it's pretty good.
35:55 >> And the voice memo, sometimes when I
35:56 don't want to type, you just do the
35:57 voice memo, and it's it feels like I'm
35:59 talking to Like I can give my open claw,
36:01 like I can give it text, I can give it
36:03 voice, I can give it pictures of things,
36:04 like I can give it files, like it's like
36:06 pretty good.
36:07 >> Yeah. I just experienced this. So, like
36:10 January, I think the last episode we
36:11 did, I just talked about this, like I
36:13 spent January and through February
36:16 building a half a million lines of code
36:18 for a Rails app, which was Gary's list,
36:21 and it was like, yeah, I know people
36:22 make fun of me for like it was a blog,
36:24 but it was like I built the blog in like
36:25 the first week. Like I spent a month and
36:27 a half building a full agentic framework
36:30 that did like my own version of deep
36:32 research and like fact-checking. But the
36:35 thing is I built it the way I would have
36:37 built software in 2013, the last time I
36:39 wrote code. It was like the web 2.0
36:41 version of this. And Claude code lets
36:43 you do that. And what's crazy to connect
36:46 is like I'm working like I don't know. I
36:49 think I wrote like 40,000 lines of code
36:50 the last 3 days just for G brain.
36:54 And G brain is basically Gary's List
36:57 2.0, but it's totally open source,
36:59 right? So everything I had to write for
37:01 agentic retrieval, everything I had to
37:04 do for voice extraction, everything I
37:06 had to do for fact-checking, all of that
37:09 now exists inside G brain and I just
37:12 gave it to my, you know, Gary's List
37:13 team yesterday as their own open claw
37:16 instance. And they're flying now, right?
37:19 Like they were complaining about like I
37:21 had made, you know, this monolithic
37:24 writer chat interface and it was like
37:26 full of bugs cuz I was like
37:27 re-implementing things that open claw
37:29 and telegram already do. And now they
37:31 just use open and claw telegram and my
37:34 retrieval system with like all the same
37:37 data that I extracted it out and with
37:39 our MCP and it's working great. Like
37:41 basically, you know, Gary's List 2.0 the
37:44 next rewrite thankfully is not half a
37:46 million lines of rails code that is like
37:49 insane to actually, you know, it's
37:51 rigid, it's takes a long time it like
37:54 takes like 10 times longer. You know,
37:55 even though it was 1/100 the amount of
37:58 time to do it like by hand, you don't
38:00 have to do it by hand. Like that half a
38:02 million lines of code in rails is easily
38:04 like 10,000 lines of like typescript and
38:08 like maybe 2,000 lines of markdown. And
38:11 all of that is way more dynamic. Like
38:13 you could just say like actually, for
38:15 the second paragraph, I really like
38:18 including a biography of like the the
38:20 we're focusing on. And it's like I don't
38:23 have to code that in Rails. I don't even
38:25 have to write that into um a Ruby file
38:28 that then gets evaled in like,
38:31 you know, my complex eval
38:32 infrastructure. Like, Open Claw just
38:34 knows that, and I have an eval skill. My
38:37 editor-in-chief can just change it on
38:38 the fly, and I didn't touch it. Yes. And
38:41 it's like, this is insane, actually.
38:42 Like, this is actually the dawn of
38:44 just-in-time software, and I can see it
38:46 right now. The best AI software that
38:48 I've used, whether it's inside of Wyse,
38:50 or
38:51 or tools that others have built,
38:53 tend to be very small. And
38:57 just add kind of the smallest amount of
38:59 code ahead of time that you need in
39:02 order to let the model shine. Mhm. And
39:05 you can build an awful lot with that,
39:08 right? I can write tens of thousands of
39:09 lines of code, uh like like you're
39:11 saying. But, the ability to start at
39:13 this like extremely simple thing that I
39:15 need to understand very little in order
39:18 to use is incredibly powerful, and I
39:20 think that's I think most software in
39:22 the future is going to look like.
39:23 >> talking about this earlier, but I think
39:24 that is what Open Claw did really well.
39:27 Like, there were like a few things that
39:29 you want you wanted like some ability to
39:30 give it a bit of personality. You wanted
39:32 it to like persist and last for a long
39:34 time, and have some concept of memory.
39:36 And it's not like perfect, but
39:38 that's like actually like good enough is
39:40 like for that use case. And Claw code,
39:42 too. Every time Boris comes and speaks
39:44 at Wyse, he spoke with Diana uh earlier
39:47 this week. One of One of the things that
39:49 really stands out is how obsessed he is
39:51 with simplicity, and with just like
39:52 making the product as small as possible.
39:55 My favorite example of this is is uh the
39:58 this open-source harness called Pi,
40:00 which is a That's what That's what Open
40:01 Claw uses as its out-of-the-box coding
40:03 agent. It's this beautiful piece of
40:05 software, which is just like the
40:06 smallest possible coding agent. You can
40:09 use Pi to modify and extend Pi, right?
40:12 And it's this kind of idea of like
40:14 self-extending and self-referential
40:16 software. It's really fascinating. And
40:18 and you're right, Openclaw was built on
40:19 top of that. One of the things I'm very
40:21 curious to see is how many other sort of
40:23 pieces of classic software emerge in
40:25 this form as this kind of minimal thing
40:28 that you start with uh and then use an
40:31 agent to extend over time. I think more
40:33 and more I mean, looking at honestly the
40:35 benefits that we've gotten from having
40:36 our own customizable software, I suspect
40:39 that a lot of commercial software
40:41 uh will come with this capability uh out
40:44 of the box in the future. There's a
40:46 really interesting subtle thing that I
40:47 wanted to talk about around like what I
40:49 learned from your essay, uh which is
40:52 like AI can either be centralizing or
40:54 decentralizing. And um the Google Gmail
40:58 like I can't change the prompt thing is
41:00 like the perfect example of that. We
41:01 basically have a choice to be made over
41:03 the next I don't think it's even that
41:05 long. I think it's like 18 to 24 months.
41:07 It might take 5 years, but um there are
41:10 sort of two scenarios and uh what comes
41:12 to mind is literally like the uh 1984
41:16 Macintosh commercial by Apple
41:18 where it's like is 2034 going to be like
41:21 1984? And you know, the 1984 case would
41:24 be we have centralized control, like
41:27 there are five kings, there's only, you
41:29 know, one of them maybe wins. They have
41:32 the most advanced AI. They have uh end
41:34 run around all compute and power. They
41:36 have all the space data centers cuz they
41:38 could you can't build any terrestrial
41:40 data centers in America anyway. There's
41:42 this like centralization of control. And
41:45 not only that, they don't let you run
41:47 your own prompts.
41:48 Like they literally do the Gmail thing,
41:51 but like for your whole computing
41:53 existence, right? And this would be as
41:55 if like personal computers never existed
41:58 and there were only mainframes and
41:59 minicomputers. Like this is sort of lost
42:01 to the sands of time, but you know, in
42:03 the 1960s and '70s when computers first
42:06 came out, like you couldn't go to the
42:08 store like you can today. You couldn't
42:09 go to an Apple store and just buy
42:12 an iPhone, let alone uh a Mac. You had
42:15 to get access to like this thing that
42:19 was worth like hundreds of thousands of
42:20 dollars to millions of dollars. And the
42:22 only
42:22 >> was like And it was like tightly locked
42:24 down by corporate policies. You're
42:26 right. And the And the thing that really
42:27 spurred the computing revolution was
42:29 when people started having personal
42:31 computers that they could experiment on.
42:33 Yeah. And just like the priesthood,
42:34 right? There was a small priesthood and
42:37 an institutional base that controlled
42:39 capital, literally the means of
42:41 production. And so, you know, this is
42:43 like a coherent future that we could
42:46 live in that I don't want to live in.
42:48 And the alternative to that is actually
42:51 uh embedded in the Homebrew Computer
42:53 Club. It's embedded in the revolution
42:55 that Steve Jobs and Steve Wozniak gave
42:57 us when they were in the garage in
42:59 Mountain View, literally soldering
43:01 together breadboards. And they like sold
43:03 500 of these Apple Ones. And I think
43:06 we're at the Apple One moment right now.
43:07 We are coming up with the primitives. We
43:09 are learning
43:10 how do these things work and how do we
43:12 sell it and how do we package it? Uh but
43:15 then there's like a lot of choices right
43:16 now, right? Like most people, the mass
43:19 you know, a billion users use ChatGPT.
43:22 And ChatGPT like gives you a little
43:25 access.
43:26 But MCP is really locked down. You
43:29 actually, you know, can't hook things up
43:32 to your own databases that easily. Um
43:35 and you know, for what? Safety? Like I
43:36 would argue Claude is like a little bit
43:38 more open, but not really. Perplexity is
43:41 probably the best version of it, but
43:42 it's still like you know, pretty limited
43:45 compared to what you could do with Open
43:47 Claude and Hermes Agent.
43:49 And so, what does the uh revolution look
43:52 like that is like the true personal AI
43:54 moment? And that's what I hope that we
43:57 are building with things like G Brain
43:59 and you know, Hermes Agent and Open
44:01 Claude. Like the ability to run your own
44:05 software,
44:06 to change your own prompts, to test all
44:09 of it, to have your own private repo
44:12 that like you know is only yours, to be
44:15 able to choose which model to use, and
44:17 maybe it's an open weight model. Like to
44:20 me that's sort of the white pill for AI
44:22 is we could have corporate control, no
44:25 control of your own prompts, and like
44:27 literally the AI happens to you.
44:29 You know, you're under the API line. Or
44:32 like there's this other alternative
44:34 where I want like a billion people
44:37 to actually control
44:39 and program for themselves what are
44:41 these things. This should be an
44:43 extension of yourself and what you care
44:44 about, not what, you know, Meta or
44:47 Alphabet or even OpenAI or Anthropic
44:50 care about. I always really bristle when
44:52 I see AI framed as a way to replace
44:55 people because it just doesn't match the
44:58 way that I have experienced it and the
45:00 way that so many of the people around me
45:02 have experienced it, not as a
45:03 replacement for humans, but as a thing
45:06 that empowers. If you look at at at kind
45:08 of how tech has developed since the era
45:10 of of mainframes to PCs to the internet
45:13 which gave everyone like a publishing
45:15 platform like it's it's a story overall
45:17 above all of individual empowerment and
45:19 I think AI is going to play out the same
45:22 way. I think it is going to enable us to
45:24 do more than we could before. I think
45:27 it's going to eliminate kind of the
45:29 drudgery style work that like made a lot
45:31 of my job painful in the past. To me
45:34 it's like we have to make choices to do
45:35 so. By default like a company is not
45:38 open. By default a company is command
45:41 and control. By default maybe the
45:43 leadership gets access to these tools,
45:45 but like the, you know, line level
45:46 people, the staff people don't, right?
45:49 And like we need like a radically
45:51 different type of organization and we
45:53 need to actually offer computing in a
45:55 different way and these are all choices
45:58 and the people who are watching are
45:59 going to be the people who build all
46:01 these things in society. So,
46:04 we better choose well.
46:05 >> [music]
46:05 >> Well, that's all the time we have for
46:07 today. I mean, I think we covered some
46:09 pretty heavy stuff, but Pete, thanks for
46:11 joining us. Thank you. Thank you. Thanks
46:14 for watching, guys. We'll see you guys
46:16 on the next one.
