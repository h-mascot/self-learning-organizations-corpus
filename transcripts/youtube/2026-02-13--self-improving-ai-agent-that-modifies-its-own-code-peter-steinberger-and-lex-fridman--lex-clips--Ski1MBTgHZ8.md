---
video_id: "Ski1MBTgHZ8"
title: "Self-improving AI agent that modifies its own code | Peter Steinberger and Lex Fridman"
channel: "Lex Clips"
source_url: "https://www.youtube.com/watch?v=Ski1MBTgHZ8"
duration_seconds: 216
upload_date: "20260213"
availability: "public"
license: null
transcript_method: "groq-whisper-asr"
asr_models: ["whisper-large-v3-turbo"]
caption_error: "YouTube captions unavailable; recovered from cached signed audio URL."
segment_count: 52
relevance_categories: []
relevance_evidence: []
relevance_spans: []
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"asr-000.json": "7adffd0f5c678929c35f7e03c24bd5a500ec2a0bb38aff633e9db24c8b8bcbcc", "source-info.json": "0b23c1ce14e1116fb30e7f0e6395f1843d41a03df714e1d07ac5241a923b039a"}
---

# Self-improving AI agent that modifies its own code | Peter Steinberger and Lex Fridman

0:00 I wanted it to be fun.
0:04 I wanted it to be weird.
0:06 And if you see all the lobster stuff online,
0:10 I think I managed weird.
0:14 Even for the longest time,
0:16 the only way to install it was
0:20 git clone, pmpm build, pmpm gateway.
0:24 You clone it, you build it, you run it.
0:26 and then the
0:28 agent, I made the agent very aware
0:31 like it knows that it is
0:33 what its source code is
0:35 it understands how it
0:37 sits and runs in its own harness
0:40 it knows where documentation is
0:42 it knows which model
0:44 it runs, it knows if you
0:46 turn on verbose or
0:47 reasoning mode
0:49 I wanted it to be more human-like
0:51 so it understands its own
0:54 system that made it very easy for an agent
0:55 to, oh, you don't like anything, you just prompted it to existence.
1:00 And then the agent would just modify it on software.
1:04 You know, we have people talk about self-modifying software, I just built it.
1:08 I didn't even plan it so much, it just happened.
1:14 Can you actually speak to that?
1:15 Because it's just fascinating.
1:17 So you have this piece of software, a certain TypeScript,
1:21 that's able to, via the agentic loop, modify itself.
1:26 I mean, what a moment to be alive in the history of humanity,
1:31 in the history of programming.
1:33 Here's the thing that's used by a huge amount of people
1:36 to do incredibly powerful things in their lives,
1:39 and that very system can rewrite itself can modify itself Can you just speak to the power of that Isn that incredible When did you first close the loop on that Oh because that how I built it as well
1:55 Most of it is built by codecs, but oftentimes when I debug it, I use self-introspection so much.
2:04 It's like, hey, what tools do you see? Can you call the tool yourself? Oh, whatever do you see?
2:08 read the source code, figure out what's the problem.
2:12 I just found it an incredibly fun way
2:14 that the very agent and software that you use
2:19 is used to debug itself so that
2:22 it felt just natural that everybody does that.
2:26 And that it led to so many
2:27 pull requests by people who never wrote software.
2:31 I mean, it also did show that people never wrote software.
2:35 I call them prompt requests in the end.
2:38 But I don't want to pull that down because every time someone made the first pull request is a win for a society.
2:46 It doesn't matter how shitty it is.
2:50 You've got to start somewhere.
2:53 I know there's this whole big movement of people complain about open source and the quality of PRs and a whole different level of problems.
3:00 But on a different level, I found it very meaningful that I built something that people love to think of so much that they actually start to learn how open source works.
3:30 Thank you.
