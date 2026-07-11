---
video_id: "dVFpczPLhVU"
title: "Intelligence explosion needs recursive self-improvement | Aravind Srinivas and Lex Fridman"
channel: "Lex Clips"
source_url: "https://www.youtube.com/watch?v=dVFpczPLhVU"
duration_seconds: 657
upload_date: "20240623"
availability: "public"
license: null
transcript_method: "groq-whisper-asr"
asr_models: ["whisper-large-v3-turbo"]
caption_error: "Deprecated Feature: Support for Python version 3.10 has been deprecated. Please update to Python 3.11 or above\nWARNING: [youtube] dVFpczPLhVU: Unable to download webpage: HTTP Error 429: Too Many Requests (caused by <HTTPError 429: Too Many Requests>)\nWARNING: [youtube] Unable to fetch GVS PO Token for web_safari client: Missing required Visitor Data. You may need to pass Visitor Data with --extractor-args \"youtube:visitor_data=XXX\"\nERROR: [youtube] dVFpczPLhVU: Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication. See  https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp  for how to manually pass cookies. Also see  https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies  for tips on effectively exporting YouTube cookies"
segment_count: 156
relevance_categories: ["agent-operations"]
relevance_evidence: ["agents"]
relevance_spans: [{"category": "agent-operations", "timestamp": "1:34", "phrase": "agents", "text": "collect a bunch of tasks like that and create a rl suit for that or like give agents like tasks"}]
rights_note: "YouTube source content remains owned by its rightsholder. Transcript is retained for research, indexing, quotation, and verification; no ownership is claimed."
raw_files: {"asr-000.json": "ba39edf96799734a72d0a0617721bc26f119cfb4bd389ae249a86ddab41be811", "asr-001.json": "440be8a3dfd3236993a630fc8fccc5d7661601a6af6a64e47942be1a22a633e1", "source-info.json": "b214aa05214f3698cce10b948122ff575ee8cd1ea398c970f15ade3fb5fab32d"}
---

# Intelligence explosion needs recursive self-improvement | Aravind Srinivas and Lex Fridman

0:00 this kind of work hints a little bit of a similar kind of approach to self-play.
0:09 I think it's possible we live in a world where we get like an intelligence explosion
0:14 from self-supervised post-training,
0:20 meaning like there's some kind of insane world where AI systems are just talking to each other
0:25 and learning from each other.
0:27 That's what this kind of, at least to me, seems like it's pushing towards that direction.
0:31 Yeah.
0:31 And it's not obvious to me that that's not possible.
0:35 It's not possible to say, unless mathematically you can say it's not possible.
0:40 Right.
0:41 It's hard to say it's not possible.
0:43 Of course, there are some simple arguments you can make, like where is the new signal to the AI coming from?
0:51 Like how are you creating new signal from nothing?
0:54 There has to be some human annotation.
0:57 Like for self-play, go or chess, you know, who won the game, that was signal.
1:02 And that's according to the rules of the game.
1:04 In these AI tasks, like, of course, for math and coding,
1:08 you can always verify if something is correct through traditional verifiers.
1:12 But for more open-ended things, like say, predict the stock market for Q3.
1:20 Like what is correct?
1:22 You don't even know.
1:23 okay maybe you can use historic data i only give you data until q1 and see if you predict it will
1:29 for q2 and you train on that signal maybe that that's useful uh and you then you still have to
1:34 collect a bunch of tasks like that and create a rl suit for that or like give agents like tasks
1:41 like a browser and ask them to do things and sandbox it and verify like completion is based
1:46 on whether the task was achieved which will be verified by humans so you you do need to set up
1:50 like the RL sandbox for these agents to like play and test and verify.
1:56 And get signal from humans at some point.
1:59 Yeah.
1:59 But I guess the idea is that the amount of signal you need relative to how much new intelligence you gain is much smaller.
2:08 So you just need to interact with humans every once in a while.
2:10 Bootstrap, interact, and improve.
2:13 So maybe when recursive self-improvement is cracked, yes, we, you know,
2:19 and that's when like intelligence explosion happens
2:21 where you've cracked it.
2:23 You know that the same compute when applied iteratively keeps leading you to like you know increase in like IQ points or like reliability And then like you know you just decide okay
2:37 I'm just going to buy a million GPUs and just scale this thing up.
2:40 And then what would happen after that whole process is done,
2:44 where there are some humans along the way providing, like, you know,
2:47 push yes and no buttons, like, and that could be a pretty interesting experiment.
2:52 But we have not achieved anything of this nature yet.
2:56 You know, at least nothing I'm aware of unless it's happening in secret in some frontier lab.
3:02 But so far, it doesn't seem like we are anywhere close to this.
3:05 It doesn't feel like it's far away, though.
3:08 It feels like there's all everything is in place to make that happen, especially because there's a lot of humans using AI systems.
3:17 like can you have a conversation with an ai where it feels like you talked to einstein
3:23 or feinman where you ask them a hard question they're like i don't know and then after a week
3:30 they did a lot of research and come back yeah and come back and just blow your mind i think that
3:35 that that's that if we can achieve that that amount of inference compute where it leads to
3:40 a dramatically better answer as you apply more inference compute i think that would be the
3:45 beginning of like real reasoning breakthroughs so you think fundamentally ai is capable of that
3:50 kind of reasoning it's possible right like we haven't cracked it but nothing says like we cannot
3:58 ever crack it what makes humans special though is like our curiosity like even if ai has cracked this
4:04 it's it's us like still asking them to go explore something and one thing that i feel like ai's
4:12 haven't cracked yet is like being naturally curious and coming up with interesting questions
4:17 to understand the world and going and digging deeper about them yeah that's one of the missions
4:21 of the company is to cater to human curiosity and it surfaces this fundamental question is like
4:28 where does that curiosity come from exactly it's not well understood yeah and i also think it's
4:33 what kind of makes us really special i know you you talk a lot about this you know what makes
4:39 human specialists, love, like natural beauty to the,
4:44 like how we live and things like that.
4:46 I think another dimension is,
4:48 we're just like deeply curious as a species.
4:51 And I think we have like some work in AIS have explored this like curiosity exploration You know like a Berkeley professor Alyosha F Rose has written some papers on this where you know
5:06 in RL, what happens if you just don't have any reward signal?
5:10 And an agent just explores based on prediction errors.
5:13 And, like, he showed that you can even complete a whole Mario game or, like, a level by literally just being curious.
5:20 because games are designed that way by the designer to like keep leading you to new things.
5:27 So I think, but that's just like works at the game level
5:30 and like nothing has been done to like really mimic real human curiosity.
5:35 So I feel like even in a world where, you know, you call that an AGI,
5:39 if you can, you feel like you can have a conversation with an AI scientist at the level of Feynman.
5:44 even in such a world like i don't think uh there's any indication to me that we can mimic
5:51 fineman's curiosity we could mimic fineman's ability to like thoroughly research something
5:56 and come up with non-trivial answers to something but can we mimic his natural curiosity and about
6:04 just you know his his spirit of like just being naturally curious about so many different things
6:09 and endeavouring to try and understand the right question
6:14 or seek explanations for the right question,
6:16 it's not clear to me yet.
6:18 It feels like the process that perplexity is doing
6:21 where you ask a question, you answer it,
6:22 and then you go on to the next related question
6:24 and this chain of questions,
6:26 that feels like that could be instilled into AI,
6:29 just constantly searching.
6:32 So you are the one who made the decision on like...
6:34 Initial spark for the fire, yeah.
6:36 And you don't even need to ask the...
6:39 the exact question we suggested, it's more a guidance for you.
6:45 You could ask anything else.
6:47 And if AIs can go and explore the world and ask their own questions,
6:52 come back and, like, come up with their own great answers,
6:55 it almost feels like you got a whole GPU server that's just like, hey, you give the task, you know,
7:02 Just to go and explore drug design,
7:09 like figure out how to take AlphaFold3
7:11 and make a drug that cures cancer
7:13 and come back to me once you find something amazing.
7:17 And then you pay like, say, $10 million for that job.
7:21 But then the answer came back with you.
7:24 It like a completely new way to do things And what is the value of that one particular answer That would be insane if it worked So that the sort of world that I think we don need to really worry about
7:37 AI is going rogue and taking over the world,
7:40 but it's less about access to a model's weights.
7:44 It's more access to compute that is, you know,
7:48 putting the world in like more concentration of power and few individuals
7:52 because not everyone's going to be able to afford this much amount of compute to answer the hardest questions.
8:00 So it's this incredible power that comes with an AGI-type system.
8:05 The concern is who controls the compute on which the AGI runs.
8:09 Correct. Or rather, who's even able to afford it?
8:13 Because controlling the compute might just be like cloud provider or something,
8:16 but who's able to spin up a job that just goes and says,
8:21 hey, go do this research and come back to me and give me a great answer.
8:26 So to you, AGI in part is compute limited versus data limited.
8:31 Inference compute.
8:32 Inference compute.
8:33 Yeah.
8:34 It's not much about, I think like at some point,
8:37 it's less about the pre-training or post-training.
8:40 Once you crack this sort of iterative compute of the same weights.
8:44 right it's going to be the so like it's nature versus nurture once you crack the nature part
8:51 yeah which is like the pre-training it's it's all going to be the nerd the uh the rapid iterative
8:57 thinking that the ai system is doing and that needs compute yeah we're calling it it's fluid
9:01 intelligence right the facts research papers existing facts about the world ability to take
9:08 that, verify what is correct and right, ask the right questions, and do
9:12 it in a chain, and do it for a long
9:16 time, not even talking about systems that come back to you after an hour,
9:21 like a week, right, or a month.
9:25 You would pay, like imagine if someone came and gave you a transformer
9:28 like paper, like let's say you're in 2016, and you
9:32 asked an AI, an EGI,
9:35 hey, I want to make everything a lot more efficient.
9:39 I want to be able to use the same amount of compute today
9:41 but end up with a model 100X better.
9:44 And then the answer ended up being transformer.
9:46 But instead it was done by an AI
9:48 instead of Google brain researchers, right?
9:51 Now what is the value of that?
9:52 The value of that is like trillion dollars,
9:55 technically speaking.
9:56 So would you be willing to pay $100 million
10:00 for that one job?
10:00 Yes.
10:01 But how many people can afford $100 million for one job?
10:04 Very few.
10:06 Some high net worth individuals and some really well capitalized companies.
10:10 And nations, if it turns to that.
10:12 Correct.
10:13 Where nations take control.
10:14 Nations, yeah.
10:15 So that is where we need to be clear.
10:17 The regulation is not on the mark.
10:19 That's where I think the whole conversation around,
10:22 oh, the weights are dangerous.
10:24 that's all like really flawed.
10:31 And it's more about like application
10:35 who has access to all this.
10:54 Thank you.
