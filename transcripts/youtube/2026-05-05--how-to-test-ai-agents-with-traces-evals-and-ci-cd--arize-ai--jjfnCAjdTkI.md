---
video_id: "jjfnCAjdTkI"
title: "How to test AI agents with traces, evals, and CI/CD"
channel: "Arize AI"
source_url: "https://www.youtube.com/watch?v=jjfnCAjdTkI"
duration_seconds: 770
upload_date: "20260505"
availability: "public"
license: null
transcript_method: "groq-whisper-asr"
asr_models: ["whisper-large-v3"]
caption_error: "Deprecated Feature: Support for Python version 3.10 has been deprecated. Please update to Python 3.11 or above\nWARNING: [youtube] jjfnCAjdTkI: Unable to download webpage: HTTP Error 429: Too Many Requests (caused by <HTTPError 429: Too Many Requests>)\nWARNING: [youtube] Unable to fetch GVS PO Token for web_safari client: Missing required Visitor Data. You may need to pass Visitor Data with --extractor-args \"youtube:visitor_data=XXX\"\nERROR: [youtube] jjfnCAjdTkI: Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies"
segment_count: 160
relevance_categories: ["agent-operations"]
relevance_evidence: ["agents", "ai agent"]
relevance_spans: [{"category": "agent-operations", "timestamp": "0:24", "phrase": "ai agent", "text": "But with the new AI agent world, it's a little bit less straightforward."}, {"category": "agent-operations", "timestamp": "0:44", "phrase": "agents", "text": "And so we definitely knew, I think, overall at Arise that we needed a better way for folks to test agents."}]
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"asr-000.json": "7214bcbdb744230c4baa5e9aac2a6ac3730e19fd1c945d02fb11f9b4c56fe70b", "asr-001.json": "c3b248ac08190af4f55a0cba77d53b35776aa50104711293817b4955241d3088", "source-info.json": "493ce421e3fd3166de5085ae23864e636c82662fac9780297946f05caaf4a3fb"}
---

# How to test AI agents with traces, evals, and CI/CD

0:00 Hey everyone, I'm Sally Anne, a product manager at Arise.
0:04 Hey, I'm Jack. I'm an AI engineer at Arise.
0:12 We want to talk a little bit about testing and what we do to test Alex.
0:16 I think in the world of software, it's pretty straightforward.
0:18 Everybody knows how to have unit tests and our GitHub actions
0:22 to make sure our code is of high quality and nothing's breaking.
0:24 But with the new AI agent world, it's a little bit less straightforward.
0:29 And I remember the early days where testing really was me with a Google Doc, writing down queries and the answers and making changes, seeing if it worked, and then repeating that process.
0:41 And it was extremely painful, super inefficient as well.
0:44 And so we definitely knew, I think, overall at Arise that we needed a better way for folks to test agents.
0:49 And even that has evolved to where we are today with these kind of automated flows that Jack's going to show us.
0:54 But the goal is to have a set of golden answers, a set of data that you can return to anytime you're making a change to ensure that things aren't breaking.
1:02 So it really is the new testing framework for AI code versus just our traditional software.
1:10 Yeah. And, you know, I feel like especially with agents, tests are so important because our system prompt is very long.
1:20 We have dozens of tools and we found that like any small change to, you know, either the tool description, the system prompt, it can kind of throw things, you know, for a loop.
1:31 And sometimes it's hard to find those cases because, you know, you're not explicitly trying to test for those.
1:38 So we found that, you know, tests really help us kind of move faster.
1:43 And one other way for tests to help us move faster, you know, is test driven development.
1:47 So if you've been watching our other videos,
1:49 you know that we've been kind of debugging the single trace here.
1:52 The user is asking to come up with categories for my issues,
1:56 tell me what the critical issue is, and build an eval for it.
1:59 And what we found that Alex is doing is just coming up with the eval,
2:03 so it's not really telling the user what are the issues,
2:07 what are the different categories of issues.
2:09 And by using the Alex trace debugging skill,
2:12 we found that there is an instruction in our system prompt,
2:18 I think with the header called eval template output rule.
2:21 And this is what is causing the issue
2:23 where it is strongly telling Alex to not respond with any text And that is kind of causing it to not give you any information about the categorization the analysis that it did and go straight to the eval template
2:40 So one thing we can do here, I want to fix this, but now I'm nervous, right?
2:44 Because what if I change it and something down the line breaks?
2:48 How can I possibly test all these flows?
2:51 and how can I test them in a way that is consistent and reliable?
2:55 So what I can do first with this trace is I'm going to add this to a data set.
3:01 So I know that this is a trace that caused us an issue in the past,
3:06 and I'm going to add this to my testing data set.
3:09 I believe it's called main chat, trace chat.
3:12 I'm going to add this to here,
3:14 and I can see that this data set or this trace was just added here.
3:27 Okay, you can see that I just added this trace. This is the one I was just reviewing.
3:32 And because it doesn't work the way I expect it to, I can't just tell, you know, I can't just
3:38 create a test that says respond the same way it always does. It's not responding the way that I
3:44 wanted to so I'm going to create a different type of expectation here and
3:48 I've created a metadata column here called eval expected result and I can
3:52 just say you know check that the LM responds with text right after the
4:03 categorize and assign tools, the text should contain the categories that come from those tools.
4:22 So basically, I'm trying to set an expectation that it actually responds after these tools,
4:30 and not much later on, but right after these tools.
4:34 And I can just create this kind of eval with free text, right?
4:39 Because again, evals use LLMs to actually check the results.
4:44 So I don't have to come up with,
4:46 hey, here's the exact JSON data format.
4:49 It should look exactly like this
4:50 because that also makes the test brittle
4:52 and it doesn't quite capture the essence
4:54 of what we trying to accomplish here So I going to update this and now I have this saved example So the real question is how do I change this code in a way that passes this test
5:11 And how do I actually run this test? So what we did was we created a script because Alex is
5:18 pretty complex. We can't just run it in a playground environment. So the script
5:24 on the back end, in fact, looks pretty simple.
5:29 You know, it's only a few hundred lines,
5:30 and it's using our existing code.
5:34 And I will run the script, you know,
5:37 with an only look for the reasoning annotations example,
5:42 so that we're only running a single example here.
5:44 So I'm going to run it.
5:50 And it'll take a few seconds to kind of get started,
5:53 but you can see that it found the one row that does have the reasoning annotations,
5:58 which is the one that we are trying to test.
6:05 And as Alex is running in the background, we're collecting the responses,
6:10 and ultimately we're going to upload this to Arise as an experiment.
6:16 And by using an experiment, this allows us to run evals against it,
6:19 which will ultimately tell us, you know, what the, is the LLM doing what we expect it to do.
6:29 I think the other powerful thing about the experiment too is we can track it over time.
6:32 So we're able to see over time as we're developing the results of those evals
6:35 and really easily identify if there's a major drop.
6:38 Because you never really expect that performance will be 100%.
6:41 That's a little suspicious, but we do want to make sure we're getting as high as possible.
6:45 And so having that baseline to compare to is something that's really powerful.
6:48 And I also want to call out the fact that, you know, our data set is created of our real production traces.
6:53 Of course, we can come up with any synthetic data, maybe even using Alex.
6:56 But I think it's powerful as people are collaborating that, you know, I can go grab an example trace that went wrong, add it to our data set, and, you know, we can continue to work all on the same tests.
7:06 Yeah.
7:06 So, you know, we'll touch on this a little bit later, but we found that, you know, tests are, you know, nice for testing your application, but they're a great way to actually communicate amongst your team, right?
7:15 So when it was just Sally and I, it was pretty easy to say, hey, this doesn't work, look at my computer.
7:21 But as our team has grown and as our agent has gotten a lot more complicated it gets pretty hard when someone just like hey this doesn work Well I don know what steps you took to get there
7:35 Did you phrase the prompt in a certain way?
7:39 And that kind of communication ultimately leads
7:42 to kind of this back and forth of,
7:44 hey, it works on my computer.
7:45 Why isn't it working on your computer?
7:47 So we found that these tests were getting exact traces.
7:50 Here's the exact data that was the input
7:54 that caused the issue for me.
7:55 It makes it so much easier to communicate.
7:59 This is the issue.
8:00 Here's my eval and what I expect to happen.
8:03 And now we can kind of use this much more concrete language
8:07 to talk about bugs,
8:10 talk about flows that we want to have.
8:12 And it really makes, you know,
8:14 this team environment a lot more,
8:18 it makes this team environment
8:19 a lot easier to communicate amongst.
8:21 So here the test runner has completed, and I can see that there is one new data set with a new example.
8:34 And again, you know, I can look at this response and kind of, okay, like read through it.
8:41 But you can see that this response is pretty verbose.
8:44 It's how many lines?
8:45 300 and almost 50 lines of code, right?
8:48 And it's all in JSON.
8:49 So, you know, I could read through it and see does this do what I expect or not.
8:55 But I can also run the evaluator.
8:57 So this evaluator is incredibly simple.
9:01 It just says, you know, does the output, you know, follow the expected response, right?
9:06 And remember, this is the column that I wrote the expectation that it will tell you,
9:11 it will explain to the user the categories before creating eval.
9:14 So I'm going to run an eval on this experiment.
9:17 and it'll take a second to run.
9:22 Okay, and you can see here it ran
9:25 and it correctly identified the responses incorrect, right?
9:29 So remember, this was a failing example,
9:32 but, you know, as with TDD,
9:34 you always want to start with a failing example
9:35 because you need to test that your test is correct.
9:39 And it kind of explains and says,
9:42 after categorize and assign the element,
9:45 LLM does not immediately respond with text.
9:47 Instead, it continues with further tool calls.
9:51 So this is kind of actually a great explanation of what the problem is,
9:55 probably better than I can explain it myself.
10:00 And, you know, if you recall from the trace debugging tool, it'll say, it said there was a critical rule, and I'm going to look over here.
10:10 It says there's a rule that says eval template output rule.
10:14 So I'm going to look at my code and see, oh, okay, eval template output rule.
10:19 This is the exact system template that we use.
10:21 And it says when a tool returns the eval template, do not restate or reformat it.
10:26 Only output a finished call with no text.
10:28 and it says that this is the rule that is causing the problem.
10:33 And, oh, look, didn't expect this to show up on the demo,
10:36 but it looks like the kid blame is on me.
10:40 So I'm just going to delete this rule and save it.
10:45 And now what I'm going to do is I'm going to rerun the exact same test.
10:50 And hopefully this is the rule that actually is causing the issue
10:55 and this is the only thing that is needed to fix it.
10:57 so I'm going to let it run. Okay, great. So the run just completed. It says, you know,
11:04 log the results to a new experiment. So now let's look at this new experiment here. I'm going to go
11:10 back and you can see this is the newest experiment And again I can look at this I mean you know a lot of text So what I just going to do is run the eval and let the LLM do the hard work of reading through all that response for me Okay so it looks like it still incorrect It says
11:32 the LLM output does not respond with the text immediately, but you can imagine this isn't
11:39 going to be as simple as deleting a couple lines of code or of the prompt. So this is now a way
11:46 for me to continue to iterate and try to figure out, you know, what exactly do I need to change
11:50 in order to get this, you know, eval to pass. And, you know, as once it passes, now this is part of
11:58 our data set that we use to test all future changes to the main chat. So, you know, our goal
12:05 is to collect, you know, maybe dozens of examples, if not more, of ways that, you know, we want the
12:10 alarm to behave and function. And, you know, hopefully as we add more functionality, as the
12:16 system gets more complex, you know, we keep those tests around and make sure that, you know, our
12:21 existing core functionality is still working as expected. Yeah. And this is something that we can
12:26 integrate directly into Git. You have these running automatically so that at any time that anybody,
12:30 you know, is making a change, these are automatically running and Jack and I can
12:33 feel confident that things are going to stay of high quality. Especially important as your teams
12:38 are growing. A lot of people are developing on top of each other. We always want to make
12:42 sure that we're never pushing anything that's going to impact the user's experience.
