---
schema_version: 1
platform: youtube
stable_id: RBqT2PHWdBg
title: "Inside Ramp, the $32B Company Where AI Agents Run Everything | Geoff Charles"
publisher: "Peter Yang"
canonical_url: https://www.youtube.com/watch?v=RBqT2PHWdBg
published_date: 2026-03-15
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via groq-whisper-asr"
rights_status: third-party
rights_holder: "Peter Yang"
content_sha256: 83596488065cc0e3b5cbf5e0445d256df87f866548d939507ba8d2c378b857cb
duration_seconds: 2642
transcript_source: groq-whisper-asr
asr_models: ["whisper-large-v3","whisper-large-v3-turbo"]
availability: public
caption_error: YouTube captions unavailable; recovered from cached signed audio URL.
raw_files: {"asr-000.json":"29cc1f26129495521c11047eac09cf859ebd7192700694647c070369fe77a6e6","asr-001.json":"263d34b9e838511f506cbd7d490b3923c44d5f88a426ad3a1c2cd4c9ec3a7c21","asr-002.json":"b7e92079fcc914a9b8b71b7e1a54d669a91f382120998c5b76ede688fb14136e","asr-003.json":"cfd5e11ec80fd790c8bccf7e74e33de720fbc398785fd0ea85925f06a7e24966","asr-004.json":"2995eb9f7364b475fe9294148738b1a12e3112c7c4b241bfbf1774194bb5a5c9","source-info.json":"a76a4daf333be41857520b4c9f8c3bfbaf6f29fa03e46f03825bb5c5319bee3e"}
raw_path: raw/youtube/2026-03-15--inside-ramp-the-32b-company-where-ai-agents-run-everything-geoff-charles--peter-yang--RBqT2PHWdBg
relevance_categories: ["feedback-systems","ai-native-company","agent-operations","named-lanes"]
relevance_evidence: ["agents","ai agent","ai-native","feedback loop","ramp"]
relevance_spans: [{"category":"feedback-systems","phrase":"feedback loop","text":"Like how much are you like embedded in like the feedback loops and like the data every single day And then you kind of just develop that as a second nature kind of thing But after you have that how do you actually","timestamp":"12:23"},{"category":"ai-native-company","phrase":"ai-native","text":"And Ramp is one of the fastest-growing companies ever and probably the most AI-native company that I know outside of the big labs.","timestamp":"0:43"},{"category":"agent-operations","phrase":"ai agent","text":"But like, yeah, the AI agent","timestamp":"3:21"},{"category":"agent-operations","phrase":"agents","text":"for the agents rather than engineers themselves.","timestamp":"2:21"},{"category":"named-lanes","phrase":"ramp","text":"My guest today is Jeff, CPO of Ramp.","timestamp":"0:41"}]
rights_note: YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed.
segment_count: 773
---

# Inside Ramp, the $32B Company Where AI Agents Run Everything | Geoff Charles

0:00 If you're not using cloud code this year, no matter what your role is, you're probably underperforming compared to others on the company.
0:06 PMs often pride themselves on like the spec, the perfect spec.
0:08 They have to understand that it's actually AI that's reading the spec now versus engineers.
0:12 50% of RAM's code is built by AI.
0:15 And that's 50% up from 30% in December.
0:17 It'll probably be 80% by March.
0:19 And this is not just like a front-end prototype, right?
0:21 This is the real product.
0:22 Back-end, front-end, and I have a PR and I can just submit it to the engineer team.
0:26 PMs are shipping tons using spec.
0:28 And so are designers, so are operators, so are account managers, and salespeople are also getting activated.
0:34 My job is to automate my job.
0:35 And all our jobs is to automate our jobs.
0:40 All right, everyone.
0:41 My guest today is Jeff, CPO of Ramp.
0:43 And Ramp is one of the fastest-growing companies ever and probably the most AI-native company that I know outside of the big labs.
0:50 So last year, Jeff and the team shipped over 500 features and hit over a billion dollars in revenue, all with around 25 PFs.
0:58 So yeah, really excited to talk to Jeff today.
1:01 And welcome, Jeff.
1:03 Super excited to be here.
1:04 Thanks for having me, Peter.
1:05 Awesome, man.
1:05 So, you know, I've worked at a lot of big tech companies,
1:09 but like, can you give us a quick overview
1:10 of how Ramp ships features, like from idea to launch?
1:14 Yeah, I'll skip the basics
1:15 and just jump into the fact that it's a crazy time right now.
1:20 And the way that we are building
1:23 has always been around velocity.
1:25 And the way that you move fast is by leveraging tools
1:28 and AI is just an incredible accelerant to everything that we do.
1:33 And I hope during this call that I'll be able to share a few of the ways that we've leveraged AI
1:38 to accelerate, to inspire folks and help amplify the learnings.
1:43 I also expect that a lot of the things that we're going to talk about today are going to be outdated,
1:47 even by the time that you even share this recording.
1:51 So I'm excited for it.
1:52 But yeah, I mean, the product development process, you know, hasn't dramatically changed in terms of principles, right?
1:59 It's about understanding customer pain point, about identifying the right solution, about building the solution and then testing and iterating.
2:06 And I think AI just lowered the cost of each of these sections dramatically.
2:12 You know, the cost of code is basically down to almost zero apart from the tokens.
2:17 And so PMs just need to be actually writing the specs
2:21 for the agents rather than engineers themselves.
2:24 And I think that a complete shift in terms of how we go about it Yeah so basically the PMs will make the product first pretty much by themselves right Or make the prototype at least
2:35 and get some validation before doing anything else.
2:38 Yeah, I mean, PMs often pride themselves
2:41 on the spec, the perfect spec.
2:43 And they have to understand that it's actually AI
2:45 that's reading the spec now versus engineers.
2:48 And so the spec itself is basically the output of a prompt.
2:53 and then the output of the spec is the product.
2:55 So at the end of the day, it's just prompt to product,
2:58 back to prompt, back to product.
3:00 And yeah, we are essentially collaborating
3:03 on an actual product itself and a prototype.
3:07 I wouldn't even call it a prototype.
3:08 It's actually a working product
3:09 rather than the actual spec itself.
3:12 Yeah, I always suspect that engineers
3:14 don't read my specs carefully.
3:15 So I always try to keep my specs
3:17 to like less than two pages to begin with
3:19 because, you know, no one wants to read this shit.
3:21 But like, yeah, the AI agent
3:22 will actually thoroughly re-read it.
3:24 So that's a good thing.
3:25 Okay, so before we even get to the spec though,
3:27 like first you have to, like you said,
3:28 you have to understand the customer,
3:29 understand the problem.
3:30 And like, how do you guys work with AI
3:33 to figure out what to build
3:35 or what the customer pain point is?
3:37 Yeah, so the advantage that we have is that,
3:39 you know, we have 50,000 plus customers
3:41 on Ramp and growing super, super fast.
3:42 We have over a million end users.
3:45 And so that gives us a ton of signal.
3:47 We also have a ton of people on sales,
3:49 on support, on account management.
3:51 And so those are all touch points.
3:52 that we can leverage to understand kind of what the problems are and what
3:56 opportunities are and, and what we should be focusing on.
3:59 The question is around like, how do you actually sift through all this noise?
4:03 And that's where like a large language model is fantastic.
4:05 So the first thing we invested in is what we call voice of the customer.
4:10 And typically it was, you know,
4:11 it was a person that we hired that that tried to do all this work themselves.
4:15 Now it's basically an agent and,
4:17 and that agent is essentially able to sift through all our gong recordings,
4:21 all our Salesforce notes, all in-app surveys, all support tickets, all in-app chats,
4:26 any email that is being sent to account managers,
4:31 and essentially gather all that context as well as our Snowflake database and our analytics
4:34 and help answer any question that product managers have around their persona,
4:39 their pain points, their workflows, and the gaps of their products.
4:42 So happy to jump into that, but that's a huge thing that we've invested in.
4:45 Yeah, are you able to give a live demo of that or show us how that works?
4:49 Let me share one version of that So this is our voice of the customer tool And as you can see you can ask any question on this bot and this bot will literally go through any type of question So for this demo I asked you know what feedback that people have on our procurement product right
5:08 And you can see that the sources.
5:11 So do you want me to look through support tickets, chat logs, sales research, feature requests, et cetera?
5:15 I said, okay, let's just go through support ticket and chat logs.
5:17 It literally went through 90 days of support tickets and chat logs and identified the actual key topics that we need to focus on, as well as links to the underlying assets for me to double click into.
5:31 So, you know, purchase order management, approval flow routing, chat, you know, chat understanding with ramp assist, exports, currency constraints.
5:39 I mean, this was done in, you know, from 38 to 40, so about eight minutes,
5:45 and something that would have taken eight days for a human to actually do across the entire volume.
5:50 Yeah, I mean, this is basically like kind of prioritizes your roadmap for you.
5:52 It has a number of support tickets and everything.
5:57 It at least helps you identify with a ton of context the problems that your customers are facing with
6:01 and enables you to go deeper.
6:03 So then you can, you know, it's essentially a conversation, right?
6:05 Imagine you have this, like, full-blown analyst.
6:07 How do you continue prompting the analyst to go deeper?
6:10 So now it's like, okay, I want to go super deep on this specific problem case.
6:13 Bring customer quotes.
6:14 Bring me some like LogRocket sessions.
6:16 Bring me customer IDs that I can go and research to.
6:21 Create an email that I can use.
6:24 Draft that in my Gmail account for me to actually automatically send to set customer to book meetings on my behalf.
6:29 All of these things are basically prompts, and this agent actually has all the connectivity to be able to do these things.
6:35 And I love how the user interface is just like a Slack channel.
6:38 Or I guess you can DM the agent too, if you want.
6:41 Yeah, 100%.
6:41 We've seen Slack being a great place to actually host these things
6:45 because that's essentially what you would do with a human, right?
6:48 You would Slack your product operator or Slack a team channel
6:51 and be like, go do these things.
6:52 So it's a very natural way of doing work
6:55 and personalizing these agents as essentially your coworkers.
6:58 Oh, wow. Okay.
6:59 This episode is brought to you by Granola.
7:02 If you're in back-to-back meetings,
7:04 you know how much work it is to take notes live and clean them up afterwards. That's why I love
7:09 Granola, the best AI meeting notes app in the market. Here's how I use it. Granola automatically
7:14 takes notes during a meeting, and I can add my own notes too. After the meeting ends, I use a
7:19 granola recipe to extract clear takeaways and next steps in the exact format that I want Then I can just share their notes directly in Slack with my colleagues or even get granola to share their notes automatically Honestly of all the AI apps that I use Granola is the one that saves me the most time
7:35 Try now at granola.ai slash Peter and use the code Peter to sign up and get three months free.
7:42 That's granola.ai slash Peter.
7:45 Now back to our episode.
7:47 So that's a qualitative piece that you showed me.
7:49 What about the metrics and the data piece?
7:51 Do you just give people access to pull data themselves?
7:57 Yeah.
7:58 So the space is moving very, very quickly.
8:03 So six months ago, we launched our own bot for data analysis.
8:08 I'll give a quick view of this.
8:11 And this is now outdated, and I'll tell you why.
8:15 So we launched what we call Ramp Research.
8:19 So it's funny, like before you would ask a data analyst or you would try to do it yourself with, you know,
8:23 Looker, Hex is getting pretty good at like creating your own prompts, et cetera.
8:26 But it was still, you know, fairly a lot of work to like get an answer to a question, right?
8:31 And now it's like, hey, I have a question.
8:34 Give me the answer.
8:37 So now we have ramp research that essentially, I mean, the use cases are insane.
8:42 And actually by making it easier for people to ask questions about data,
8:45 you actually increase the number of people who actually ask questions about data,
8:49 and you actually become more data-centric as a company.
8:52 So what's an example?
8:55 Let's say that you have an automated email campaign,
8:57 and you want to understand the performance.
8:58 What's the open rate of automated emails that customers send?
9:00 Boom.
9:01 Ramp Research understands our entire database and understands all the schemas
9:05 and understands what you're trying to do,
9:06 and automatically generates the actual interpretation of said results.
9:11 And this is used so much, and this was in two minutes, right?
9:15 by literally everyone. So salespeople trying to find, you know, what are our customers in Milwaukee,
9:21 support people trying to figure out like the common use cases of XYZ product,
9:26 marketers trying to figure out the performances of their campaigns, et cetera. But I shared that
9:31 this was outdated in the sense that we now basically have moved to Snowflake CLI plus
9:38 plus CLOD plus skills.
9:40 So essentially we've now moved to using CLOD code.
9:45 We have our own database of skills that we've developed.
9:48 So we have a data analyst skill
9:51 that essentially fully understands our database
9:53 and understands how we go about approaching
9:56 a data analytics problem and the best practices of that.
10:00 And we essentially can now prompt Cloud to say, hey, build me a full report of the performance of our procurement product and identify the top reasons why people opt in, the top blockers in our funnel, and draft with me 10 different growth ideas that we could be running.
10:19 And Cloud will actually generate a full HTML report fully baked into our data that is directly actionable.
10:27 Yeah, okay.
10:28 So it's not just Q&A anymore.
10:29 It's actually doing work for you, right?
10:31 That's why it's better than the thing.
10:32 Yeah, I mean, at the end of the day, like, it's funny.
10:35 Like, you know, you ask a question, but you have a goal, right?
10:37 So sometimes you ask the question and you get the result,
10:39 but you should just tell AI what your goal is,
10:42 and you'll actually be surprised at the questions
10:45 that the AI can actually ask themselves to get to the goal.
10:49 And have you given the entire company access to Cloud Code?
10:52 Or is it, like, just engineers, or everybody can use it?
10:56 Anyone can use it, right?
10:57 And in fact, we'll get into this around how you actually become more AI-driven as a company.
11:02 But if you're not using cloud code this year, no matter what your role is, you're probably underperforming compared to others on the company.
11:11 And so it's certainly not a product for engineers.
11:15 It is absolutely a product for builders.
11:18 And we talk a lot about cloud code right now, like Opus 4546, big launches and a big, big movement in the last three months.
11:25 I mean, you just saw the anthropic $30 billion raise.
11:29 But I expect the tools to continue evolving.
11:32 Like, you know, by the time we meet next, you know, the next 90 days, it might actually be completely different, right?
11:37 Yeah.
11:37 And so it's less about, like, forcing people to use one tool.
11:42 It's about giving people full access to any tool they want to share openly where people are using and then get people to adopt to get to the aha moment.
11:51 and then,
11:53 but yeah,
11:53 we don't want to be dogmatic,
11:54 but we want to like
11:55 radically empower
11:56 and also have like
11:57 full visibility
11:58 on what people are doing.
11:59 Yeah, let's talk about it later, man,
12:00 because I think so many companies
12:01 still don't get this.
12:02 They're like,
12:03 oh, you know,
12:03 like what's the cost of this?
12:04 What's the ROI of this?
12:05 Why should I give
12:06 some salesperson this thing?
12:07 They just don't get it, man.
12:09 We'll talk about it later.
12:11 Yeah.
12:11 So let's keep going.
12:12 Let's keep going down
12:13 the product development process.
12:14 So now you have all this crazy
12:15 feedback coming
12:16 and the quote,
12:17 I mean,
12:17 people talk about Protestants
12:19 like it's some mythical thing,
12:20 But I think it's just like,
12:22 like how much product feedback are you getting?
12:23 Like how much are you like embedded in like the feedback loops and like the data every single day And then you kind of just develop that as a second nature kind of thing But after you have that how do you actually
12:37 You mentioned that you don't actually read specs anymore.
12:39 How do you define this solution?
12:41 Just make the product right off the bat?
12:44 Yeah, so there's the problem identification,
12:48 then there's the actual writing of requirements.
12:51 And we have our own cloud skills for that.
12:53 Right. So so, you know, Claude has full access to our notion.
12:57 Notion has the full context and all our personas and all the research we've done.
13:01 That's all automatically transcribed and aggregated.
13:05 And then we have skills in Claude that is like your your product spec skill.
13:10 And we've prompt we've designed it so that it's a conversation based approach.
13:15 So just like you have maybe like a manager or a peer reviewer on your spec,
13:20 Claude will actually interact with you and ask you clarifying questions.
13:24 So, for example, what's the main goal here?
13:27 Here are the tradeoffs.
13:28 Should we trade off this or that?
13:29 Have you thought about this?
13:30 What is the intersection with that?
13:32 It has all the context about what we're trying to do because it has all the other projects that we're building,
13:37 and all of that is a notion.
13:39 And so it helps you basically refine and get to an end state.
13:44 But, yes, we don't really talk about the spec itself.
13:46 That's just a step in the process.
13:48 We talk about the actual product.
13:50 And so happy to share a little bit of how fast we move in terms of prototypes and show you kind of what we're talking about here.
13:56 Yeah, yeah.
13:57 Please show us the skill and everything else.
13:59 Yeah.
13:59 Yeah.
14:00 So let's go through an example of this skill, and then we'll talk about the actual how we build.
14:08 So this is an example of a class skill.
14:12 Folks should be pretty well-versed in this world.
14:16 Yeah, so, you know, product shaping, defining like the role, right, push for simplicity, surface tradeoffs, surface questions, you know, key definition of the problem, you know, like looking up like, you know, all the data that we have access to, do the actual research, look at different competitors, customer evidences.
14:37 It has links to all these different things.
14:40 Synthesize the completion.
14:41 Help me shape this question.
14:42 So, you know, you know, present the synthesis, ask questions around, you know, the forcing decisions, all the different principles that we have and then like related skills.
14:52 So like this is like a skill that you that we load up and this this was actually just built by one of my PM Other PM actually have their own skills We trying to figure out how we actually get to one strong skill as part of the evaluation process
15:05 but this is one of the examples.
15:07 I want to share something.
15:08 So you basically just have to,
15:09 so you basically just be like,
15:10 hey, I want to build some expense tracking feature.
15:13 This thing actually drives the conversation, right?
15:15 It actually drives the conversation with you.
15:17 Yeah, wow. Exactly.
15:18 And then let's go into the build.
15:20 So, you know, 50% of RAMP's code is built
15:25 And that's 50% up from 30% in December.
15:29 It'll probably be 80% by March.
15:32 And it's not inconceivable for it to be like 90% to 100%.
15:37 We've hit coding escape velocity, and it's a brave new world out there.
15:44 The question becomes, like, how do you make it easy for a non-builder to engage with code?
15:52 Because it's obviously pretty intimidating.
15:55 So we invested a lot in building our own visual on top of, you know, any large language model and to radically accelerate, like, how builders can build and how even, like, PMs can build.
16:10 I mean, if you have, like, infinite coders at your disposal, you know, you are actually the bottleneck and you actually need to, like, start moving faster.
16:19 So I'll give you an example.
16:20 Let's say that you actually want to, you have a lot of feedback from customers saying,
16:26 hey, I need more visibility on what needs my attention, and I need to understand kind of what's overdue,
16:32 what's on track, and, like, what's upcoming.
16:35 So I need to understand, like, my account's payable cash flow, okay?
16:38 Yeah.
16:38 So all I need to do is I will go in and say, okay, please build me a report on top of this table that has four metrics.
16:49 my overdue bills, my upcoming bills,
16:54 zero 30 days, 30 to 90 days,
16:56 and the total amount outstanding that I will need to pay.
17:00 So this is obviously a shitty spec.
17:03 This is just for demo purposes.
17:06 But inspect will go,
17:09 and it will actually implement this product.
17:13 And it will understand the task it needs to do.
17:17 It'll actually plan.
17:18 It'll understand the code base. You've already directed it exactly to where you actually need.
17:23 And it also has access to our design component library Right So I don need to teach it to know what a metric should look like what a module should look like what a click should look like
17:35 It has all these components baked in.
17:37 And so it's actually able to just reuse a lot of our existing code to build this thing.
17:41 And I actually did this yesterday for this demo purposes.
17:43 So, you know, here's like where it gets to.
17:47 See if this is working.
17:50 Boom.
17:51 Wow.
17:51 So now you have on top of the bills table your entire metrics.
17:57 What's past due, what's coming up, and the total to pay.
18:00 And this took five minutes.
18:03 And this is not just like a front-end prototype, right?
18:05 This is like the real product?
18:07 This is the real product, back-end, front-end.
18:11 I mean, a lot of this is front-end code, though,
18:14 because I didn't need to create more endpoints.
18:16 Like, we already have all these endpoints.
18:17 but Inspect is able to do both front-end and back-end.
18:21 Dude, that's because I've been using, like, you know, Google AI Studio and stuff just to make prototypes,
18:25 but that's like pure front-end code. It's not, you can't actually push to prod.
18:29 But it sounds like... Correct, and it doesn't have context on your code base.
18:33 It doesn't have, you need to, it doesn't look the same as your product.
18:36 No, I mean, here I can literally, now I can go in and, you know, I have a PR
18:44 and I can just submit it to the engineer team.
18:46 And we have automatic PR review processes where a double-digit percentage of our PRs are automatically approved.
18:53 So PMs are shipping tons using InSpec.
18:59 And so are designers.
19:01 So are operators.
19:02 So are, like, you know, to some extent, like, account managers and salespeople are also getting activated on this piece.
19:09 So it's just a massive accelerant.
19:11 And the number one users are also engineers, engineers using InSpec.
19:15 And here's the other crazy thing about this technology that I want to share.
19:20 So oftentimes you have feedback.
19:24 So we love feedback.
19:25 We obsess over customer feedback.
19:27 We have tons of Slack channels where people are just constantly posting things, right?
19:30 It's very overwhelming once you have the number of customers that we have.
19:35 This is an example of a UX channel.
19:40 And basic thing, right?
19:42 Hey, like, treasury's a product.
19:44 Should probably be case sensitive, right?
19:46 Yeah.
19:47 Add inspect.
19:48 In the web repo side nav, change the following sentence.
19:54 PR merged.
19:56 Like, this is just one, and this is a very easy thing.
20:00 But like anything, any question that you have, say you're an engineer, say, where do I get started?
20:06 There's an escalation, a problem.
20:08 Like anytime there's an escalation on ramp, you know, AI takes the first step.
20:11 It understands exactly what happened.
20:13 It understands we're in the code base.
20:14 It creates the actual PR.
20:16 And oftentimes it ships it.
20:19 Same thing with support tickets.
20:21 Anytime there's a support ticket that comes in where someone is confused, we have inspect basically run through that and recommend changes and have the PR up and ready.
20:29 for the PM or the product operator or even the engineer to review and ship it.
20:33 The speed at which we can move with some of these things is radical.
20:37 So you kind of have the AI to get the first pass.
20:39 Yeah, yeah.
20:39 First pass of everything.
20:40 Yep.
20:41 Let me push back a little bit.
20:42 If everyone in the company is shipping these PRs all day,
20:45 how are you going to keep the product cohesive or keep the quality bar high?
20:50 A lot of the PRs themselves are quality of life improvements.
20:55 We also, within Inspect, we have an understanding of complexity
20:59 And so we do have a process by which we review things based on, like, the sheer amount of complexity that it has.
21:05 And it does route to the right person based on, you know, whether this is, like, a big change on the product side or on the engineering side, et cetera.
21:11 But we haven't yet gone to a big problem.
21:14 We also have a pretty robust release process.
21:16 So once the PR has merged, like, we will, like, slowly roll it out.
21:20 And before any, like, major changes happen on the product that goes to the rest of our customers,
21:26 We have an automated process by which I get involved or the directors of products get involved as well.
21:30 Okay, so you have the typical first everyone in the company plays with it,
21:35 and then if nothing breaks, you get some beta users to play with it,
21:39 and then you roll it to all users?
21:41 Yeah, exactly.
21:42 So we have DocFooting.
21:43 Alpha is your customers that are part of a research group.
21:47 Beta is anyone that opted into the beta tier.
21:49 We have about 10% of our customer base that's in the beta tier.
21:53 So you can launch very, very quickly to beta,
21:55 and then you track analytics on that.
21:57 And then to go from beta to GEA,
22:00 we basically require for large announcements,
22:03 like not really like this naming convention
22:06 or anything like that.
22:07 For any large feature that is material to the customer,
22:10 we basically have a reprocess that's fully automated.
22:12 So because everything is in our databases,
22:17 we have another bot, Ramp Releases,
22:20 that creates a ramp release report.
22:22 It pulls all the information of the context It pulls a preview of the actual product that we can use It pulls from our Snowflake databases the impact this feature has had
22:35 It pulls from any Slack channel, a summary of all the work that was done.
22:40 And it basically synthesizes all the things that...
22:44 It also can do work.
22:46 So to do release, you basically need a help center article.
22:48 Well, it gets written automatically.
22:50 You probably need an internal enablement of what this feature is, how do you use it,
22:54 Why did we build it?
22:55 It writes that automatically.
22:56 You can also post it in Slack.
22:59 So yeah, that's a little bit of how we speed up that process.
23:02 And when you review these larger features,
23:04 are you reviewing the actual product?
23:06 Because a lot of companies,
23:08 the PM writes some sort of document,
23:10 and then it goes through multiple rounds of reviews,
23:13 and then you approve it,
23:15 and then they finally go build a product.
23:17 But I don't think that's how it works at RAMP, right?
23:20 Yeah, I mean, the question is,
23:21 what is my role in all of this now?
23:24 And I think, you know, in the past, my role was, well, you know, I'm the best at like the craft or I'm the best at like understanding what customers want or I'm the best at, you know, understanding the data.
23:36 And that's no longer true.
23:38 Like you have a super intelligent platform that you can leverage.
23:42 So, yes, like I will try my best to look at all the customer feedback, make sure that this is actually meeting the customer feedback.
23:49 I will look at the metrics and call bullshit on like this is not good enough or this is not big enough.
23:52 That's something that is fairly subjective.
23:54 I will go into the product and test it out and play with it and really just hone in on what's working, what's not working.
24:01 But I think the higher level job for leaders now is based on your feedback, what broke down in the process?
24:10 So if you caught a poor user experience, what broke down?
24:16 What prompt failed?
24:18 What skill failed?
24:20 What design system failed?
24:22 because giving feedback to the person
24:24 and so that it can just fix it,
24:26 that's a one-time banding, right?
24:30 What you want to do is you want to figure out
24:32 within the process what broke down
24:33 and fix that process
24:34 so the next time you never have that feedback again.
24:35 Like a classic example for me is like,
24:37 I've told the team 10 times,
24:39 the call to action needs to be above the fold.
24:44 That's like, you want to just,
24:47 you know, six years of A-B testing,
24:50 you want to increase conversion?
24:51 It's a big button that's above the fold.
24:54 That it And I said that like 10 times or maybe 100 times but now it part of our design create process which is a fully automated process in and of itself
25:05 And so before before it gets to me, you know, within within our Figma prototypes, those those those core concepts are actually fully integrated.
25:14 OK, got it. OK, so you have to say the same thing over again. You can provide me like higher level feedback or something.
25:19 Yeah. My job is to automate my job. And all our jobs is to automate our jobs.
25:24 Um, yeah, we can talk about what happens next, but yeah.
25:27 And how about, uh, how about that?
25:28 Cause another thing that sucks up a lot of time is like this annual planning process of
25:32 like, Oh, I spent like a month to figure out what we're going to build for the year or
25:35 like for the next three, three years.
25:37 Right.
25:37 Like how, how, how do you guys manage that process?
25:40 Or is there even like a, like how far do you go?
25:42 How far are you guys look on this stuff?
25:45 Uh, honestly, three months.
25:47 Okay.
25:48 We, we, we can only predict within three months now.
25:51 And by the way, like within three months you can do what you can do.
25:54 in three years now. So like three months is actually a really long time. Yeah. Um, you know,
26:00 planning, planning for me is, um, I think there's actually like three main objectives to planning.
26:07 One is actually aligning on strategy, which is much, much more important. Like what problems are
26:12 you focused on? What are problems you're not focused on and which customer segments are you
26:16 going after? And, and how are you thinking that we're going to win long-term? Like what is the
26:20 the end state for this thing. So it's about trade-offs. And I think like the conversation
26:24 should really be about trade-offs. The second thing that, that planning is good for is just
26:28 having some level of commitment from the teams, right? Um, some level of accountability. And the
26:35 third is, um, to have some baseline for sales to know what's coming. Um, for them when they,
26:43 when they, when they, when they talk to a customer and the customer asks, okay, like this is great,
26:47 But, you know, I have a lot more needs when it comes to our international exposure.
26:53 And the sales team needs some basic assets.
26:55 And so that's the third kind of pillar.
26:58 And that also is, like, fairly automated.
26:59 So once the team kind of does, you know, their backlog and their plan in Notion, we have an automatic, like, process that creates, you know, one-pagers.
27:09 And then it creates slides and content for the sales organization within our own branding guidelines.
27:14 and then the sales team can essentially just look at
27:18 a higher level view of our roadmap
27:19 to be able to sell effectively against it.
27:21 Wow, okay.
27:23 And then you have all these vision
27:24 and how we gonna win stuff Obviously AI can read it and if something changes you can just ask AI to update it Is that how it works I mean what I ask AI to do is to synthesize information
27:37 A lot of leadership time is about helicoptering between the nitty-gritty problems and then the higher level strategy and roadmap,
27:47 and making sure that every level of the organization understands information at the bottom and information at the top,
27:53 Like how you communicate to the CEO and the board is very different than how you communicate to the director is very different than how you communicate with the teams.
27:59 And that LLMs are incredibly good at because it's so like the translation layer, right?
28:05 When I'm in an all hands meeting versus when I'm at a team meeting versus when I'm in a boardroom, very, very different.
28:10 And so I waste a lot less time on those things.
28:13 Got it. Got it. Okay, great.
28:14 Let's get to the key question then.
28:15 I mean, you just mentioned that your job is to automate your job.
28:18 I'm sure all your PMs feel the same way.
28:19 And so what's going to happen to the PM function?
28:22 Do you think it's getting over?
28:26 Yeah.
28:27 What was going on?
28:28 You know, it's funny.
28:31 I was surprised by once you automate code,
28:35 a lot of people concluded that PMs are over for PMs.
28:40 And I thought to myself, it's over for the engineer, for most engineers.
28:45 Maybe it's like a lot of engineers who are like, I'm going to be a PM now
28:47 because the engineering function has changed a lot.
28:53 Now, obviously, there's a ton of value for engineers
28:55 because I think an engineer now is managing hundreds of thousands of agents
28:59 and they can actually scale their impact.
29:02 But let's go back to the PM role.
29:06 There's a lot of bad PMs out there or badly trained PMs.
29:10 I think that the way we've trained PMs in the past has been really, really bad.
29:14 And we've trained them on stakeholder management.
29:16 We've trained them on prioritization.
29:18 We've trained them on communication.
29:19 We've trained them on frameworks.
29:21 And those are all outdated because code is free.
29:24 And so, like, all that matters now is are we going the right direction?
29:28 How fast can we go?
29:30 And how do we remove bottlenecks?
29:31 And how do we build a system by which, like, we can accelerate?
29:33 And to do that, I think PMs need to really rethink their skills.
29:38 So, like, a lot of PMs join product management because it's a safe job.
29:43 You know, they might not be good enough at the engineering task.
29:45 They might not be good enough at design tasks,
29:47 but they're really good at the consultancy.
29:50 I'm an ex-consultant.
29:50 That's why I joined the function.
29:52 I understand the customer, I can communicate to engineers,
29:55 and I can somewhat facilitate design tasks.
30:00 making. The downside is that if you're a risk adverse PM, you're not going to change your way.
30:04 So I still see, you know, very high performing PMs who don't get it, who haven't yet adopted
30:10 these core skills, who haven't changed the way that they're working because it's worked for them
30:15 so far in their career. They've been successful because of it. That is the biggest danger that
30:18 I'm seeing. And so I think that the role of the PM is going to shift and I think it's going to
30:24 shift in two directions.
30:26 PMs are going to become much more builders, right?
30:29 Because code is free.
30:30 So just like I showed, like, a product, right, that I basically built in five minutes.
30:37 It's going to require, then, like, the iteration from the product very, very quickly.
30:42 And so I think the craft and the building is going to be, like, really, really essential
30:45 versus the spec.
30:46 Like, you no longer have to write the spec anymore.
30:49 You need to actually, like, be in the product itself.
30:51 Now, a great product engineer can do that and a great product designer can do that.
30:57 The other path for product is the business side.
31:05 What engineers and designers often lack is an understanding of the context in which the
31:10 business operates and what actually matters and how we're going to win long term.
31:15 So maybe they're really good at building really good products, so give them that.
31:19 And then the product team should be focused on, like, okay, but now that we have this really good product, like, how are we competing?
31:25 How are we positioning?
31:26 How are we distributing?
31:27 How are we monetizing?
31:28 How are we actually using this to win and drive enterprise value?
31:31 And I think that, you know, even looking at opening the anthropic, like, it's a decision of strategy.
31:40 They have different strategies.
31:42 And that's actually where the PM should be really, really focused is the underlying way that we're going to win.
31:48 and playing the GM mindset.
31:51 Because you're going to have a ton of builders
31:53 that can build great products,
31:55 that can iterate on customer feedback,
31:56 that have all the context.
31:57 You've built that system.
31:58 So now focus on what actually no one can do,
32:01 which is to make sure that the product you're building
32:03 is going to have an insane amount of value in the market
32:05 and an insane amount of value for your business.
32:07 And a lot of PMs are just stuck,
32:09 like you mentioned,
32:09 they're stuck in cross-functional line meetings all day,
32:11 back to back.
32:13 And I think it's a company culture kind of thing too, right?
32:16 Like, do you make sure your PMs actually have time to build
32:18 or is it sort of like, do they have to get alignment
32:21 from 10 people to ship anything?
32:22 No it doesn seem like that the case yeah No I mean we designed the organization so that we do not have committees and we do not have sign offs You just need to prove that you added value and then you can go go for the races
32:38 I will say that, like, it's it's it's actually really, really important for PMs to carve out time to build.
32:45 And I say this not just PMs, but like managers.
32:48 I think that it's a really tough time to be a manager right now because you're managing a team whose skill set needs to change, and you might not actually have that skill set.
32:57 So I think that right now, like, going back to IC mode is paramount.
33:02 And I've done this for myself where I say, like, hey, guys, like, I'm going to be in way less meetings.
33:05 I'm going to be way less in one-on-ones.
33:07 And I'm going to be, like, I'm just going to be adopting AI tools.
33:10 I'm going to be building and vibe coding and understanding what's working, what's not working.
33:13 so that I can become more educated because this is just the beginning.
33:17 I mean, the sheer amount of changes that happened over even the last, like, three months is profound.
33:23 And I think if you're stuck in meetings, you're not going to be effective.
33:27 So definitely creating space for work.
33:30 And honestly, you know, that's also where nights and weekends come in,
33:32 which is, like, this is the year that, like, you need to really prioritize learning and growth
33:37 because no one's going to do that for you.
33:39 So, yeah, it's going to be a wild ride.
33:45 And if it's doing it the old way, your company's going to die, basically, right?
33:48 If it's doing the waterfall and all this kind of stuff, it's not going to survive.
33:52 Yeah.
33:53 Let's skip to talking about companies that are watching this.
33:57 They want to become AI-native, like Ramp, like how you guys operate.
34:00 How do you go about doing, like, you know, building systems and that kind of stuff?
34:04 Yeah.
34:04 So there isn't like one right way, but I'll share kind of what we've done.
34:12 And we've kind of like built a framework around this.
34:14 So we think about like being AI proficient in like multiple levels.
34:19 The bottom level is like people who sometimes use chat GPT.
34:24 We'll call them like the L0.
34:26 The level one is like people who build their custom GPTs.
34:29 Maybe they built a Notion agent.
34:31 Maybe they've built, they've used like clock code to like do some of these things.
34:35 Level two is people who are actually like fairly proficient.
34:39 They have been able to build an app that automates part of their job.
34:44 They have been able to commit code or feedback to other people's work.
34:49 And then level three is like the fundamental like systems builders.
34:52 And our job is to get everyone in the organization up the ladder And the way we do that is as follows The people who are still in L0 they will most likely not be at the company Because the fact is you can tell them as much
35:07 as possible. If you're not a self-starter and you don't have that growth mindset,
35:10 it's going to be very, very hard to train you out. So that's L0. The L1s, you get L2s,
35:17 L2s into L3s, and L3s basically influence the rest of the organization. And the way we do that is
35:22 Because we have a lot of public channels around people sharing what they've built.
35:29 We've made it really, really easy for anyone to adopt these things.
35:31 So we've removed any constraints around access, around tokens, around budgets.
35:35 We have, like, the setup of those tools are extremely well done.
35:41 So you have access to all the different MCPs.
35:43 You have access to all the different skills.
35:45 We even have, like, an internal repository of skills that people are deploying to.
35:48 You can pull from those.
35:48 And then we have a lot of culture around, in all hands,
35:53 around showcasing non-builders doing things.
35:57 You know, our finance team building
35:58 their own treasury management system.
36:00 Our legal team doing contract reviews.
36:02 Our marketing teams automating website creation.
36:06 To get people inspired.
36:07 And then we have office hours that people can join
36:09 to ask any questions to get set up.
36:12 We have designated experts that people can just ping
36:16 and their entire job is to evangelize,
36:18 to get you set up, to get you comfortable, to get you going.
36:21 Those are some of the principles there.
36:24 And then the other piece is just hiring and performance management.
36:28 So on the hiring front, we now have an absolute requirement
36:31 for anyone who joins the company to be somewhat proficient for these tools.
36:34 There's just absolutely no excuses.
36:35 And in the interview process, we'll have basically a dedicated session for this
36:39 where they will either, I mean, for the product team,
36:42 I literally have a session where you're going to build a product.
36:45 You're going to show me a product that you've built.
36:47 and you're going to tell me exactly why you built it, how you built it, and how it works.
36:50 Like it is a full-blown prototype.
36:52 And then we also track usage of AI across the company.
36:56 So, you know, we have – we vibe-coded this product even within the team
37:03 where we can see every other company and their full usage of tokens across Notion AI,
37:08 ChatGPT, Cloud Code, Cloud Coworker, our inspect tools, any of the internal apps.
37:15 and we can see kind of like who is actually pushing the bar
37:19 to amplify and who's not and who we need to intervene on.
37:22 Do you worry about like this cost of running out of control
37:24 or like the ROI is so clear that there no it just fucking just give everyone access Let them do it yeah I mean I haven done the ROI around like if you let say you have a person who
37:35 who's has a hundred thousand dollars salary. How many, how many tokens should this person use?
37:40 And there's debates right now around, you know, you know, uh, uh, productivity versus just like
37:46 noise and you don't actually need these things. I think right now we need to invest the budget
37:52 for people to discover.
37:54 And if we are not as efficient in that spend, that's okay.
37:57 That's our competitive advantage.
37:58 That's why we raise money.
37:59 That's why we have a pretty good war chest.
38:02 But I can safely say that we pay our employees a lot of money
38:07 and the token consumption per employee is not even close to double digits.
38:13 And I think it's not unreasonable to think that it should be higher than your salary.
38:19 because if you have agents that are able to do 10 times more work than you,
38:24 then why would you not pay them twice as much as you?
38:27 And so I think that's the way that we should be really framing it.
38:31 But yeah, I would say we're not really worried about costs.
38:35 We're mainly worried around we have the next X months or X years
38:39 where AI has not yet fully one-shotted a ramp platform,
38:44 and we need to use that to our competitive advantage
38:48 to move as fast as possible.
38:50 Yeah, I feel like a lot of the internal tools
38:51 that you showed me
38:52 are also really good for Ramp customers, right?
38:54 You can just make that available for Ramp customers.
38:58 100%.
38:58 Okay, last question, man.
39:00 So if I'm a PM or builder,
39:03 how should I think about my career these days?
39:05 Like the old climb the ladder to VP or whatever,
39:10 is that still going to work?
39:10 curve. How should I think about being employable still? I would say I think that where you should
39:20 be optimizing is not management. It is being the best builder in the world. I would say that
39:26 management is probably dead. There's always going to be value in someone giving you feedback and
39:33 coaching and being your advocate and being a team leader. But now is not the time to build that
39:38 skill set, now is the time to be very, very proficient in this new technology and to radically
39:44 improve the way that you use it. And so I would say for all the PMs out there, get really
39:54 embedded in these tools. And that's why engineers are so good at understanding what
40:00 Because they live and breathe it.
40:02 That's the first knowledge work that has been mostly automated with Coding Agent.
40:07 But it's coming for everyone else.
40:08 I mean, it's going to come for PMs.
40:09 It's going to come for designers.
40:10 It's going to come for any white-collar job.
40:13 And so I would say just get very, very proficient at using these tools.
40:18 And ultimately, your career is about impact.
40:21 And right now the impact that you can have is to ship great products faster and move more metrics for customers into the business.
40:30 And so create a lot of space to learn these things and have the beginner's mindset,
40:37 the humility to understand that the way you're doing things is not the best way.
40:42 And I think my job as a leader is just to get people to get to that aha moment.
40:47 And even my brightest PMs, I had to sit down with them
40:50 and say, we're gonna go through this workflow together.
40:52 What have you done today?
40:54 And I will show you a new way of doing it And once you get that aha moment that red pill there no coming back You like oh I get it now And it also make you a better builder because the software
41:07 you're building, if you're in B2B and even in B2C, it is going to look radically different
41:11 than what exists today. I mean, fundamentally, software is dead. It's all going to be like
41:16 coworkers. And if you haven't used coworkers in your own job, you don't understand how
41:21 that actually might look like your product a lot more than you think, right?
41:25 Yeah, you don't have the process.
41:27 That's exactly right.
41:28 Ramp itself is going to look much more like a finance co-worker
41:30 than it does tables and charts and workflows.
41:34 Yeah, I've been using open client.
41:38 It's not like CLIs.
41:40 No one wants to touch buttons anymore.
41:42 It's just like, let me talk to my co-worker and get him to do stuff for me.
41:47 So that's basically it.
41:48 Yeah, cool.
41:49 And how do you build one of those great co-workers?
41:52 Domain-level expertise is another one.
41:54 Like I think that in the past it was like,
41:56 I going to talk to customers I going to kind of understand the requirements and kind of build a product for them to do their job right But if you doing the job of your customers so that they can do other things you need to actually be an expert
42:08 Or you need to build a system by which you can ingest that expertise, right?
42:11 So accounting, like you can build an accounting workflow where they have to go and code things.
42:16 But if you're actually going to code on behalf of the accountant, you need to deeply understand the philosophy or be able to extract that knowledge.
42:22 Like how do you download, you know, CPA and all the best practices and actually bake that into your product?
42:27 So it's a very different way of thinking where fundamentally like a login in your product in the future, I think is going to be a failure.
42:34 Right. And I think that's also how we think about it.
42:36 We track the amount of time you spend in ramp and how we can actually reduce that time as much as possible, which is, by the way, the opposite of how many PMs are trained.
42:45 The Facebook and Netflix, right.
42:48 Right?
42:48 The fangs of the world
42:49 that are mainly
42:50 advertising businesses
42:51 like it is the opposite
42:53 and I think
42:54 there's going to be
42:55 reckoning for sure.
42:56 But also a very exciting time I mean you know I think it very scary and a lot of people are alarmist and everyone should be paranoid But man it an amazing time to be a builder right now especially a product manager where you have taste and vision
43:09 The time it takes
43:09 to go from your taste and vision
43:11 to a product
43:11 is shorter than ever
43:12 and I think it's a really,
43:13 really,
43:13 really exciting time
43:14 to be a builder here.
43:15 Yeah,
43:16 and I think another thing
43:17 you mentioned
43:17 is just like setting up systems
43:19 to dedicate all the bullshit work
43:21 to AI,
43:22 right,
43:22 so you can focus on stuff
43:23 that you actually enjoy doing.
43:24 Like,
43:24 that's a key part of it.
43:25 So,
43:26 yeah.
43:26 All right, Jeff.
43:27 Well, I mean, thanks for being an inspiration, man.
43:29 Like, I think hopefully every company can learn how to operate like a ramp.
43:36 Yeah.
43:36 We're just getting started.
43:37 There's also a lot of things that, you know, we're not doing well that other companies are doing super, super well.
43:42 I think, you know, part of me going on this talk is not to share that we have all of it figured out.
43:48 Most of the things that you saw here are things that we built in the last months.
43:51 So excited to keep the conversation going.
43:53 Excited to continue learning.
43:54 and really a privilege to be here today.
43:59 Thanks a lot for having me.
44:00 Yeah, thanks, Jeff.
