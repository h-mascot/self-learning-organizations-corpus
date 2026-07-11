---
video_id: X_JsIHUfUjc
title: "How to Build a Self-Improving Company with AI"
channel: "Y Combinator"
source_url: https://youtu.be/X_JsIHUfUjc
duration_seconds: 808
upload_date: 20260521
transcript_source: youtube captions
---

# How to Build a Self-Improving Company with AI

0:00 This is based a little bit off a talk
0:01 Diana gave. There's a video up over the
0:03 weekend, which is super cool. Um Jack
0:04 Dorsey was tweeting some stuff like two
0:06 or three weeks ago that I thought was
0:08 super cool. And I've kind of um stolen a
0:10 bunch of those ideas and shoved them in
0:13 here. This talk is like pretty
0:14 conceptual and high-level about thinking
0:17 about how to build companies. So, the
0:19 Roman legions were designed to
0:23 project power over two continents or
0:27 something from Rome at the center to
0:29 like these people on Hadrian's Wall up
0:31 in Scotland. And the idea was um this
0:35 nested hierarchies with consistent spans
0:37 of control. And you had like named
0:39 individuals with spans of control to
0:41 pass orders down and send information
0:44 back up the hierarchy. And if you think
0:46 about most companies today, they are
0:48 organized like a Roman legion, where
0:50 human beings are the conduit for
0:52 information flowing up and down. And so,
0:54 Jack Dorsey's tweet that I thought was
0:55 great was this like this underlying
0:57 assumption that hierarchically organized
1:00 companies are the are the way that we
1:02 should be organizing like our economic
1:04 units of value. And I think AI basically
1:06 breaks that. If you talked to people a
1:08 year ago about how AI was useful,
1:11 they talked about productivity. Like
1:15 co-pilots, making engineers 20% more
1:17 productive, adding co-pilots to
1:18 workflows, shipping more software.
1:21 But I think that is actually a
1:22 broken way of thinking about AI. That's
1:25 like P had a great blog post where
1:27 basically just like taking the old way
1:29 of working and adding like a more
1:30 powerful engine onto it. And instead of
1:32 that, I think you can reimagine like
1:34 what a company is and how it acts. And
1:37 so, as Gary's talking, like he
1:39 I genuinely believe can produce more
1:41 code than an entire engineering team.
1:44 The thing that's really stuck with me is
1:45 this idea of like extracting the domain
1:48 knowledge from your company and defining
1:50 it as a as like context or a set of
1:52 skills or whatever you want to call it.
1:54 But like this idea that there's domain
1:56 knowledge or business knowledge or like
1:58 some know-how that's inside the heads of
2:01 people and in Slack messages and in
2:04 emails and in Notion, all of this like
2:06 information together defines how your
2:09 company works.
2:11 And if you can make that legible,
2:13 you suddenly can
2:15 can move from this hierarchical
2:16 organization to a sort of intelligent
2:19 AI-powered organization
2:21 with AI-native software. AI isn't the
2:23 something It's not something you bolt
2:25 onto the side of a company. It's not
2:26 like a tool you give to engineers to
2:28 make them more productive. But I think
2:30 you can reimagine what a company is as a
2:32 set of recursive self-improving AI
2:35 loops. I think this is really, really,
2:37 really important because when it gets
2:39 there, I think the company starts to
2:42 self-improve
2:43 even when you're sleeping.
2:45 So let me give you an example. Diana's
2:46 talk talks about this as well. This AI
2:48 loop, you start with like a sensor layer
2:50 which is like That's a fancy word, but
2:52 really it might be like
2:54 emails from your customers. Might be
2:56 support tickets, code changes, people
2:59 canceling their subscription, uh product
3:02 telemetry. It's like sensor data to get
3:05 information from the outside world. And
3:07 then a a policy layer, a decision layer,
3:09 like rules about what you can do, what
3:11 it has to ask a human permission for,
3:13 what it must log, a tool layer that's
3:15 kind of Gary's skills and code like the
3:18 tool layer is Gary's code. It's
3:20 basically deterministic APIs, things
3:21 like query my database or look at my
3:24 calendar. Um a set of tools that the the
3:28 AI can call, a quality gate like that
3:31 might be eval's deterministic checks,
3:32 safety filters, human review for
3:34 high-risk stuff, and then a learning
3:37 mechanism. It's like your system
3:39 interacts with the real world, picks up
3:41 where it doesn't work, and loops back
3:42 into the top again. And if you can run
3:44 every single step of that without human
3:46 intervention without with minimal human
3:48 intervention, your system gets better
3:50 and better and better
3:51 while you're are
3:52 And I can give you actual examples of
3:54 this that are live right now. We started
3:56 with an agent that you can ask and if it
3:58 has deterministic tools to query our
4:00 database. Pretty simple like, when did I
4:02 last have office hours with this
4:03 company? Then it got a little bit
4:05 smarter, which was like, for this
4:07 company I'm doing office hours with
4:08 right now, they need introductions for
4:10 anyone in petrochemicals or something.
4:12 And it could query the database in
4:13 different ways and use rag and all sorts
4:15 of stuff to like come up with five
4:16 relevant founders for you to meet. But
4:18 again, this is like this is a sidekick,
4:20 right? This is an agent. This is like
4:21 the old This is last year's version of
4:23 how a how AI is making me better as a
4:26 group partner. It's making me 20 or 30%
4:27 more effective.
4:29 The aha moment for me came when we put a
4:32 monitoring agent on top of that, which
4:34 looked at every single query every
4:36 single YC employee was doing and saw
4:39 when it worked
4:41 and when it did not work.
4:42 And when it did not work, it's like, oh,
4:44 why not? What would have made this query
4:46 work? Do we need different deterministic
4:48 tools? Do we need to update the skills
4:50 file? Do we need a different database
4:51 for you? Do we need a new index? And
4:53 this happened This literally happens
4:54 overnight now. Let's write the code, put
4:57 in a merge request to the YC code base,
4:59 have an agent review it, and merge it,
5:00 and deploy it. So, when a human comes
5:02 the next day to ask the same query, it
5:05 will now succeed. For me, that was like
5:07 the
5:08 holy [ __ ] [ __ ] But that's not just
5:10 AI making you 20 or 30% more valuable,
5:12 it is the AI going through this loop to
5:15 figure out how to self-improve. And I
5:17 think basically, if you can identify
5:19 parts of your company that work like
5:21 this and eliminate as much of have the
5:24 human in kind of a monitoring or
5:25 supervisory capacity,
5:28 you can just throw tokens at this
5:30 problem and your company will get
5:31 better.
5:32 And so, other examples might be, if you
5:34 have product analytics, having an agent
5:36 go through your product analytics to to
5:38 figure out what part of your sales
5:39 funnel is presenting the highest amount
5:42 of friction, researching best practices,
5:44 putting in place an AB test, running it
5:45 for a week, picking the best version,
5:47 and deploying it. Then doing that again
5:49 and again and again for your product. So
5:50 you just have a self-optimizing like
5:52 product loop. Or you do it with customer
5:53 service queries. You have customer
5:56 suggestions coming in and in and in. You
5:58 triage it with a kind of you have to
6:00 have an agent which is like your chief
6:01 product officer and your chief
6:02 technology officer who make kind of
6:04 judgment calls about okay, this is a
6:06 suggestion we just don't want to do,
6:07 we'll discard it. But no, this is a
6:08 suggestion which is now in line with our
6:10 road map. Um we can do it overnight.
6:12 Let's write the code. Let's deploy it.
6:14 Let's ship it to the customer without a
6:15 human being involved.
6:17 So I think if you can think about each
6:19 part of your company as a self-improving
6:22 like recursive AI loop, it becomes very
6:24 very different to this like
6:24 hierarchically organized Roman legion of
6:26 a company. So what? So like if you want
6:28 to do this, what are the implications?
6:29 One is like burn tokens, not headcount.
6:32 We are seeing companies get to demo day
6:34 with about 5x more revenue per employee
6:37 than they did
6:38 18 months ago. And I think that's going
6:40 to continue to series A and series B.
6:43 And so I think you're going to be
6:45 constrained on token usage, not on
6:47 headcount really really soon. The blunt
6:49 measure now is just like measuring
6:50 everyone's token usage, which is
6:51 obviously like dumb and gameable at the
6:55 extreme, but directionally I think is
6:58 correct.
6:59 We're in the phase of like what is
7:01 possible right now, and so everyone
7:03 should be experimenting to the max to
7:05 figure out what we can even do with this
7:07 crazy new intelligence we have. As soon
7:09 as you turn it into a leaderboard and
7:10 people get promoted or fired based on
7:11 it, obviously it gets gamed. Obviously
7:13 that's dumb. But I think directionally
7:15 figuring out who in the organization is
7:17 token maxing, who is not, is like a good
7:20 way to think about which employees you
7:22 should be spending your time with. I
7:23 think middle management is done.
7:24 I just don't think you need middle
7:25 management for this coordination
7:27 problem. I think AI should be doing it.
7:29 And for me there are two roles. Jack
7:31 Dorsey has three. I actually don't like
7:32 the third one, so I deleted it. But
7:34 there are two roles that really really
7:35 matter for me. I think everyone just has
7:36 to be an IC now, a builder, an operator.
7:39 And I think crucially having directly
7:41 responsible individuals to get anything
7:44 done, I think you need a named human.
7:46 Not a committee, not a group of people,
7:47 just a single person.
7:48 And I think you can build companies
7:50 based on ICs effectively. I I think just
7:53 middle management is is over. So,
7:55 building the self-improving company,
7:56 that's the dream. And by the way, I
7:58 think like people are
7:59 at the bleeding edge of this right now.
8:01 I'd be interested to see where you all
8:02 are, but it feels like people are like
8:04 exploring the boundaries here. I'm not
8:06 sure anyone has a truly self-improving
8:08 company in every function.
8:10 I might be wrong. You might prove me
8:12 wrong. What would I do? First of all,
8:13 this is really, really important. I
8:14 would make the entire organization
8:16 legible to AI. What does that mean? It
8:19 means you've got to record everything.
8:21 Um simplistically, all of our um partner
8:25 emails, now if you email a YC partner,
8:27 that email is in the YC database. Every
8:30 Slack message, every DM, every office
8:32 hour we've started recording for the
8:33 last three or four months. Every single
8:35 thing that happens,
8:37 if it is recorded, it happened to the
8:39 AI. If it did not get recorded, it is it
8:41 did not happen to your intelligence. You
8:43 know what I mean? And so, I was talking
8:45 with some founders over here um just
8:47 now, and we're having like really good
8:48 conversations about their company. But I
8:50 every conversation I had, I was like,
8:52 "Fuck, I need to be recording this
8:53 conversation." Because some guy wanted
8:56 an introduction to I can't even remember
8:58 who the introduction was now. Uh who was
9:00 that?
9:01 I was talking to someone about an I
9:02 promised you an introduction. I said,
9:03 "Yes." And I said, "Email me afterwards
9:05 cuz I would I I'm going to forget this.
9:07 I'm going to talk to 20 people." Yeah,
9:08 so it needs to be on my phone or a or or
9:10 smart glasses. Or we deck out every room
9:12 with like microphones. But basically,
9:15 everything needs to be recorded so that
9:16 it can be legible to the AI. And then as
9:17 Garry talked about like diarization, you
9:20 cannot pump in
9:21 100,000 hours worth of recordings into
9:23 context window. So, you have to diarize
9:26 it. You have to basically aggregate it
9:27 down, synthesize it into the important
9:29 parts, and then give the AI breadcrumbs.
9:31 So, like, "Okay, so here's an example.
9:33 Who's read the user manual, the YC user
9:35 manual?" Hopefully, everyone in this
9:37 room has at least opened the user manual
9:38 at one point in time, right? Like
9:40 it's fine. It was written 5 to 10 years
9:42 ago, most of it. It's kind of out of
9:44 date.
9:45 So, Harj thought uh last weekend, since
9:47 now we've got about 2,000 hours of
9:49 recorded office hours from the last 3
9:50 months, why don't we regenerate the user
9:52 manual?
9:53 And so, you can click like you give it a
9:55 set of instructions, you basically
9:56 diarize it down, synthesize like
9:59 categorize it into certain areas like
10:00 fundraising, hiring, co-founder
10:02 disputes, whatever,
10:04 and then write me a new user manual.
10:06 And by the end of the weekend, he had a
10:07 150 page user manual, which is
10:09 dramatically better than the existing
10:11 user manual. And now we can also update
10:13 it every single month. So, our user
10:15 manual becomes self-improving. Every new
10:17 piece of advice we give, it's compared
10:20 with the existing user manual and either
10:21 incorporated or thrown away. So, the
10:23 user manual becomes this up-to-date
10:25 living brain of the advice we give to
10:26 founders.
10:28 And obviously, it doesn't stop as a user
10:29 manual, you then pump it in as context
10:31 to an AI agent, and suddenly you can ask
10:33 a superintelligent AI
10:34 and get the combined wisdom of 16 YC
10:36 partners in one.
10:39 But only if it's legible. So, you have
10:41 to record everything. The second point
10:43 is kind of the same, right? Like if it
10:44 creates an artifact that can
10:45 self-improve, it's legible. If it
10:47 doesn't, you throw it away. The third
10:49 point then is that every function can
10:52 generate This used to say dashboards.
10:54 It's not just dashboards, it's on-demand
10:55 software. Codex 55 is now good enough
10:57 you can one-shot most simple like
11:00 most internal software dashboards you
11:02 can one-shot to a pretty high level of
11:04 quality. I tried it over the weekend on
11:06 a bunch of our stuff. It's just unreal.
11:09 So, all of your internal operations
11:10 teams should be sitting on this layer of
11:13 like kind of intelligence understanding,
11:15 and then creating their own dashboards
11:17 and their own workflows. And I would see
11:20 that those as
11:21 entirely disposable. I would very
11:24 preciously store all the data. So, as
11:26 Garry said, he puts it all all of his
11:28 emails in markdown. Never throw anything
11:29 away,
11:30 but then treat these the software as
11:33 ephemeral. You can you can generate it.
11:35 You can regenerate it. The valuable part
11:37 is like the comprehension inside
11:39 people's heads of like this is how the
11:40 function works. This is how we run a YC
11:43 event, whatever. The software to
11:44 actually run the event you can generate
11:46 for the event. You can throw it away.
11:47 The the models get smarter in a month or
11:49 two. Throw the software away. Give it
11:52 your original set of instructions and
11:53 regenerate the software.
11:54 So I think the business context and and
11:57 skills are the valuable part. I think
11:59 the software on top of it is ephemeral.
12:01 So what what is humans for in this
12:03 world? I think basically we're talking
12:06 about a company brain. And I know a
12:07 bunch of people in this room are
12:08 building this. But the bit in the
12:10 middle, like all of your data, all of
12:12 your emails, your DMs, the skills, the
12:14 know-how, that is like the company
12:17 brain. And I think the humans sit around
12:19 the edge of this interfacing with the
12:20 real world.
12:22 So it's where this intelligence makes
12:24 contact with reality.
12:26 Human beings reach into places the
12:27 models can't go yet. That might be like
12:31 a conference. It might be a I'm trying
12:33 to think of examples. I would say a
12:34 phone call, but I think the AI can reach
12:35 into phone calls pretty easily now.
12:37 I think it's like novel situations,
12:39 ethical considerations, high-stakes
12:41 moments. You know, it's like it's where
12:42 the founder comes to us
12:45 and is
12:46 like thinking about breaking up with
12:47 their co-founder. Right? It's like those
12:49 real high-stakes, high-emotion moments
12:51 where you really want a human being. I
12:53 think that's where the human fits. For
12:56 all of you, like sales conversations. I
12:58 think that's a human being in the room
12:59 for the next 20 years. So the humans
13:01 live I think around the edge.
13:03 And I'm over time and Kulveer should
13:05 bullhorn me. I will leave you this one
13:07 question. If you were building your
13:09 company today,
13:10 would you start it in this shape?
13:14 For most of you, you're small enough to
13:16 build it right. And so I don't think you
13:17 have any excuse. And I know there are a
13:19 few of you who are in the process of
13:21 ripping up and rebuilding your company.
13:23 So with that I will stop and will hand
13:26 over to Pete. Thank you for listening.
