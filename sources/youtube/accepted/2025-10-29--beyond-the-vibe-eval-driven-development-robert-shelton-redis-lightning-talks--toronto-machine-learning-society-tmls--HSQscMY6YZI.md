---
schema_version: 1
platform: youtube
stable_id: HSQscMY6YZI
title: "Beyond the Vibe: Eval-Driven Development | Robert Shelton, Redis | Lightning Talks"
publisher: "Toronto Machine Learning Society (TMLS)"
canonical_url: https://www.youtube.com/watch?v=HSQscMY6YZI
published_date: 2025-10-29
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via groq-whisper-asr"
rights_status: third-party
rights_holder: "Toronto Machine Learning Society (TMLS)"
content_sha256: 2c309f037abf17b504215f4c8f18ffbf5e32d3c4dd03072baa5042539c6d3d61
duration_seconds: 306
transcript_source: groq-whisper-asr
availability: public
license: null
caption_error: "Deprecated Feature: Support for Python version 3.10 has been deprecated. Please update to Python 3.11 or above\nWARNING: The extractor specified to use impersonation for this download, but no impersonate target is available. If you encounter errors, then see  https://github.com/yt-dlp/yt-dlp#impersonation  for information on installing the required dependencies\nERROR: Unable to download video subtitles for 'en-orig': HTTP Error 429: Too Many Requests"
segment_count: 76
relevance_categories: ["feedback-systems","ai-native-company","agent-operations"]
relevance_evidence: ["ai-native","eval driven","feedback loop"]
relevance_spans: [{"category":"feedback-systems","phrase":"feedback loop","text":"And then automate your feedback loops.","timestamp":"2:17"},{"category":"ai-native-company","phrase":"ai-native","text":"there's people who are building AI-native apps","timestamp":"2:20"},{"category":"agent-operations","phrase":"eval driven","text":"So today we're going to be talking about eval driven development which is kind of","timestamp":"0:00"}]
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"asr-000.json":"ffb8d884079d517185442fb69565725eebcac3d25639a7e91cf67d3c7cdd0a34","source-info.json":"172cdde9956d8500b58b6c13a4fa8f510b641a1924b8a25d7d50762ddf32bca3"}
raw_path: raw/youtube/2025-10-29--beyond-the-vibe-eval-driven-development-robert-shelton-redis-lightning-talks--toronto-machine-learning-society-tmls--HSQscMY6YZI
asr_models: ["whisper-large-v3"]
---

# Beyond the Vibe: Eval-Driven Development | Robert Shelton, Redis | Lightning Talks

0:00 So today we're going to be talking about eval driven development which is kind of
0:12 a controversial topic right we're all wondering how to do this and this is
0:16 some of the insights I've gained from working with a bunch of different
0:19 customers on this topic. So the problem is that you know with probabilistic
0:25 systems you can't map the entire input space you can't just do simple testing
0:29 for pass fail in your pipelines. You need evaluations, which moves us to a paradigm of
0:34 grading versus just testing. What happens is we get a buffet of different solution patterns that
0:40 you've seen on LinkedIn that a bunch of people want to try, but improvement becomes incredibly
0:44 opaque. So customers I've worked with, they was like, oh, we need to do this, right? And I'm like,
0:49 well, does it improve? And they don't really know. This leads to a trap where everyone's looking for
0:53 like the fanciest new metric that's going to automatically monotonically increase in their
0:58 application to make everything better. But what we find is there's usually not one metric that's going to do it. And while all models are wrong, some are useful.
1:08 So what I want to present today is what might be a useful evaluation and how to select this for the type of apps you building So what does a useful evaluation look like To me a useful evaluation codifies the base
1:23 expectations of a user's experience in a production environment before, you know,
1:28 in a test environment before production, and it can capture some aggression and account for some
1:33 future needs. So why does this matter? It helps us separate signal from noise. At enterprise scale,
1:40 I find that engineers are largely inconsistent.
1:43 And so we have very distributed teams
1:45 and they'll be implementing different features.
1:47 It's hard to know how that all impacted
1:49 a fundamental probabilistic system.
1:51 This may be less important
1:52 if you're still figuring out product market fit
1:54 and you need to get things out of the door.
1:55 You'll see on LinkedIn,
1:56 not everybody loves eval-driven development.
1:59 Some of that is valid.
2:00 If you're really early stage
2:01 and you don't know where you're at with your team,
2:04 you can move quick.
2:05 But if you are in the evaluation stage,
2:07 here are three bullets I want you to remember.
2:09 One, know the app.
2:11 Know what you're going to build.
2:12 Two, model intended usage with data.
2:14 Data is still king. Record data.
2:17 And then automate your feedback loops.
2:19 So when you're knowing your app,
2:20 there's people who are building AI-native apps
2:22 where users traverse a smooth space,
2:25 whereas hybrid apps
2:27 where people are moving through a striated space What I mean by striated space is the outcomes of your AI system are n There n number of outcomes You can label this in data and this is really important
2:39 to understand with what you're evaluating. You don't use the same evaluation metrics for both.
2:45 So when we're getting into striated apps like a RAG system, how would you evaluate that? Well,
2:51 I know what some of my outputs might look like, so I can use more traditional metrics like precision
2:57 and recall an F1 score to monitor retrieval.
3:00 There's more advanced metrics for the generation
3:02 like faithfulness or relevancy,
3:04 but I want to attribute this to my data as much as possible
3:08 because it's a finite set of outputs from retrieval.
3:11 I know that and I can model that in my data.
3:14 So I want to leverage that.
3:15 For smooth systems,
3:17 what I recommend is taking a teaching approach.
3:20 Like in the same way we want our students to be creative
3:23 to some extent,
3:24 we want our LLM systems to be creative.
3:26 They're moving through some sort of space.
3:28 And so here we always collect simulated
3:31 or collected examples with a rubric and give us a grade.
3:35 So this gives us a way of evaluating,
3:36 hey, what was system A versus system B like,
3:40 but helps us measure also to a rubric of creativity.
3:44 Because the reason you using LLMs is to be creative So in an agent system we built out which works through Slack we actually have this automatically built into our pipeline So as ML practitioners
3:55 and you're building things that need to work in the real world, we have every time any signal is
4:00 recorded, it's like a thumbs up, thumbs down on our system, it goes to an S3 bucket. And every
4:05 time we merge to main, we run our teacher bot to make sure that the last thing that works is either
4:11 up or down from where we were. But we can't model all that at once. So to recap, identify what type
4:17 of app you're building, whether it's smooth or striated. Document. You need data. Record how
4:23 people are going to use your app or intend to use your app. And finally, quality is still a function
4:28 of creativity and intention. There's no one metric that's just going to monotonically improve your
4:33 app. With that, I really appreciate your time. Redis is at booth 37 if you want to talk more to me.
4:43 And then you can check out my email or GitHub. I've written an open source Python package for
4:49 doing evaluations on information retrieval tasks. So if you're working on a search use case or
4:55 something of that nature, there's a package for that. Thanks for your time, everybody.
5:03 you
