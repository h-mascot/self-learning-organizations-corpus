---
schema_version: 1
platform: youtube
stable_id: WW-v5mO2P7w
title: "Build Self-Improving Agents: LangMem Procedural Memory Tutorial"
publisher: "LangChain"
canonical_url: https://www.youtube.com/watch?v=WW-v5mO2P7w
published_date: 2025-02-18
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via groq-whisper-asr"
rights_status: third-party
rights_holder: "LangChain"
content_sha256: a92240b3f472c3d201e7ea123795059379b3ea91030c59bf75d6a1d052527de4
duration_seconds: 407
transcript_source: groq-whisper-asr
availability: public
license: null
caption_error: "YouTube captions unavailable; recovered from cached signed audio URL."
segment_count: 97
relevance_categories: ["agent-operations"]
relevance_evidence: ["agents"]
relevance_spans: [{"category":"agent-operations","phrase":"agents","text":"for helping your agents learn and adapt as they work. In this video, we will show you how to add","timestamp":"0:04"}]
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"asr-000.json":"ff230be829581449c1adb3a19ef07f327fa5b8f78df2efc3d9302e1e4afffa25","source-info.json":"24beadf102b5f9166b1234ab00febaeb2d1a6334e91e185d7c25bec520396c26"}
raw_path: raw/youtube/2025-02-18--build-self-improving-agents-langmem-procedural-memory-tutorial--langchain--WW-v5mO2P7w
asr_models: ["whisper-large-v3"]
---

# Build Self-Improving Agents: LangMem Procedural Memory Tutorial

0:00 Hi all, Will here. This week we're excited to launch the Langma MSDK, a library of utilities
0:04 for helping your agents learn and adapt as they work. In this video, we will show you how to add
0:09 procedural memory to your agents so they can learn instructions, rules, and other procedures
0:14 that dictate how it should respond and act in given situations. By the end of this tutorial,
0:19 you'll be able to create an email assistant agent that's able to learn from feedback.
0:24 By submitting feedback, the agent will update its own prompt and learn new instructions
0:29 inferred from the user. The updated prompt can live in the memory. You can see that it's able
0:33 to learn these procedures so that anytime you have a new conversation, it's able to act on this new
0:38 behavior. You can see from the result that it's able to learn this. Procedural memory is great
0:42 for learning rules, instructions, and other things that dictate the core behavioral tendencies.
0:49 Let's build an email assistant agent to demonstrate how procedural memory works.
0:53 We'll start by installing Langman and Landgraf and then set up our initial instructions for the agent.
0:59 These can be learned over time as we'll demonstrate later.
1:02 We will manage the prompt for now in the long-term memory store,
1:05 just because it's convenient to be accessing this across different threads.
1:08 Now let's create the agent itself.
1:10 It will have a single tool called draftEmail.
1:13 This will be a placeholder that gets it to actually write the email as a response,
1:17 and we'll have the prompt function.
1:19 The prompt function takes the state,
1:21 can access the long-term memory store,
1:23 and prepares the list of messages to send directly to the LLM.
1:26 In our case, we'll get this instructions list, get the prompt out of it, and then put that in the system prompt that will pass to the LLM.
1:33 We see the agent doesn't yet know my name.
1:35 It has a pretty simple email structure Suppose I wanted to always include my name in the sign because it is my personal email assistant Whenever it doing meeting requests it should offer to send a Zoom or Google Meet link Let have our agent learn from feedback We import the prompt optimizer from
1:50 LangMem, initialize it using Cloud Sonnet to drive the optimization process. We'll run the optimizer
1:55 itself. It's taking the conversation and optional feedback and using that to infer what type of
2:00 instructions it should be learning to include in the prompt for later interactions. Here we've
2:05 passed in feedback saying to always sign off as my name, but this information also could be found
2:10 within the existing conversation history. That's very common with chat interactions. Since we're
2:16 using an LLM to drive this optimizer, it should glean this type of implicit feedback from the
2:21 conversation history. We call them trajectories because it could include any series of operations
2:25 for your agent, including tool calls and other information. Let's print this out to see what
2:29 It responded.
2:30 You see the new learned prompt.
2:32 It's able to notice that we implicitly condone the existing structure, saying to use clear, concise language and to always sign off with my name now.
2:41 For meeting requests, see it has this conditional rule.
2:44 It says to clearly state the proposed time and to offer these two things.
2:48 So it's able to learn these different things and propose a new instruction structure.
2:51 And it even provides a few shot example or give the example across.
2:55 You can control the parameters of the optimizer if you think this is too verbose or not verbose enough.
2:59 to give the optimizer more time to think
3:01 or more constraints around what type of updates to make.
3:04 We'll put this back in the store
3:05 and then run our process again.
3:07 We see now that it signs off with my name
3:09 and offers to use whichever meeting platform
3:13 the recipient prefers.
3:14 If it's drafting an email to a different type of content,
3:17 it should be smart enough to know when the procedure should be followed or not You see it was able to infer that it should still sign off using my name but since this isn about a meeting follow it doesn need to actually include any information
3:29 about how we should be following up.
3:31 Simple, right?
3:32 So we showed how to update the procedural memory
3:34 for a single agent, but what if you have multiple agents
3:36 all working in concert?
3:38 We're going to use Landgraf's Multi-Agent Supervisor Library
3:41 to build a multi-agent system and then show how you can be
3:44 improving the procedural memory for both agents
3:47 in a single pass.
3:48 We'll install the LandGraph Supervisor package to get this additional inform,
3:52 and then we'll create two working agents in a similar fashion to before.
3:55 The first is our email agent, which looks the same.
3:58 The only changes we've made is we've changed the key of the memories here to be the email agent
4:02 so we can differentiate the instructions between this and our social media or Twitter agent.
4:06 And then we've created a second one in a similar style that's able to send tweets.
4:12 Please make sure you update the keys so that their instructions aren't mixed.
4:15 Next, we'll create our supervisor agent.
4:17 We'll import from the LandGraph supervisor package and initialize it with our two agents we created above.
4:23 Our prompt doesn't have to be very specific, since it should know when to route to the email or tweet assistance depending on content.
4:29 We'll repeat our experiment above, asking it to draft an email to joe at langchain.dev.
4:33 And then we can see the sub-agent has responded, showing what type of content it set.
4:38 Now comes the fun part. Let's say we want to leave the same feedback.
4:41 We always want to sign off emails from William for meeting requests.
4:45 We will offer to schedule on Zoom or Google Meet.
4:47 We'll use the multi-prompt optimizer this time,
4:49 which is designed to pick which prompt
4:51 in a multi-agent system it needs to update
4:53 based on feedback and conversation history.
4:55 In an arbitrary multi-agent system,
4:58 the prompt relationships can get a bit complicated In order to have a more reliable attribution of blame we going to provide more information about the prompt namely when to update the prompt in a given system and how to update it if so
5:11 We'll use a prompt type, which is just a typed dictionary, by providing a name to the prompt, exactly what it is currently, the update instructions, and when to update.
5:21 We'll fetch these two prompts and initialize them accordingly.
5:24 If you look at the results, you can see that the tweet prompt hasn't been updated, but the email prompt itself has.
5:30 It again has learned to be incorporating my preferred sign-off, as well as in these particular situations, to offer multiple options for meeting scheduling.
5:39 Put it back in the store and then rerun the system.
5:41 We should be able to see whether the desired prompt effects are useful.
5:45 As you can see, it's learned how to sign off its emails and is also offering multiple options for this meeting schedule.
5:51 The multi-prompt optimizer is useful in the very common situation where you might have outcome level supervision, either from end user feedback or other scenarios, but you want your system as a whole to be able to learn and make improvements.
6:03 What works under the hood is that it takes this prompt context as well as the feedback and ongoing trajectories and learns which prompts contributed to the overall outcome.
6:12 It then uses that optimizer loop to learn what updates are necessary to make this improvement and returns those suggested prompt improvements.
6:19 And that's all you have for today. In this tutorial, you used LangMEM's prompt optimizer
6:24 in order to learn instructions based on user feedback and conversation history.
6:28 You then created a multi-agent system and used the multi-prompt optimizer in order to learn
6:32 updates to a multi-agent system based on end-user feedback. Procedural memory is useful for teaching
6:37 your agents how to accomplish tasks, especially when those instructions are conditional. For more
6:41 information about this and other types of memories, check out the LangMEM docs in our other videos.
6:45 Catch you next time.
