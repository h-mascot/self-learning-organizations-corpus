---
schema_version: 1
platform: youtube
stable_id: AkadGXzDqBw
title: "NOT-Recursive NOT-Self Improvement: autoresearch isn't SuperAI's next step"
publisher: "Internet of Bugs"
canonical_url: https://www.youtube.com/watch?v=AkadGXzDqBw
published_date: 2026-05-14
content_type: transcript
status: accepted
relevance_status: relevant
provenance: "YouTube transcript retained from the goal/youtube worker via groq-whisper-asr"
rights_status: third-party
rights_holder: "Internet of Bugs"
content_sha256: e96b97874dc57a65bc2708342f7a743501e33d83db584fff78f58bea142a07be
duration_seconds: 392
transcript_source: groq-whisper-asr
asr_models: ["whisper-large-v3"]
availability: public
caption_error: YouTube captions unavailable; recovered from cached signed audio URL.
raw_files: {"asr-000.json":"b2a13b8a44a0563af0b1cf8279d01b850831a7f595601e057a539a2e38c029b0","source-info.json":"f6943323dd0d8390f9680db5e71514388578e010acdbb54b33082c831bbed36c"}
raw_path: raw/youtube/2026-05-14--not-recursive-not-self-improvement-autoresearch-isn-t-superai-s-next-step--internet-of-bugs--AkadGXzDqBw
relevance_categories: ["agent-operations"]
relevance_evidence: ["agents"]
relevance_spans: [{"category":"agent-operations","phrase":"agents","text":"A lot of people say that coding agents like Cloud Code can write code better than humans.","timestamp":"3:55"}]
rights_note: YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed.
segment_count: 102
---

# NOT-Recursive NOT-Self Improvement: autoresearch isn't SuperAI's next step

0:00 All right, so today I'm going to talk about non-recursive, not self-improvement.
0:03 The idea of AI recursive self-improvement is a key concept in a lot of what will happen with AI in the future kind of scenarios.
0:10 There's been a lot of chatter about it recently because of an AI tool that was recently released,
0:14 and it's made it quite clear that either many people have no idea what recursive self-improvement actually means,
0:20 or they don't care what it means and are just trying to use it to get more clicks.
0:23 As usual, I'm concerned that people who don't have the skills or time to understand in detail what's going on with AI
0:28 will see the stupid headlines and they'll get the wrong idea.
0:31 And of course, as usual, that would be bad
0:33 because the worldview that those headlines and the clickbaiters amplify is utter bullshit.
0:44 This is the Internet of Bugs. My name is Carl.
0:46 I've been a software professional since the late 1980s
0:48 and I'm trying to do my part to make the Internet a safer, less buggy place.
0:51 You can find out more about me on InternetofBugs.com.
0:54 The trigger for this current wave of AI's improving itself rhetoric
0:56 is a project called Auto Research, which was announced a month or so ago,
1:00 which led to some crazy takes showing up before long.
1:03 And many of the crazy takes are confusing what Auto Research is doing
1:06 with a talking point from the AI Doomer and AI Accelerationist playbook.
1:10 But they're not the same at all.
1:12 So I posted an essay on my sub stack about how the AI Doomers make completely impossible claims
1:16 about how powerful their mythical super AI would be if it were possible, which it isn't.
1:21 I'll put a link to that below.
1:23 The concept of recursive self-improvement didn't belong in that essay
1:25 because unlike much of the totally unhinged Doomer crap,
1:29 recursive self-improvement might actually be possible,
1:33 maybe at least theoretically However it just a sci thought experiment and there no actual evidence yet it could really happen and it certainly not happening now Despite what these people hyping auto would lead you to believe
1:45 The idea behind recursive self-improvement
1:47 is that people make an AI that's smarter than humans,
1:49 or at least better at AI research than humans,
1:52 and that AI in that AI creates newer, even smarter AI,
1:55 which in turn creates another AI even smarter than that one,
1:58 and so on and so forth.
1:59 This is the rationale that the Doomers used to try to justify super AI
2:02 by claiming it will be so far beyond our understanding
2:04 because it was built by an AI smarter than an AI that's smarter than an AI
2:08 that's smarter than an AI that's smarter than an AI that's smarter than an AI
2:10 that's smarter than an AI that's smarter than an AI that's smarter than us.
2:13 Or something to that effect. You get the idea.
2:15 To get some concept of how seriously you should take this idea,
2:18 this is literally the inciting incident of the Hitchhiker's Guide to the Galaxy series.
2:23 So this new auto-research tool that everyone is hyping up,
2:26 it's not that at all.
2:28 It's a pretty simple tool.
2:29 You give it access to some code.
2:31 you give it a way to measure a number that indicates whether things are getting better or worse.
2:35 And then it just runs in a loop and it makes them tweak to the code that you give it.
2:38 It runs the measurement. And if the measurement is better, it keeps the change.
2:41 If the measurement isn't better, it rolls it back to the previous version.
2:43 Does this over and over in a loop until you stop it or you burn through all your AI token budget,
2:47 which can happen pretty quick in this scenario.
2:49 I have written a ton of code that does this kind of thing in my career, minus the AI.
2:54 For example, anytime you're working on code that does network transfers,
2:57 There's always a fixed amount of memory that gets allocated as a buffer to hold the data that came from the network during processing
3:03 Question always arises how big a buffer should you allocate?
3:06 So you write some code that loops through various buffer sizes runs a benchmark records the results for each when it done Assuming your benchmark was good You know what to set the buffer size to for maximum performance Auto research is basically an AI version of that It more convenient than having to code for yourself
3:22 what values you want the tool to experiment with.
3:24 But it's just a performance-getting tool,
3:26 and it's not a particularly sophisticated one at that.
3:29 Understand that this isn't nearly sufficient.
3:31 In order for recursive self-improvement to even start,
3:34 an AI would first have to code better than humans.
3:37 Not better than the average human,
3:38 not better than the best human,
3:39 but better than the best possible human.
3:41 And AIs, despite what everyone seems to say,
3:44 cannot write better code than the average professional human coder.
3:47 A lot of people get this wrong, so let me be very clear.
3:49 What today's AI can do is write code faster than a human, not better.
3:55 A lot of people say that coding agents like Cloud Code can write code better than humans.
3:59 And many professional programmers have said that AIs can write code better than they can.
4:03 But that's only true if time is an important factor.
4:07 AI can write more code and more functional code in an hour than any human can write in an hour.
4:12 But that doesn't mean that the code is better than a human could write.
4:16 It just means that it's better given a relatively short amount of time.
4:20 And you'll notice that benchmarks and standardized tests are pretty much all intended to produce results in a relatively short amount of time.
4:26 That's why generative AI is so good at benchmarks.
4:29 But that's nowhere near good enough to kick off recursive self-improvement.
4:33 And the programming part is just the easiest part for an AI to do.
4:36 I spend a lot of time on this channel talking about the difference between training an AI to play a game like chess or Go or even the computer security hacking version of capture the flag and training an AI for general intelligence also known as anything and everything a human has ever learned how to do That the second thing that AI has to be able to do for recursive self to work It has to be able to understand and create better than any human the criteria for measuring whether the changes being made to an AI make it better or worse at anything and everything
5:03 a human has ever learned to do. No one and nothing has any idea how to do that. A phrase often used
5:09 in discussing AI functionality these days is jagged. The idea that if you could graph how good
5:13 AIs are at everything, there would be some things that AIs are a lot better at than humans like
5:18 Yes or go. And the graph for those things would be really high.
5:20 And then the things the AIs are way worse than humans at, like recognizing when they're operating outside the parameters that they've been trained for.
5:26 Like in those videos where the self-driving cars keep ignoring hand signals from police officers directing traffic.
5:32 The graph for those things would be really, really low.
5:34 And so the whole graph would look jagged with big spikes up and big drops down.
5:38 We have no idea how to fix the jagged problem.
5:40 And the best AIs that we built have even less of an idea how to fix it than we do.
5:44 But we're not done yet, because the third thing that an AI would have to do for recursive self-improvement
5:49 is to come up with new and better ways of simulating how an artificial brain should work.
5:53 Not tuning the neural networks we have now.
5:55 We're already seeing that's not going to get us much closer to general intelligence.
5:58 As an AI researcher recently said, we're moving from the age of scaling to the age of research.
6:03 And recursive self-improvement requires the AI to be better than we can be at that new research.
6:08 And right now, the best an AI can do is tune up a single, simple Python script
6:13 after being given a human-defined metric for judging what better or worse means.
6:17 This is not a step toward recursive self-improvement,
6:20 which means it's not a step toward super AI.
6:23 So take a deep breath, ignore the headlines,
6:25 send this video to anyone you know that's freaked out about super AI getting closer,
6:29 and above all, let's be careful out there.
