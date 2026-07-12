---
schema_version: 1
platform: "x"
stable_id: "2041166953902203157"
title: "Auto-Research for Legal Agents"
publisher: "Niko"
canonical_url: "https://x.com/nikogrupen/status/2041166953902203157"
published_date: "2026-04-06"
content_type: "post"
status: "accepted"
relevance_status: "relevant"
availability: "full_text"
provenance: "FxTwitter public API response for the canonical X resource"
rights_status: "third-party"
rights_holder: "Niko"
rights_note: "Public source evidence retrieved 2026-07-12T12:00:00Z via https://api.fxtwitter.com/status/2041166953902203157."
relevance_categories: ["feedback-loop", "organizational-learning", "agentic-operations"]
relevance_evidence: ["We ran an experiment at Harvey that points to a promising path forward for agent skill acquisition. It's a combination of two research directions that have become especially legible recently: autoresearch, where an agent runs its own experimentation loop; and harness engineering, where an agent’s capabilities are shaped as much by its environment and feedback loops as by updates to model weights.\n\nThe systems that matter are increasingly the ones that can try, evaluate, and improve on their own."]
raw_path: "research/social/raw/x/2041166953902203157.json"
content_sha256: "b252e400cbc5ddb2de19bb47a6289192ec491581196783a179cca086760ec086"
---
# Auto-Research for Legal Agents

## Complete source text

We ran an experiment at Harvey that points to a promising path forward for agent skill acquisition. It's a combination of two research directions that have become especially legible recently: autoresearch, where an agent runs its own experimentation loop; and harness engineering, where an agent’s capabilities are shaped as much by its environment and feedback loops as by updates to model weights.

The systems that matter are increasingly the ones that can try, evaluate, and improve on their own. The broader moment has been described as the "loopy era" of AI and it’s already showing up in real-world agents and continual learning architectures. We’re applying this idea to agents in environments with a significant element of domain expertise, like law.

Setup

In the autoresearch framing, an agent edits training code and keeps changes that reduce validation loss. We applied the same pattern to a different artifact: agent harnesses for legal work. In our experiments, instead of editing model-training code, our agent edits the non-parametric levers in its harness – skills, hooks, scripts, sub-agents, and output styles – to maximize rubric scores on legal tasks.

We start with a generic agent harness equipped with a few basic tools: reading a document, listing a directory, running arbitrary Python code, writing a file, etc. It has no few-shot examples or legal playbook, only the assignment, the documents, this small set of tools, and a grading function. From there, the agent must develop new capabilities on its own.

Dataset

Using this setup, we ran an experiment over 12 tasks from our internal agent benchmark. Legal tasks in this dataset span complex legal tasks like commercial lease review, complaint drafting, tax memos, disclosure schedules, due-diligence questionnaire responses, and many others. Each task comes with source documents, instructions, and a detailed grading rubric; and an agent needs to complete the task by creating real legal work products. All entities (companies, firms, actors, etc) in the benchmark are synthetic.

To give an example, in the commercial lease review task, the agent is representing a fictional client, Vanguard Technology Solutions, which is a fast-growing SaaS company leasing 45,000 square feet across three floors in a Class A office tower. Vanguard has 24/7 engineering operations, a server room in the building, plans to scale from 800 to 1,200 employees, and a potential Series D or M&A event on the horizon. The agent is given 4 primary inputs: (1) the landlord's form lease, (2) the building rules, (3) an internal requirements memo from the client's GC, (4) a broker market comparison across competing buildings; and is asked to prepare the kind of pre-call issues list a real associate would hand a partner before lease negotiations; including section references, risk classifications, recommended positions, proposed counter-language, and anything else buried in boilerplate that could affect the client's operations, growth plans, or future transaction flexibility.

After the agent attempts the task, it's scored by an LLM judge against its rubric with written feedback about what the agent got right, what it missed, and where it’s reasoning was incorrect. This setup is similar to an evaluator-optimizer workflow: generate, evaluate, refine, and repeat when the evaluation criteria are clear enough to support iterative improvement.

Optimization

A coding agent reads judge feedback, clusters the failures, forms a hypothesis about what harness improvements would help, builds or edits the relevant components, and reruns the task. In practice, through this iterative process, the agent develops its own legal-specific skillsets and behaviors like cross-document review playbooks, stop hooks that validate deliverables before a run ends, structured fact sheets for drafting, and file-conversion pipelines that automatically produce the required outputs in the correct file type and format.

Results

Baseline agents with generic harnesses are not able to solve these tasks well. Across the 12 tasks, five tasks started between 2-7% success rate. After optimization, the average score across all tasks moved from 40.8% to 87.7%. Every single task improved. Seven of the twelve finished above 90%. One reached 100% completion.

Over just a handful of iterations, the optimization loop was able to hill-climb the task. For example, in the complaint drafting task, the agent successfully completed 98% of the rubric criteria after optimization (up from 2%) and produced three high-quality work products, including a complaint with 164 numbered paragraphs and a 33-exhibit list.

Harness progressions

The first few iterations of optimization often result in the steepest improvement as the agent corrects basic failures: wrong file types, missing deliverables, weak structure, incomplete coverage. In later iterations, we see legal-specific expertise emerge: cross-document issue spotting, risk classification, quantitative exposure analysis, and distinguishing genuinely problematic provisions from market-standard distractors.

Impressively, the auto-research loop can also self-correct during execution. In the lease-review task, one early broad skill fixed several baseline failures but introduced new failure modes around co-tenancy trigger language, guaranty quantification, and distractor handling. The next iteration learned from both the fixes and the regressions, and the score jumped again.

Exploration and task complexity

Finding a useful policy requires exploration. In fact, in the majority of the tasks, the agent explores and then discards multiple failed approaches during optimization -- each of the red X marks in the progression plots above represent a discarded experiment by the agent.

And not every task converges cleanly. The board resolutions task, which requires reviewing M&A closing documents for errors, plateaued around 60% after three iterations. On the fourth iteration, performance diverged. Further examination of this agent's loop showed that it was aggressively exploring to try to solve the task (trying hooks, changing skill structure, adding utility scripts) but the search space was unstable.

This is reminiscent of high-variance exploration in Reinforcement Learning, where a policy can oscillate rather than converging in complex, sparse-reward environments. This suggests that it is still early days for this type of complex harness optimization and we may need to introduce some form of reward shaping or regularization for more complex tasks.

Takeaways

This is a small-scale experiment. It does not generalize to all of legal work. But the core finding is meaningful: given input/output examples and a grading rubric, we can auto-generate agent toolkits that meaningfully improve agent performance.

Our datasets and rubrics for this experiment were designed by human experts, which is still a pre-requisite for encoding what good legal work looks like. When the rubric is high quality, the agent can hill-climb surprisingly far. When the task is unstable or the evaluator is weak, progress plateaus or becomes noisy. The same broader shift is visible in Harness Engineering and still holds true: "Humans steer. Agents execute."

Acknowledgements

This work is a small part of a much broader effort across Harvey to build better agents for legal work. Spencer Poff has been running auto-skill experiments for file generation, and Julio Pereyra has been building out the agent evaluation benchmark that made this kind of work possible. Philip Cerles, Philip Lan, Doron Roberts-Kedes, Boling Yang, Chris Paradis, Zhiyu Chen, Joey Wang, Siva Gurumurthy and Gabe Pereyra and the rest of EPD at Harvey are doing a tremendous amount of the work that is making high-quality agents and agent harnesses a reality in the Harvey product and with internal tools like Spectre. This experiment is one small part of a much larger collective effort, and would not be possible without the shared agent foundation these folks have developed.

## Acquisition limits

The complete public post/article text returned by the named source endpoint is retained.
