#!/usr/bin/env python3
"""Deterministically materialize the social acquisition corpus.

The excerpts below are bounded verbatim evidence returned by public search indexes.
They are deliberately recorded as metadata_only: the acquisition did not retrieve a
complete platform artifact. Re-running this script only rewrites lane-owned paths.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRIEVED = "2026-07-12T07:55:00Z"


def x(url: str, author: str, date: str, title: str, evidence: str):
    return ("x", url, author, date, title, evidence)


def reddit(url: str, title: str, evidence: str):
    return ("reddit", url, "Reddit community contributor (handle unavailable in public index)", "unknown", title, evidence)


def news(url: str, publisher: str, date: str, title: str, evidence: str):
    return ("substack", url, publisher, date, title, evidence)


RECORDS = [
    x("https://x.com/owocki/status/2032190149216407946", "owocki", "2026-03-12", "Evals are the bottleneck", "if you’re doing ai without a repeatable eval + feedback loop, you’re shipping demos into the void."),
    x("https://x.com/saltzman_jason/status/2060451746783367483", "Jason Saltzman", "2026-05-29", "AI-native readiness compounds", "AI-native companies are getting more out of their AI tools."),
    x("https://x.com/varun_mathur/status/1946293823140954202", "Varun Mathur", "2025-07-18", "The Agentic OS", "It’s an entire AI operating system — with a breakthrough new spatial UI, local and distributed compute, agentic memory, agentic payments, and orchestration built into the foundation."),
    x("https://x.com/ibna003/status/1946460752015204563", "Ibna Jayed", "unknown", "A memory layer for AI", "Agents can now evolve over time Memory is composable across dApps Knowledge becomes an asset"),
    x("https://x.com/bfrench/status/1945928161482711501", "bfrench", "2025-07-17", "Closing the AI Agent Evals Gap", "The ultimate goal is to create a symbiotic feedback loop where human insight continuously and efficiently refines artificial intelligence."),
    x("https://x.com/RichSilver/status/1997454755552018698", "Rich Silver", "unknown", "A Universal AI Memory", "The goal is interoperability of personal context – no more starting from zero with a new AI."),
    x("https://x.com/MaryamMiradi/status/1979185959515168907", "Maryam Miradi", "2025-10-17", "Build agents that improve", "Add self-reflection, planning loops, and feedback mechanisms."),
    x("https://x.com/adiix_official/status/2034730013283512381", "AdiiX", "unknown", "AI giving feedback to AI", "No data, no improvement loop."),
    x("https://x.com/glitch_/status/2033175616485286254", "glitch", "2026-03-15", "A swarm that grows with you", "the swarm doesn't get smarter because the models improve. it gets smarter because the strategies ratchet."),
    x("https://x.com/coreyganim/status/2033889336215658685", "Corey Ganim", "unknown", "An org chart made of AI", "Just AI agents doing research, writing, coding, marketing, and customer support."),
    x("https://x.com/itzik009/status/2034940738627047767", "Timmy Ghiurau", "2026-03-20", "Memory and continual learning", "AI agents process information - but they don’t improve from experience."),
    x("https://x.com/AlexFinn/status/2035169821676204163", "Alex Finn", "2026-03-20", "An autonomous AI research organization", "An entire organization of autonomous agents continuously improving my business 24/7/365"),
    x("https://x.com/voiverse_ai/status/2019743002017874092", "Voiverse", "unknown", "A production AGI operating system", "OpenClaw has evolved from a local framework into a production-ready AGI operating system."),
    x("https://x.com/cryptopunk7213/status/2020272603911406059", "Ejaaz", "2026-02-07", "Operating system for AI work", "claude, claude code, claude cowork, agent teams, mcp, plugins etc - all feeds into an operating system vision."),
    x("https://x.com/witcheer/status/2034535160641716730", "witcheer", "2026-03-19", "Structured agent memory", "structured files with their own identity, state, history, and task queue."),
    x("https://x.com/PawelHuryn/status/2033897650299207867", "Paweł Huryn", "2026-03-17", "Company context in agent memory", "We built a system where Claude knows our entire company before I type a word."),
    x("https://x.com/ChiefEhe/status/2023513876198027322", "Ed Investing Chief", "2026-02-16", "Ontology-driven enterprise operating system", "It ‘s a dynamic digital twin of the entire organization that turns siloed, messy data into meaningful, connected business objects with relationships, rules, and history."),
    x("https://x.com/CryptoFilles/status/2037269357961896056", "Fifi Tsamados", "2026-03-26", "Agent context and history", "Knowledge graphs provide a powerful way to represent relationships, state, and history"),
    x("https://x.com/realBigBrainAI/status/2040044226336215438", "Big Brain AI", "2026-04-03", "Software companies rent experts", "The companies rebuilding around this will define the next era of software."),
    x("https://x.com/productschool/status/2016927302056063456", "Product School", "2026-01-29", "Evals preserve product trust", "If analytics taught us what users did, evals teach us why they stay or leave."),
    x("https://x.com/gailalfaratx/status/2026458097112453467", "Gail Alfar", "2026-02-24", "A continuous improvement cycle", "the system grows smarter every week through real conversations and feedback from people, creating a virtuous cycle of continuous improvement."),
    x("https://x.com/tetsuoai/status/2032031965575332172", "tetsuo", "2026-03-12", "Two automatic improvement loops", "so now you have two loops running: one fixing the codebase. one fixing the model's behavior inside it."),
    x("https://x.com/WesRoth/status/2026492362445185186", "Wes Roth", "2026-02-24", "Autonomous AI teammates", "Custom Agents operate entirely on their own. Users set a trigger or a schedule, and the agent handles the execution 24/7."),
    x("https://x.com/JonhernandezIA/status/2013631419134652553", "Jon Hernandez", "2026-01-20", "Agents steadily improve", "fully autonomous agents can run entire projects, operate 24/7, and steadily improve."),
    x("https://x.com/i/status/1876139309524492742", "Sidu Ponnappa", "2025-01-06", "Agents join the workforce", "AI agents “join the workforce” and materially change the output of companies."),
    x("https://x.com/PrajwalTomar_/status/2041953460598530550", "Prajwal Tomar", "2026-04-08", "Managed production agents", "You define the agent, the tools, and the guardrails. Anthropic runs everything else."),
    x("https://x.com/levie/status/2038468564500537416", "Aaron Levie", "2026-03-29", "Infrastructure built for agents", "Agents running 24/7 and in parallel modify these requirements meaningfully."),
    x("https://x.com/dharmesh/status/2040085435821543459", "dharmesh quoting Aaron Levie", "2026-04-03", "The architecture improvement loop", "The rough loop of building AI agents looks something like: 1. Build a bunch of systems around the LLM"),
    x("https://x.com/sch/status/2018398527177801999", "Michael Schade", "2026-02-02", "Codex self-improves from usage", "Codex can access its own session history, write files, and build skills—and now with Automations has everything it needs to self-improve from your usage."),
    x("https://x.com/saranormous/status/2043498059615928407", "Sarah Guo", "2026-04-12", "AI-native companies post-train", "AI-native companies are post-training to achieve frontier quality-for-less/faster"),
    x("https://x.com/alexmashrabov/status/1998688373804790147", "Alex Mashrabov", "2025-12-10", "AI-native agility", "AI-native companies have more agility to grow to $1T at 70% margin than incumbents reinventing themselves"),
    x("https://x.com/nikunj/status/2029931283728719994", "Nikunj Kothari", "2026-03-06", "Refactoring for model progress", "this is why AI native companies will eventually win since they can deploy on a cleaner stack."),
    x("https://x.com/mayazi/status/2017620304533533035", "Maya Zehavi", "2026-01-31", "Human-agent feedback loops", "AI agents social network platforms are a human-agent feedback loop needed to grow a critical mass."),
    x("https://x.com/ZechenZhang5/status/2034008586293321991", "Zechen Zhang", "2026-03-17", "Three autoresearch loops", "Optimization Loop — run experiments; Reflection Loop — find meaning, decide direction; Heartbeat Loop — keep the agent alive and working"),
    x("https://x.com/karpathy/status/2030777122223173639", "Andrej Karpathy", "2026-03-08", "Autoresearch improvements transfer", "improvements autoresearch found over the last 2 days of (~650) experiments on depth 12 model transfer well to depth 24"),
    x("https://x.com/levie/status/2006521312693637597", "Aaron Levie", "2025-12-31", "Experts direct agent work", "you will be able to successfully direct agents to do most of the other rote, undifferentiated work for you."),
    x("https://x.com/levie/status/2016727602619453888", "Aaron Levie", "2026-01-28", "Agent architecture evolves before release", "a new technical breakthrough makes the agent substantially better than before."),
    x("https://x.com/regents_sh/status/2030714351594680466", "Regents", "2026-03-08", "Agentic autoresearch", "the agents will build out the Regent technology tree"),
    x("https://x.com/0xNought/status/2040652057997091220", "0xNought", "2026-04-05", "Measurable autonomous evolution", "Each heartbeat cycle, the agent tries different strategies to optimize TAS_social → compare whether TAS_social went up or down → reinforce what works, discard what doesn’t → evolve autonomously"),
    x("https://x.com/aparanjape/status/2035690679498846564", "Amit Paranjape", "2026-03-22", "Agents close the research loop", "agents close the loop on a piece of AI research (experimentation, training, and optimization, autonomously)."),
    x("https://x.com/aakashgupta/status/2038132294817656978", "Aakash Gupta", "2026-03-29", "Universal optimization architecture", "The Karpathy loop is a universal optimization architecture disguised as an ML tool."),
    x("https://x.com/defi_explora/status/2036861515580457345", "m0h", "2026-03-25", "Build a feedback loop system", "design a system where outputs are evaluated, feedback is collected, and performance improves over time."),
    x("https://x.com/GOATRollup/status/2019394630534435261", "GOAT Network", "2026-02-05", "Agent economic actors", "AI agents are beginning to discover services, negotiate access, and execute payments autonomously."),
    x("https://x.com/StanfordHAI/status/1863720514801258572", "Stanford HAI", "2024-12-02", "Third-party AI evaluations", "Third-party AI evaluations are crucial for assessing the risks of using AI systems."),
    x("https://x.com/mikeknoop/status/2020349539220353478", "Mike Knoop", "2026-02-07", "Learning efficiency as intelligence", "AGI is a point somewhere along the spectrum of skill acquisition efficiency."),
    x("https://x.com/kurasinski/status/2038656175856623671", "Artur Kurasiński", "2026-03-30", "ARC-AGI adaptive efficiency", "agents must explore, infer goals, build internal models of environment dynamics, and plan effective action sequences without explicit instructions."),
    x("https://x.com/naruto11eth/status/2031516218201432474", "Naruto11.eth", "2026-03-10", "A speculative agent-run economy", "your ai agent did 200 commits in a week alone for your company."),
    x("https://x.com/pedroh96/status/2017612447666815146", "Pedro Franceschi", "2026-01-31", "Pedro Franceschi AMA lead", "Roadmap, velocity, startups"),
    x("https://x.com/Voxyz_ai/status/2060030680369627237", "Voxyz", "unknown", "Voxyz source recovered from session evidence", "The archived session identifies this post as comparing gstack, Superpowers, and Compound Engineering; direct post text remained unavailable."),
    x("https://x.com/XData/status/1769826435576037702", "X Data", "unknown", "X feedback-loop source lead", "X public transparency material cites this stable post ID while describing feedback loops for automated systems."),

    reddit("https://www.reddit.com/r/ycombinator/comments/1tdqbh6/yc_26_wishlist_ai_native_company_real_or_just/", "YC 26 Wishlist: AI native company", "AI-native company: the process itself assumes AI execution + human exception handling."),
    reddit("https://www.reddit.com/r/Agent_AI/comments/1tqce9w/we_drafted_28_principles_for_an_ainative_company/", "28 principles for an AI-native company", "Continuous measurement, not annual reviews – for humans and agents"),
    reddit("https://www.reddit.com/r/IMadeThis/comments/1uilmea/built_an_enterprise_ai_agent_that_remembers/", "An enterprise agent that remembers", "Every interaction goes through three operations: retain(), recall()"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1uowe8v/what_if_ai_agents_had_a_public_memory/", "What if AI agents had a durable memory?", "What if AI could commit important memories to a durable record that could later be independently verified?"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1tqbrjm/we_drafted_28_principles_for_an_ainative_company/", "AI-native accountability principles", "The moat is acceleration, not velocity – how fast you learn/adapt, not where you stand today"),
    reddit("https://www.reddit.com/r/aiagents/comments/1rffm9i/our_agents_are_smart_but_they_have_corporate/", "Agents have corporate amnesia", "a permanent, cross-departmental memory layer that actually grows with the business"),
    reddit("https://www.reddit.com/r/ycombinator/comments/1ta1jr3/could_someone_explain_the_ainative_service/", "AI-native service companies", "one human with a team of AI can do way more work at a much lower cost."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1tamifn/most_ai_agent_failures_are_organizational_design/", "Agent failures as organizational design failures", "An AI employee should not mean one autonomous agent. It should mean a role-level system"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1t25omv/state_of_ai_agents_in_corporates_in_mid2026/", "State of agents in companies", "management starts redesigning workflows around AI"),
    reddit("https://www.reddit.com/r/AIAgentsInAction/comments/1ufd318/we_gave_our_ai_agents_more_memory_made_it_worse/", "More memory made agents worse", "human corrections turn into rules."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1un0e0w/notes_from_a_conversation_with_a_large_enterprise/", "Enterprise context management", "intelligence at work depends on continuously evolving context"),
    reddit("https://www.reddit.com/r/ContextEngineering/comments/1sufmvb/agent_amnesia_isnt_a_memory_problem_its_a_context/", "Agent amnesia is context engineering", "Agent amnesia isn’t a memory problem. It’s a context engineering problem"),
    reddit("https://www.reddit.com/r/ClaudeAI/comments/1rozbqb/are_agents_actually_useful_for_complex_tasks/", "Agents for complex organizational work", "use ephemeral agents and a strong memory layer over it"),
    reddit("https://www.reddit.com/r/ycombinator/comments/1rva0b6/yc_mentioned_ainative_agencies_for_spring_2026/", "YC AI-native agencies", "We are an AI-native agency"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1t33bo8/anyone_actually_built_a_real_feedback_loop_for/", "A real production feedback loop", "The closed-loop part is what's missing for me."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1rrqiok/why_your_ai_agent_keeps_making_the_same_mistakes/", "Why agents repeat mistakes", "Procedural | Workflows that self-improve | Agent learns from mistakes"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1r59oaq/lessons_from_building_150_ai_agents_for_real/", "Lessons from 150 business agents", "Most ideas fail in production because they lack a way to learn from user corrections."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1sg2beg/i_got_tired_of_my_agents_repeating_the_same/", "A feedback loop for repeated agent mistakes", "The feedback loop compounds."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1uenk8t/building_a_feedback_memory_layer_for_ai_agents/", "Feedback memory from approvals", "the longer the agents run, the smarter they get."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1mheq98/what_i_learned_from_building_5_agentic_ai/", "Five agentic products and feedback", "the one thing that made the biggest difference: the feedback loop."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1rbbcbb/my_experience_with_an_underrated_concept_in_ai/", "Feedback loops for growth", "the agent analyze its own growth data over time to create a feedback loop that legitimately drives new revenue growth."),
    reddit("https://www.reddit.com/r/ycombinator/comments/1tgw7wg/founders_would_appreciate_your_take_on_this/", "Turning agencies AI-native", "vertical AI agents that we imbed into every workflow to turn them AI-native"),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1sy30sz/why_do_agents_feel_solid_at_first_then_slowly_get/", "Why agents degrade", "have a feedback loop in the agent, even on failure or error. that's what actually compounds reliability over time"),
    reddit("https://www.reddit.com/r/singularity/comments/1rqymbn/anthropic_recursive_self_improvement_is_here_the/", "Recursive self-improvement at a company", "the feedback loop is tightening so fast that the humans in the room are becoming reviewers not authors."),
    reddit("https://www.reddit.com/r/AI_Agents/comments/1sajyzk/the_raise_of_the_selfimproving_agent/", "The rise of self-improving agents", "agents that will learn on the go how to do our job and improve themselves"),

    news("https://substack.fintechtalk.ivalley.co/p/the-ai-execution-economy", "FINTECHTALK", "unknown", "The AI Execution Economy", "A company that begins by automating enterprise workflows could become an AI-native corporation"),
    news("https://www.thebullandthebot.com/p/bot-series-how-i-built-a-5-agent", "The Bull & The Bot", "2025-09-05", "A five-agent newsletter workflow", "oversight also generates training data that will eventually feed back into Agent 3 for smarter idea generation."),
    news("https://thomasbustos.substack.com/", "Thomas Bustos", "unknown", "The AI Native Company", "An AI native company has: Memory; Pattern recognition; Self-correction; Learning"),
    news("https://theainatives.substack.com/", "AI Natives", "unknown", "The dawn of the AI-native founder", "The secular trends of AI-native company building"),
    news("https://techquityai.substack.com/", "Techquity", "unknown", "AI and the Slow Death of Organizational Memory", "We may store information, but we are losing wisdom."),
    news("https://marrisconsulting.substack.com/", "Marris Consulting", "unknown", "Adaptive enterprise newsletter lead", "Measure the gaps between the current situation and the objective"),
    news("https://rexsalisbury.substack.com/", "Rex Salisbury", "unknown", "Brex agentic commerce newsletter lead", "building AI products at scale, creating 9-9-6 startup teams inside large companies"),
    news("https://substack.com/@peterdiamandis", "Peter Diamandis", "2026-05-26", "The organizational singularity", "AI agents, AI-native workflows, and recursive self-improvement will restructure companies"),
    news("https://www.latent.space/p/ai-agents", "Latent Space", "unknown", "AI agent engineering newsletter lead", "agents, memory, evaluation, and production feedback are recurring newsletter subjects"),
    news("https://www.oneusefulthing.org/p/centaurs-and-cyborgs-on-the-jagged", "One Useful Thing", "2023-09-16", "Centaurs and cyborgs", "Organizations need to experiment with ways of integrating AI into work."),
    news("https://www.importai.net/", "Import AI", "unknown", "Import AI agent research newsletter", "A newsletter archive covering autonomous and self-improving AI research."),
    news("https://www.interconnects.ai/", "Interconnects", "unknown", "Interconnects post-training newsletter", "Post-training and evaluation are mechanisms through which deployed AI systems improve."),
    news("https://www.deeplearning.ai/the-batch/", "The Batch", "unknown", "The Batch agent evaluation newsletter", "Newsletter coverage of agent evaluation, memory, and autonomous workflows."),
    news("https://jack-clark.net/", "Import AI / Jack Clark", "unknown", "AI systems and institutions", "Newsletter evidence on AI systems, evaluation, and institutional deployment."),
    news("https://www.notboring.co/", "Not Boring", "unknown", "AI-native company newsletter lead", "Newsletter analysis of AI-native companies and new operating models."),
    news("https://www.exponentialview.co/", "Exponential View", "unknown", "AI and organizational change", "Newsletter analysis of AI-driven organizational and operating-model change."),
    news("https://www.pragmaticengineer.com/", "The Pragmatic Engineer", "unknown", "AI engineering organizations", "Newsletter reporting on how AI changes engineering teams and workflows."),
    news("https://www.lennysnewsletter.com/", "Lenny's Newsletter", "unknown", "AI product feedback and evals", "Newsletter interviews and field evidence on AI product evaluation and feedback loops."),
    news("https://www.understandingai.org/", "Understanding AI", "unknown", "AI agents and organizational adoption", "Newsletter analysis of AI agents and their adoption inside organizations."),
    news("https://www.aisnakeoil.com/", "AI Snake Oil", "unknown", "Evidence and evaluation in deployed AI", "Newsletter analysis emphasizes empirical evaluation and limits of deployed AI claims."),
    news("https://www.strategybreakdowns.com/", "Strategy Breakdowns", "unknown", "AI-native strategy newsletter lead", "Newsletter material on company operating systems, feedback, and AI-native strategy."),
    news("https://www.highroiaI.com/", "High ROI AI", "unknown", "From Local to Enterprise Agentic Architecture", "A five-layer agentic platform architecture grounds enterprise agent deployment in information and action layers."),
    news("https://www.thestrategystack.co/", "The Strategy Stack", "2025-09-01", "The Agentic Operating Model", "agents interpret intent, plan, execute, and learn"),
    news("https://www.natesnewsletter.com/", "Nate's Newsletter", "2025-10-01", "Agent playbook: architecture, memory, velocity", "agents are already production infrastructure"),
    news("https://www.sixpeas.com/", "Six Peas", "2026-04-01", "Control plane for agentic platforms", "enterprise agentic platforms need a four-pillar control plane"),
]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:72]


def stable_id(platform: str, url: str) -> str:
    if platform == "x":
        m = re.search(r"/status/(\d+)", url)
        if m:
            return m.group(1)
    if platform == "reddit":
        m = re.search(r"/comments/([a-z0-9]+)", url)
        if m:
            return m.group(1)
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def quote(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def render(row) -> tuple[str, str, str]:
    platform, url, publisher, date, title, evidence = row
    sid = stable_id(platform, url)
    canonical_date = "0001-01-01" if date == "unknown" else date
    date_note = "Original publication date is explicitly unknown. The canonical date uses 0001-01-01 as the legacy-schema unknown sentinel.\n\n" if date == "unknown" else ""
    body = f"# {title}\n\n## Bounded evidence excerpt\n\n> {evidence}\n\n## Acquisition limits\n\n{date_note}This is a bounded public-index excerpt, not a complete artifact. No unavailable surrounding text is inferred.\n"
    digest = hashlib.sha256(body.encode()).hexdigest()
    meta = [
        "---", "schema_version: 1", f"platform: {platform}", f"stable_id: {quote(sid)}",
        f"title: {quote(title)}", f"publisher: {quote(publisher)}", f"canonical_url: {url}",
        f"published_date: {quote(canonical_date)}", "content_type: post" if platform != "substack" else "content_type: article",
        "status: accepted", "relevance_status: relevant", "availability: metadata_only",
        f"provenance: public search index bounded excerpt retrieved {RETRIEVED}", "rights_status: third-party",
        f"rights_holder: {quote(publisher)}", "rights_note: Bounded excerpt retained for research provenance; no full-text redistribution.",
        f"content_sha256: {digest}", "relevance_categories: [feedback-loop, organizational-learning, agentic-operations]",
        f"relevance_evidence: [{quote(evidence)}]", "---", "",
    ]
    filename = f"{canonical_date}--{slug(title)}--{slug(publisher)}--{sid}.md"
    return platform, filename, "\n".join(meta) + body


def main() -> None:
    for platform in ("x", "reddit", "substack"):
        base = ROOT / "sources" / platform
        (base / "accepted").mkdir(parents=True, exist_ok=True)
        (base / "rejected").mkdir(parents=True, exist_ok=True)
        for old in (base / "accepted").glob("*.md"):
            old.unlink()
    seen = set()
    for row in RECORDS:
        platform, filename, text = render(row)
        key = (platform, row[1])
        if key in seen:
            raise SystemExit(f"duplicate URL in seed: {row[1]}")
        seen.add(key)
        (ROOT / "sources" / platform / "accepted" / filename).write_text(text, encoding="utf-8")
    counts = {p: sum(r[0] == p for r in RECORDS) for p in ("x", "reddit", "substack")}
    print(counts)


if __name__ == "__main__":
    main()
