---
schema_version: 1
platform: youtube
stable_id: RoaPvj9Ovug
title: "Self Improving Agents in 5 Minutes"
publisher: "Developers Digest"
canonical_url: https://www.youtube.com/watch?v=RoaPvj9Ovug
published_date: 2026-04-04
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via groq-whisper-asr"
rights_status: third-party
rights_holder: "Developers Digest"
content_sha256: a4282edb8ff4b588e43bc0323717761e68611dcdff6132b470478c848b4c63f4
duration_seconds: 307
transcript_source: groq-whisper-asr
asr_models: ["whisper-large-v3"]
availability: public
caption_error: YouTube captions unavailable; recovered from cached signed audio URL.
raw_files: {"asr-000.json":"3a1bdea8c5d16c4109546aea6d5566345232517912ad6954e105bf3b1b2c52d7","source-info.json":"a9e2a5bf87c260c9dec501f6ba7bb0e2debe63275e2d7f0486cfbc3d2166e748"}
raw_path: raw/youtube/2026-04-04--self-improving-agents-in-5-minutes--developers-digest--RoaPvj9Ovug
relevance_categories: ["agent-operations","recursive-improvement"]
relevance_evidence: ["agents","ai agent","self-improving"]
relevance_spans: [{"category":"agent-operations","phrase":"ai agent","text":"And if you're not familiar with auto research, the idea with this was basically give an AI agent a small but real LLM training setup and let it experiment overnight.","timestamp":"0:33"},{"category":"agent-operations","phrase":"agents","text":"In this video, I'm going to be taking a look at self-improving agents, specifically how a new project extends ideas from Andre Karpathy's auto research into something that is arguably even much bigger.","timestamp":"0:00"},{"category":"recursive-improvement","phrase":"self-improving","text":"In this video, I'm going to be taking a look at self-improving agents, specifically how a new project extends ideas from Andre Karpathy's auto research into something that is arguably even much bigger.","timestamp":"0:00"}]
rights_note: YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed.
segment_count: 64
---

# Self Improving Agents in 5 Minutes

0:00 In this video, I'm going to be taking a look at self-improving agents, specifically how a new project extends ideas from Andre Karpathy's auto research into something that is arguably even much bigger.
0:11 Now, if you've been following the channel, I cover things like self-improving skills, continual learning, as well as how to run clogged code autonomously.
0:17 And one of the interesting things and areas that more and more people are starting to look at is this idea of actually autonomously improving the agent harness themselves.
0:26 Now, I saw this post from Kevin Gu on X, and Kevin put out a really interesting project called AutoAgent, which I'll link within the description of the video.
0:33 And if you're not familiar with auto research, the idea with this was basically give an AI agent a small but real LLM training setup and let it experiment overnight.
0:42 It modifies the training code, trains for five minutes, check if the results have improved, and then it decides whether to keep or discards the results, and it will repeat that process.
0:50 And effectively overnight, what you can do is you can determine based on these experiments, is this actually a value?
0:56 Auto agent, instead of optimizing the training code, what it optimizes for is the agent harness itself.
1:01 So effectively, it's sort of like a meta agent that experiments on different tasks of the agent's prompts, tools, as well as orchestration.
1:08 Now the results of this are really impressive which I touch on in just a moment But all in all the pattern is effectively the same loop but just on different scopes Auto research will optimize the training code whereas auto agent will optimize the agent harness itself
1:21 The looping mechanism is effectively identical, but the implications are very different.
1:25 Now, one thing that people really liked with Carpathia's setup within auto research, it was very simple.
1:30 It was effectively a few different files, one GPU, as well as a five minute training budget.
1:35 There was the prepared pie, which was fixed.
1:37 This was the data prep, the tokenizer, the data loader.
1:40 Nobody effectively touched this. There was the train pi, and this was what the agent actually edits.
1:45 The full GPT model optimizes the training loop, architecture, hyperparameters, batch size.
1:50 Everything was effectively fair game within that file.
1:54 And then the program MD is what the human edits.
1:56 And this file has the instructions, what to tell the agent, how to try, what to avoid, how to evaluate the different results.
2:02 And the key insight here was you're not writing Python anymore.
2:05 You're effectively just writing the markdown file.
2:07 You're programming in natural language.
2:10 The human programs the agent and the agent programs the code.
2:13 And then the agent will just run all night.
2:15 And Karpathy calls this the story of how it all began, because the implication is this
2:19 is what research looks like from here on out.
2:22 Now, with auto agent, it takes that same research loop, but it makes it work for any domain,
2:26 not just ML training.
2:28 Now the architecture with this it a bit different Effectively you have a meta agent and a task agent The task agent is one for doing the actual work on whatever domain you care about It starts with almost nothing
2:39 It's just a bash tool.
2:40 It reads the program.md for research direction.
2:44 Then it experiments with the agent.py, which is the task agent's code.
2:47 And then within auto agent, there's an adapter where it connects to whatever benchmark you're evaluating against.
2:52 And the meta agent will spin up thousands of parallel sandboxes,
2:55 sandboxes, run the task agent on evaluation tasks, read the results and the reasoning traces, and
3:01 decide what to keep and what to revert. Very similar, same type of idea to auto research.
3:06 Effectively, again, overnight, the agent has domain-specific tooling, verification loops,
3:11 orchestration logic, things that nobody programmed that it all discovered autonomously by the meta
3:17 agent just by running in a loop. And now, like they show within the repos, they have two different
3:21 examples. They show spreadsheet bench as well as terminal bench. And you can see when it goes
3:25 through these different iterations, how it's actually improving the harness itself.
3:29 As it verifies, this is actually a better result than the previous one.
3:33 It would go and continue building off of that.
3:35 Here are some of the results with a very similar idea to what
3:38 Carpathia had within auto research.
3:40 Now within auto agent, the loop is effectively the same.
3:42 It going to edit the agent harness similar to how auto research would edit the train pie It would run on those tasks and then it would check the benchmark and then repeat Effectively the same loop it just a different target What really interesting with this and why it matters is arguably every domain needs a bit of a different harness And the harness
3:58 engineering in and of itself requires someone who understands both the domain as well as how the
4:02 models behave. And the thing with companies is oftentimes they don't have one workflow. Being
4:06 able to optimize different harnesses that might live at different parts of the stack or different
4:10 parts of the process, this allows you to potentially explore areas where you might have an optimized
4:14 harness where you can run with cheaper models that are geared towards specific tasks instead
4:19 of just having one monolithic harness that tries to do everything. I think this is just one of
4:23 probably many projects of what we're going to see, but the domain experts are going to be really
4:28 valuable with these types of projects because they're going to be able to define what are good
4:32 instructions for the outcomes that you want from these different meta agents. And the interesting
4:36 thing with this is it's arguably just another level of abstraction. Similar to code, we used
4:41 to write the actual syntax of all of the different code. And now increasingly more and more of code
4:45 is just written by AI models. A similar thing potentially could happen with harnesses where
4:50 instead of actually engineering the harness manually, we could just let agents engineer
4:54 the harnesses themselves, effectively define what success looks like, point the meta agent at it,
4:58 and then come back in 24 hours and see the results. That's it for this video. If you found
5:02 this video useful, please like, comment, share, and subscribe. Otherwise, until the next one.
