# Canonical Organization Evidence Index

Generated from `research/organization-evidence.json`. Only accepted evidence about a named organization's implemented operating practice is indexed; generic tooling and theory are excluded.

- Organizations: **14**
- Organization-evidence source links: **15**
- Sources with a measurable outcome: **9**
- Independently sampled generic/theory exclusions: **10**

## Mechanism dashboard

| Mechanism | Source links |
| --- | ---: |
| feedback/evals | 5 |
| organizational memory | 7 |
| experimentation | 5 |
| decision systems | 2 |
| failure/postmortem learning | 3 |
| specialized agents | 4 |
| workflow adaptation | 9 |
| knowledge curation | 6 |
| governance | 4 |
| measurable outcome | 9 |

## Organizations

### Accenture

- [Research: Quantifying GitHub Copilot’s impact in the enterprise with Accenture - The GitHub Blog](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/) — feedback/evals, measurable outcome. Accenture and GitHub measured Copilot adoption and impact using organization-level usage data and public APIs. Evidence: Named enterprise study with an explicit measurement method; outcome claims remain publisher-reported.

### Automattic

- [ExPlat: Automattic’s Experimentation&nbsp;Platform](https://data.blog/2021/03/16/explat-automattics-experimentation-platform/) — experimentation, knowledge curation, governance. Automattic operates an experiment education and review hub, internal feedback forum, wiki, checklist, and peer review process. Evidence: First-party engineering account names the internal operating practices.

### Bayer China

- [Covering 1,000 People in 6 Months, Saving 7,000 hours per year, Bayer China Reshapes Training System with Generative AI](https://aws.amazon.com/solutions/case-studies/bayer-china/) — feedback/evals, workflow adaptation, measurable outcome. Bayer China deployed a learn-practice-evaluation training loop and reported adoption, hours saved, and coaching-efficiency results. Evidence: Named customer deployment with quantitative, vendor-published outcomes.

### Canva

- [How we build experiments in-house - Canva Engineering Blog](https://www.canva.dev/blog/engineering/how-we-build-experiments-in-house/) — organizational memory, experimentation, workflow adaptation. Canva built an internal experimentation platform and is adapting setup, analysis, and result-learnability workflows. Evidence: First-party engineering account describes a deployed internal platform and its evolution.

### Endava

- [How Endava builds an agentic organization with Codex](https://openai.com/index/endava/) — organizational memory, specialized agents, workflow adaptation, knowledge curation, measurable outcome. Endava codifies senior architectural judgment into agents used across its delivery lifecycle and reports compressing a requirements-analysis engagement from weeks into two one-hour meetings. Evidence: Named Endava executives describe the deployed knowledge-transfer mechanism; the bounded time outcome is vendor-published.

### Etsy

- [Etsy's Debriefing Facilitation Guide for Blameless Postmortems](https://www.etsy.com/codeascraft/debriefing-facilitation-guide) — organizational memory, failure/postmortem learning, knowledge curation. Etsy evolves a debriefing practice that combines objective event data with multiple subjective perspectives to create organizational learning. Evidence: First-party engineering account describes Etsy's implemented and evolving debrief practice.

### Google

- [Google SRE - Blameless Postmortem for System Resilience](https://sre.google/sre-book/postmortem-culture/) — organizational memory, failure/postmortem learning, knowledge curation, governance, measurable outcome. Google coordinates postmortems across the company, standardizes templates, automates evidence capture, and mines postmortems for trends. Evidence: First-party SRE book describes a named working group and company-wide mechanism; outage reduction is a company claim.

### Khorasan Regional Electric Company

- [Description of Organizational Learning Network and Identification of Factors Influencing Its Formation Using Network Analysis Method (Case Study: Khorasan Regional Electric Company)](https://doi.org/10.47176/smok.2025.1821) — organizational memory, workflow adaptation, knowledge curation. The company's employee learning network carries knowledge through informal social interaction and collaborative work; network analysis identified fragmentation and peripheral knowledge consumers, motivating cross-functional communities and learning facilitators. Evidence: Named single-organization academic study of 327 employees with explicit knowledge-flow mechanisms; recommendations are distinguished from observed findings.

### LG CNS

- [LG CNS builds a self-improving modernization harness with Claude Code](https://www.anthropic.com/customers/lg-cns) — feedback/evals, organizational memory, specialized agents, workflow adaptation, measurable outcome. LG CNS uses persistent file-based memory, multi-agent file handoffs, and deterministic quality measurement in a self-improving modernization harness. Evidence: Named customer implementation; mechanism detail is retained, while results are vendor-published.

### Macquarie Group

- [The (not so) secret ingredient — prioritising continuous improvement](https://medium.com/macquarie-engineering-blog/the-not-so-secret-ingredient-prioritising-continuous-improvement-667f8a4bcdb3) — feedback/evals, experimentation, workflow adaptation, governance, measurable outcome. Macquarie teams use retrospectives, a tracked continuous-improvement backlog, OKRs, and reserved Innovation Days; a reported initiative could reduce support by 40 hours per month. Evidence: First-party engineering account by Macquarie's Chief Scrum Master describes concrete team practices and a company-reported bounded outcome.

### Siemens

- [How Siemens handles 90% of calls autonomously with Amazon Connect Customer AI Agents | AWS Contact Center](https://aws.amazon.com/blogs/contact-center/how-siemens-handles-90-of-calls-autonomously-with-amazon-connect-customer-ai-agents/) — specialized agents, workflow adaptation, measurable outcome. Siemens moved from legacy IVR to production AI-agent routing, validated it in one workflow, and extended it to additional workflows. Evidence: Named customer implementation with vendor-published autonomous-handling results.

### Spotify

- [Better Experiments with LLM Evals — A funnel, not a fork | Spotify Engineering](https://engineering.atspotify.com/2026/5/better-experiments-with-llm-evals-a-funnel-not-a-fork) — feedback/evals, experimentation, workflow adaptation. Spotify continuously recalibrates offline evals against online outcomes to improve their value as verification tools. Evidence: First-party engineering account describes an operational calibration loop.
- [Beyond Winning: Spotify’s Experiments with Learning Framework | Spotify Engineering](https://engineering.atspotify.com/2025/9/spotifys-experiments-with-learning-framework) — experimentation, decision systems, measurable outcome. Spotify uses an Experiments-with-Learning metric to guide investment, testing capacity, and experimentation practice. Evidence: First-party engineering account supplies the decision mechanism and reported learning and win rates.

### Wise

- [Blameless postmortems: Creating an honest and open culture](https://medium.com/wise-engineering/blameless-portmortems-creating-and-honest-and-open-culture-6202b0946a1e) — organizational memory, failure/postmortem learning, knowledge curation, governance. Wise records incident impact, timeline, cause, detection, repair, and prevention steps, then shares postmortems so relevant teams or the whole company can learn. Evidence: First-party engineering account describes Wise's organization-wide incident-learning practice.

### bunq

- [How bunq handles 97% of support with Amazon Bedrock | Artificial Intelligence](https://aws.amazon.com/blogs/machine-learning/how-bunq-handles-97-of-support-with-amazon-bedrock/) — decision systems, specialized agents, workflow adaptation, measurable outcome. bunq runs an orchestrator that routes support work among primary and specialized agents and scales their execution services. Evidence: Named production customer architecture; the support outcome is vendor-published.

## Exclusion audit sample

These records remain accepted as topical corpus sources but do not count as organization evidence.

- `github-explodinggradients-ragas` — vibrantlabsai/ragas: Generic evaluation toolkit; the record does not evidence a named organization's internal learning practice.
- `github-openai-evals` — openai/evals: Generic evaluation framework; repository availability alone is not organization operating evidence.
- `github-promptfoo-promptfoo` — promptfoo/promptfoo: Generic evaluation toolkit; usage by a named organization is not established in this record.
- `github-dastergon-postmortem-templates` — dastergon/postmortem-templates: Generic postmortem templates; no named organization's adoption or operating loop is evidenced.
- `github-joelparkerhenderson-issue-postmortem-template` — joelparkerhenderson/issue-postmortem-template: Generic template repository; it is theory/tooling rather than organization case evidence.
- `github-peter-evans-lightweight-architecture-decision-records` — peter-evans/lightweight-architecture-decision-records: Generic ADR tooling; no named organizational decision practice is established.
- `1mnr6d2` — How valuable are RAG modules + synthetic datasets for boosting an agent’s cognitive depth?: Anonymous exploratory question about RAG and synthetic data; no named organization or deployed practice.
- `1nh9iet` — Idea for AI Agent Collaboration: Real-Time Shared Memory – Thoughts?: Proposed multi-agent memory idea; no named organization or implemented operating mechanism.
- `1qpwwpr` — I made a complete reference guide for building AI agents (200+ scripts from API basics to deployment) — any feedback?: General educational agent-code collection; not evidence of organization learning.
- `1r54kau` — anyone else struggling with agent loops getting stuck on simple logic?: Anonymous implementation question; no named organization and no substantiated organizational mechanism.
