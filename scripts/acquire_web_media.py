#!/usr/bin/env python3
"""Acquire and materialize public web/media lane records.

Network collection is explicit (`--collect`). The bounded candidate manifest is then
deterministically materialized (`--materialize`) so reruns do not depend on live web
responses. No complete third-party page text is stored.
"""

from __future__ import annotations

import argparse
import html
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACQ = ROOT / "research/web-media-acquisition"
MANIFEST = ACQ / "candidate-manifest.jsonl"
QUERY_LEDGER = ACQ / "query-ledger.jsonl"
RETRIEVAL_LEDGER = ACQ / "retrieval-ledger.jsonl"
KEYWORDS = re.compile(
    r"self.improv|organizational learn|learning organization|feedback loop|experiment|"
    r"continuous improvement|retrospective|postmortem|institutional memory|organizational memory|"
    r"agentic|AI.native|AI agent|evaluation|eval.driven|autonomous|knowledge shar|psychological safety|"
    r"blameless|adaptive organization|data flywheel|learn from failure|human.in.the.loop",
    re.I,
)
REJECT_HOSTS = {"youtube.com", "youtu.be", "wikipedia.org", "amazon.com", "goodreads.com"}

EXA_QUERIES = {
    "blogs": [
        ("experimentation", "first-party engineering blog how company experimentation creates organizational learning feedback loops"),
        ("postmortems", "company engineering blog blameless postmortem learning from incidents continuous improvement"),
        ("ai-native", "company engineering blog AI-native operations agents human feedback evaluation learning loop"),
        ("memory", "company blog organizational memory knowledge sharing engineering decisions learning organization"),
        ("platform-learning", "engineering blog internal platform feedback loop improves developer productivity organization"),
        ("retrospectives", "engineering company blog retrospectives continuous improvement team learning"),
        ("data-flywheel", "company engineering blog data flywheel feedback loop product improves from usage"),
        ("evals", "company engineering blog eval-driven development AI agents production feedback"),
        ("adaptive", "company blog adaptive organization learning culture systems thinking"),
        ("failure", "engineering blog failure review learning culture resilience company"),
        ("spotify-netflix", "site:engineering.atspotify.com OR site:netflixtechblog.com experimentation learning feedback"),
        ("uber-airbnb", "site:uber.com/blog/engineering OR site:medium.com/airbnb-engineering experimentation feedback learning"),
    ],
    "case-studies": [
        ("ai-agents", "official customer story company deployed AI agents measured outcome human oversight"),
        ("copilot", "official GitHub customer story Copilot organization productivity learning adoption"),
        ("cloud-ai", "official AWS customer story generative AI agents organization measurable improvement"),
        ("microsoft-ai", "official Microsoft customer story AI transformation agents employee feedback measurable"),
        ("google-ai", "official Google Cloud customer story generative AI operational improvement"),
        ("openai", "site:openai.com/index customer story enterprise AI workflow company"),
        ("anthropic", "site:anthropic.com/customers AI company customer story agents"),
        ("experimentation", "company case study experimentation platform organizational learning measured outcome"),
        ("knowledge", "customer story organizational knowledge management AI measurable outcome"),
        ("continuous-improvement", "case study continuous improvement learning organization company results"),
        ("dev-productivity", "official customer case study developer productivity feedback loop engineering intelligence"),
        ("autonomous", "official case study autonomous enterprise agentic operations customer"),
    ],
    "conferences": [
        ("qcon-learning", "site:infoq.com/presentations organizational learning feedback loops experimentation QCon"),
        ("leaddev", "site:leaddev.com learning organization engineering culture feedback conference talk"),
        ("reinvent", "AWS re:Invent session continuous improvement generative AI agents organization"),
        ("build", "Microsoft Build session AI agents evaluation feedback loop enterprise"),
        ("next", "Google Cloud Next session AI agents enterprise customer learning"),
        ("devops", "conference talk blameless postmortems learning organization DevOps"),
        ("experimentation", "conference talk experimentation platform organizational learning company"),
        ("ai-evals", "conference talk eval-driven AI agents production feedback human oversight"),
        ("org-memory", "conference talk organizational memory knowledge management engineering"),
        ("adaptive", "conference presentation adaptive organization continuous improvement systems thinking"),
    ],
    "podcasts": [
        ("hbr-transcript", "HBR IdeaCast podcast transcript learning organization experimentation psychological safety"),
        ("mckinsey-transcript", "McKinsey podcast transcript organizational transformation learning AI agents"),
        ("lenny-transcript", "Lenny podcast transcript experimentation feedback loops product organization"),
        ("worklab-transcript", "Microsoft WorkLab podcast transcript AI organization learning agents"),
        ("knowledge-project", "Knowledge Project podcast transcript learning organization feedback decisions"),
        ("a16z-transcript", "a16z podcast transcript AI-native company agents enterprise"),
        ("no-priors", "No Priors podcast transcript AI agents company operations evaluation"),
        ("acquired", "Acquired podcast transcript company culture continuous improvement operating system"),
        ("psych-safety", "podcast transcript psychological safety organizational learning Amy Edmondson"),
        ("experiment", "podcast transcript experimentation culture product learning organization"),
        ("autonomous-enterprise", "podcast transcript autonomous enterprise agentic organization"),
        ("engineering", "engineering podcast transcript blameless postmortem feedback loop learning"),
    ],
}

BOOK_QUERIES = [
    "learning organization", "organizational learning", "continuous improvement organization",
    "organizational memory knowledge management", "systems thinking organization",
    "psychological safety learning", "high reliability organization", "Toyota continuous improvement",
    "adaptive enterprise", "self managing organizations", "experimentation culture business",
]
GITHUB_QUERIES = [
    "agent memory", "llm evals", "agent evaluation", "continuous learning agents",
    "AI organizational memory", "self improving agent", "prompt evaluation",
    "agent observability", "knowledge graph memory agents", "autonomous company agents",
]

PRIMARY_CONFERENCE_HOSTS = {
    "infoq.com", "leaddev.com", "zephrcf.leaddev.com", "zporigin.leaddev.com",
    "github.com", "microsoft.github.io", "repost.aws", "devblogs.microsoft.com",
}

CONFERENCE_CITATIONS = [
    "https://www.infoq.com/presentations/culture-continuous-experimentation/",
    "https://www.infoq.com/presentations/heauristic-learning-organization/",
    "https://www.infoq.com/presentations/experiments-agile/",
    "https://www.infoq.com/presentations/responsive-organization/",
    "https://www.infoq.com/presentations/experimentation-mindset/",
    "https://www.infoq.com/presentations/complexity-feedback-loops/",
    "https://www.infoq.com/presentations/controlled-experiments/",
    "https://www.infoq.com/presentations/thoughtworks-high-performance-teams/",
    "https://www.infoq.com/presentations/etsy-deploy/",
    "https://www.infoq.com/presentations/process-evolution-flat-structure/",
    "https://www.infoq.com/presentations/culture-blameless-failure/",
    "https://www.infoq.com/presentations/blame-accountability/",
    "https://www.infoq.com/presentations/ddd-wardley-mapping-team-topology/",
    "https://leaddev.com/management/improving-your-feedback-loop-engineering-teams",
    "https://leaddev.com/career-development/building-learning-culture-unlock-developer-thriving",
    "https://leaddev.com/career-development/learning-core-capability-software-teams-heres-how-measure-it",
    "https://leaddev.com/technical-direction/crowdsourcing-platform-engineering",
    "https://leaddev.com/culture/beyond-timelines-learning-from-incidents",
    "https://leaddev.com/culture/simplify-your-postmortems-and-focus-scaling",
    "https://leaddev.com/leadership/how-mcdonalds-and-jpmorgan-chase-safely-scale-experimentation",
    "https://zephrcf.leaddev.com/velocity/using-learning-themed-retrospective-strengthen-your-teams-learning-culture-and",
    "https://zephrcf.leaddev.com/technical-direction/theory-to-action-architecting-and-implementing-your-team-operating-system",
    "https://zephrcf.leaddev.com/leadership/how-do-netflix-nubank-and-airbrake-achieve-engineering-success",
    "https://zephrcf.leaddev.com/culture/demings-wisdom-for-staff-engineers-a-modern-take-on-timeless-principles",
    "https://zephrcf.leaddev.com/culture/from-hurdles-to-highways-crafting-a-collaborative-experimentation-ecosystem-at-getyourguide",
    "https://zporigin.leaddev.com/culture/great-engineers-are-made-great-engineering-teams",
    "https://github.com/microsoft/Build26-LAB540-observe-optimize-and-protect-your-hosted-agents-in-microsoft-foundry",
    "https://github.com/microsoft/Build26-BRK252-from-observability-to-roi-for-ai-agents-on-any-framework",
    "https://github.com/microsoft/build26-brk241",
    "https://github.com/microsoft/Build26-BRK242-turn-your-agents-into-action-connect-tools-apis-and-documents",
    "https://github.com/microsoft/Build26-BRK240-build-context-aware-agents-from-data-to-decisions/blob/main/README.md",
    "https://microsoft.github.io/build26-next-steps/agents-apps/",
    "https://repost.aws/articles/AR9fNVsR75Q_KYE19tA9E2HQ/re-invent-2025-build-deploy-and-operate-agentic-architectures-on-aws-serverless",
    "https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/",
]

CASE_STUDY_CITATIONS = [
    "https://www.microsoft.com/en/customers/story/26405-premera-blue-cross-microsoft-365",
    "https://cloud.google.com/customers/viesure", "https://openai.com/index/endava/",
    "https://aws.amazon.com/solutions/case-studies/blue-origin-case-study/",
    "https://www.microsoft.com/en/customers/story/25046-microsoft-dynamics-365-customer-service",
    "https://cloud.google.com/blog/topics/customers/how-manipal-hospitals-sped-up-nurse-handoffs-across-37-hospitals",
    "https://aws.amazon.com/solutions/case-studies/genentech-generativeai-case-study/",
    "https://www.anthropic.com/customers/tidio",
    "https://www.microsoft.com/en/customers/story/25660-banco-bradesco-sa-azure-ai-foundry",
    "https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/",
    "https://cloud.google.com/customers/eversana",
    "https://press.aboutamazon.com/aws/2025/12/sansiri-transforms-home-buying-and-ownership-in-thailand-with-generative-ai-on-aws",
    "https://github.com/customer-stories/mercedes-benz",
    "https://fin.ai/customers/anthropic",
    "https://aws.amazon.com/blogs/contact-center/how-siemens-handles-90-of-calls-autonomously-with-amazon-connect-customer-ai-agents/",
    "https://info.rasa.com/hubfs/2026_Case_Studies/Rasa_AlbertHeijn_customerstory.pdf",
    "https://aws.amazon.com/solutions/case-studies/bpc/", "https://openai.com/index/lseg/",
    "https://openai.com/index/dai-nippon-printing/", "https://cloud.google.com/customers/axa-switzerland-ai",
    "https://aws.amazon.com/solutions/case-studies/bayer-china/", "https://cloud.google.com/customers/emccamp",
    "https://openai.com/index/boston-childrens-hospital/", "https://www.anthropic.com/customers/lindy",
    "https://openai.com/index/wayfair/", "https://www.microsoft.com/en/customers/story/25506-danone-microsoft-365-copilot",
    "https://aws.amazon.com/solutions/case-studies/doordash-bedrock-case-study/", "https://openai.com/index/mufg/",
    "https://cloud.google.com/blog/products/ai-machine-learning/how-signal-iduna-supercharges-customer-service-with-gen-ai",
    "https://aws.amazon.com/blogs/machine-learning/how-bunq-handles-97-of-support-with-amazon-bedrock/",
    "https://aws.amazon.com/solutions/case-studies/asapp-case-study/", "https://claude.com/customers/rakuten",
    "https://cloud.google.com/customers/oneassure", "https://claude.com/customers/coinbase",
    "https://www.microsoft.com/en/customers/story/23524-holland-america-line-microsoft-copilot-studio",
    "https://openai.com/index/travelers/", "https://www.microsoft.com/en/customers/story/23194-pegasus-airlines-azure-ai-services",
    "https://www.microsoft.com/en/customers/story/26047-air-india-azure-openai-in-foundry-models",
    "https://github.com/resources/insights/thomson-reuters-ai-adoption", "https://openai.com/index/cisco/",
    "https://cloud.google.com/customers/telusai", "https://decagon.ai/case-studies/hunter-douglas",
    "https://cloud.google.com/customers/sabre", "https://openai.com/index/stadler/",
    "https://www.microsoft.com/en/customers/story/26166-microsoft-microsoft-copilot-studio",
    "https://gradient-labs.ai/customers/digital-bank-at-scale", "https://openai.com/index/bbva/",
    "https://github.com/customer-stories/amd",
    "https://www.microsoft.com/en/customers/story/23738-hitachi-ltd-github-copilot",
    "https://www.microsoft.com/en/customers/story/25676-commerzbank-ag-azure-ai-foundry-agent-service",
    "https://www.microsoft.com/en/customers/story/26197-regal-rexnord-microsoft-copilot-studio",
    "https://claude.com/customers/notion-qa", "https://www.claude.com/customers/slack",
    "https://www.claude.com/customers/figma", "https://claude.com/customers/hubspot",
    "https://www.anthropic.com/customers/lg-cns", "https://www.anthropic.com/customers/advantage-solutions",
    "https://www.anthropic.com/customers/pacific-community-ventures", "https://www.anthropic.com/customers/dust",
    "https://www.anthropic.com/customers/cox-and-accenture", "https://www.anthropic.com/customers/kai",
    "https://www.anthropic.com/customers/box", "https://www.anthropic.com/customers/juno",
    "https://www.anthropic.com/customers/warp", "https://www.anthropic.com/customers/jakala",
    "https://www.anthropic.com/customers/chatplace", "https://www.anthropic.com/customers/brainlabs",
]

BLOG_CITATIONS = [
    "https://confidence.spotify.com/blog/experiment-like-spotify",
    "https://engineering.atspotify.com/2026/5/better-experiments-with-llm-evals-a-funnel-not-a-fork",
    "https://engineering.atspotify.com/2025/9/spotifys-experiments-with-learning-framework",
    "https://www.databricks.com/blog/platform-engineering-building-internal-developer-platforms-improve-developer-productivity",
    "https://sylvain.artois.io/tech/blameless-postmortem-en", "https://easygo.io/blog/engineering-team-scaling-at-speed",
    "https://mixpanel.com/blog/culture-of-experimentation/", "https://developers.openai.com/blog/eval-skills",
    "https://data.blog/2021/03/16/explat-automattics-experimentation-platform/", "https://www.uber.com/us/en/blog/supercharging-a-b-testing-at-uber/",
    "https://www.alibabacloud.com/blog/the-second-half-of-the-enterprise-agent-era-how-to-make-agents-smarter-the-more-they-are-used_603319",
    "https://medium.com/leboncoin-tech-blog/confidence-by-spotify-bringing-a-b-testing-into-the-product-conversation-at-leboncoin-d197e9354854",
    "https://dataworkers.io/blog/what-allspaw-blameless-postmortem-taught-our-incident-agent/", "https://servantium.com/blog/building-an-institutional-memory-engine/",
    "https://codeclimate.com/legacy/plan-retrospectives-with-data", "https://zakhassan.com/blog/building-a-learning-culture-from-incidents-beyond-blameless-postmortems",
    "https://zylos.ai/research/2026-04-16-ai-agent-data-flywheels-production-feedback-loops/", "https://rootly.com/incident-postmortems/blameless",
    "https://www.kitchensoap.com/2013/09/30/learning-from-failure-at-etsy/", "https://dora.dev/capabilities/platform-engineering/",
    "https://simwood.com/2026/07/internal-documentation-that-actually-gets-used-adrs-mcp-servers-and-ai-accessible-knowledge/",
    "https://contextual.ai/blog/optimize-agent-performance-using-self-evolving-context", "https://sre.google/sre-book/postmortem-culture/",
    "https://medium.com/wise-engineering/blameless-portmortems-creating-and-honest-and-open-culture-6202b0946a1e",
    "https://reindeer.ai/blog/inner-loop-outer-loop", "https://labs.scale.com/blog/insights-generator",
    "https://blog.radeuslabs.com/continuous-improvement-in-practice-inside-the-shingo-workshop-at-radues-labs",
    "https://zakhassan.com/blog/building-a-reliability-culture-the-organizational-work-that-makes-sre-stick",
    "https://www.pagerduty.com/eng/production-ai-agents-closing-the-gaps-between-idea-and-reality/", "https://www.nvidia.com/en-us/glossary/data-flywheel/",
    "https://www.atlassian.com/incident-management/postmortem/blameless", "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    "https://medium.com/macquarie-engineering-blog/the-not-so-secret-ingredient-prioritising-continuous-improvement-667f8a4bcdb3",
    "https://incident.io/blog/sre-incident-postmortem-best-practices", "https://blog.antnsn.dev/2026-p5-rre-weekly-reflection-framework/",
    "https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals",
    "https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop", "https://www.canva.dev/blog/engineering/how-we-build-experiments-in-house/",
    "https://www.datadoghq.com/blog/feedback-loops-progressive-delivery/", "https://engineering.monday.com/how-we-shortened-development-feedback-loops-from-30m-to-30s/",
    "https://www.dench.com/blog/ai-for-retrospectives", "https://tianpan.co/blog/2025-09-28-data-flywheels-llm-applications",
    "https://cloud.google.com/blog/topics/developers-practitioners/from-vibe-checks-to-continuous-evaluation-engineering-reliable-ai-agents",
    "https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/",
    "https://www.asapp.com/blog/the-autonomous-agentic-life-cycle-how-the-asapp-cxp-flywheel-works",
    "https://rootly.com/blog/how-we-used-crdts-to-build-real-time-collaborative-retrospectives",
    "https://www.linkedin.com/blog/engineering/ab-testing-experimentation/our-evolution-towards-t-rex-the-prehistory-of-experimentation-i",
    "https://aws.amazon.com/blogs/devops/from-ai-agent-prototype-to-product-lessons-from-building-aws-devops-agent/",
    "https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-reliable-ai-agents", "https://factory.ai/news/factory-signals",
    "https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-organization-blog/is-your-organization-harnessing-the-proven-power-of-learning",
    "https://www.dessia.io/blog/repeated-design-mistakes-engineering-know-how-reuse", "https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/",
    "https://pulsehq.tech/blog/team-re-debating-decisions", "https://www.etsy.com/codeascraft/debriefing-facilitation-guide",
    "https://bloomfire.com/blog/benefits-learning-organization-culture/", "https://bloomfire.com/blog/knowledge-sharing-guide/",
    "https://falconer.com/guides/preserve-institutional-knowledge/", "https://barancezayirli.com/blog/leadership/the-company-knowledge-os",
    "https://tryglen.com/blog/how-to-build-a-company-brain", "https://www.axelerant.com/blog/building-internal-developer-platforms",
    "https://floriancourouge.com/en/blog/platform-engineering-idp", "https://adam-analytics.com/internal-developer-platforms-should-feel-like-products/",
    "https://greyhaven.ai/feed/ai-engineering-flywheel", "https://resources.rework.com/libraries/ai-transformation-saas/telemetry-loops-for-in-product-ai",
    "https://instituteod.com/unlocking-the-power-of-systems-thinking-and-organizational-learning/", "https://drcone.com/2026/05/18/toward-an-adaptive-organizational-intelligence-framework/",
    "https://evolved.institute/blogs/news/adaptiveness-guide-long-version", "https://www.deel.com/blog/learning-organization-examples/",
    "https://noteandsave.com/blog/sre-postmortems/", "https://www.coehub.ai/blog/closing-long-loop-nick-rockwell",
    "https://www.lucasware.com/embracing-agile-principles-in-the-warehouse-continuously-learning-and-improving-with-retrospective-sessions/",
    "https://www.glowbl.com/blog/en/the-retrospective-a-powerful-tool-for-continuous-improvement-",
    "https://codeclimate.com/legacy/culture-of-feedback-engineering", "https://medium.com/hootsuite-engineering/optimizing-the-feedback-loop-a-key-to-great-developer-productivity-f567c4e80c80",
    "https://tianpan.co/blog/2026-04-18-data-flywheel-feedback-loops-engineering-ai-product", "https://www.rootly.com/blog/how-we-used-crdts-to-build-real-time-collaborative-retrospectives",
    "https://www.rework.com/libraries/ai-transformation-saas/telemetry-loops-for-in-product-ai", "https://www.hyscaler.com/insights/internal-developer-platforms-idp-guide/",
    "https://andrewodendaal.com/platform-engineering-internal-developer-platform/", "https://www.oracles.cloud/post-mortem-2-0-building-resilience-from-the-year-s-biggest-",
    "https://www.noteandsave.com/blog/sre-postmortems/", "https://www.falconer.com/guides/preserve-institutional-knowledge/",
]


def make_row(*, lane: str, url: str, title: str, creator: str, publisher: str,
             source_type: str, evidence: str, query_id: str, kind: str = "excerpt",
             published_date: str | None = None, status: str = "accepted",
             retrieval_method: str = "public publisher retrieval") -> dict:
    return {
        "platform": lane, "stable_id": stable_id(lane, url), "title": title,
        "creator": creator, "publisher": publisher, "canonical_url": url,
        "published_date": published_date, "date_precision": "day" if published_date else "unknown",
        "source_type": source_type, "status": status,
        "artifact_level": "transcript" if kind in {"transcript", "timestamped-note"} and status == "accepted" else ("metadata_only" if status == "accepted" else "unavailable"),
        "retrieved_at": now(), "retrieval_method": retrieval_method,
        "provenance": f"Recovered from research/discovery-inventory.md via {query_id}.",
        "rights_status": "bounded-public-evidence" if status == "accepted" else "retrieval-evidence-only",
        "rights_note": "Only a bounded public evidence span is stored; no complete protected work is copied.",
        "relevance_evidence": ["Early project lead directly documents an organizational learning, adaptation, autonomy, or AI operating mechanism."] if status == "accepted" else [],
        "evidence": [{"locator": "public publisher page", "text": bounded_evidence(evidence), "kind": kind}] if evidence else [],
        "query_ids": [query_id], "rejection_reason": None if status == "accepted" else "Public retrieval did not substantiate the earlier discovery claim.",
    }


def collect_early_leads(rows: list[dict], queries: list[dict], retrievals: list[dict]) -> None:
    for lane in [*EXA_QUERIES, "books", "github"]:
        queries.append({"query_id": f"early-inventory-{lane}", "lane": lane, "family": "existing-discovery", "backend": "repository evidence plus public publisher retrieval", "query": "research/discovery-inventory.md and existing lane files", "attempted_at": now(), "outcome": "success", "result_count": 0, "error": None})
    seeds = [
        make_row(lane="blogs", url="https://www.ycombinator.com/library/RB-the-ceo-must-be-the-chief-ai-officer", title="The CEO Must Be the Chief AI Officer", creator="Pedro Franceschi; Y Combinator", publisher="Y Combinator", source_type="article", query_id="early-inventory-blogs", evidence="Brex co-founder and CEO Pedro Franceschi argues AI is a foundation for building products, teams, and companies. Timestamped chapters cover making AI safe for enterprise, rebuilding Brex around AI, and building company AGI."),
        make_row(lane="blogs", url="https://ramp.com/intelligence", title="Ramp Intelligence", creator="Ramp", publisher="Ramp", source_type="article", query_id="early-inventory-blogs", evidence="Ramp says its AI agents are refined through patterns and learnings from customers and work on fraud, expense coding, and policy enforcement."),
        make_row(lane="blogs", url="https://www.brex.com/product/ai", title="Brex AI page retrieval contradiction", creator="Brex", publisher="Brex", source_type="article", query_id="early-inventory-blogs", evidence="The public route returned a 404 page rather than the AI product evidence claimed by the early index.", status="rejected"),
        make_row(lane="blogs", url="https://www.jimcollins.com/concepts/the-flywheel.html", title="The Flywheel Effect", creator="Jim Collins", publisher="Jim Collins", source_type="article", query_id="early-inventory-blogs", evidence="Good-to-great transformations do not happen in one action; repeated turns of a flywheel build organizational momentum toward breakthrough."),
        make_row(lane="blogs", url="https://www.holacracy.org/", title="Holacracy: The Operating System for Self-Management", creator="HolacracyOne", publisher="HolacracyOne", source_type="article", published_date="2022-11-10", query_id="early-inventory-blogs", evidence="The framework defines clear roles, responsibilities, delegation boundaries, and transparent governance for self-management."),
        make_row(lane="blogs", url="https://www.corporate-rebels.com/blog/when-agile-self-management-and-holacracy-fail", title="When Agile, Self-Management, and Holacracy Fail", creator="Pim de Morree", publisher="Corporate Rebels", source_type="article", published_date="2021-12-04", query_id="early-inventory-blogs", evidence="The article examines how organizations copy fashionable self-management methods for the wrong reasons and why implementation fails."),
        make_row(lane="podcasts", url="https://www.leanblog.org/2020/01/amy-edmondson-psychological-safety-speaking-up/", title="Amy Edmondson on Psychological Safety: What It Is, Why Fear Persists, and What Leaders Can Do", creator="Mark Graban; Amy Edmondson", publisher="Lean Blog", source_type="episode", published_date="2020-01-01", query_id="early-inventory-podcasts", kind="transcript", evidence="The public episode page supplies a transcript and detailed discussion of psychological safety, speaking up, and how leaders enable organizational learning from failures."),
        make_row(lane="podcasts", url="https://news.sap.com/2026/06/introducing-autonomous-enterprise-podcast-series/", title="Introducing the Autonomous Enterprise Podcast", creator="Benedikt Gieger; Julia Kloppenburg", publisher="SAP", source_type="episode", published_date="2026-06-10", query_id="early-inventory-podcasts", status="rejected", evidence="The announcement establishes a relevant podcast series about autonomous-enterprise operating models, but no episode transcript or timestamped notes were available on the inspected page."),
        make_row(lane="case-studies", url="https://engineering.ramp.com/", title="Agentic risk operations and AI engineering index", creator="Ramp Engineering", publisher="Ramp", source_type="case-study", query_id="early-inventory-case-studies", evidence="Ramp's engineering index points to agentic risk operations, an accounting benchmark, skill ablation, memory, and a reported autonomous security-repair result."),
        make_row(lane="case-studies", url="https://ramp.com/customers", title="Ramp Customer Stories", creator="Ramp", publisher="Ramp", source_type="case-study", query_id="early-inventory-case-studies", evidence="The customer index names organizations using agents and reports bounded outcomes including finance-team scaling, faster close, and staff hours saved."),
        make_row(lane="case-studies", url="https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/", title="Klarna AI assistant handles two-thirds of customer service chats in its first month", creator="Klarna", publisher="Klarna", source_type="case-study", published_date="2024-02-27", query_id="early-inventory-case-studies", evidence="Klarna reports 2.3 million conversations in the first month, two-thirds of service chats, work equivalent to 700 full-time agents, and customer satisfaction on par with human agents."),
        make_row(lane="case-studies", url="https://www.zenml.io/llmops-database/github-copilot-integration-for-enhanced-developer-productivity", title="Duolingo: GitHub Copilot Integration for Enhanced Developer Productivity", creator="ZenML", publisher="ZenML", source_type="case-study", query_id="early-inventory-case-studies", evidence="The case reports a 25% speed increase for developers new to repositories and 10% for experienced developers, with Copilot, Codespaces, and API integrations supporting consistent standards."),
        make_row(lane="case-studies", url="https://www.self-managementinstitute.org/about-morning-star", title="The Morning Star Company: Self-Management at Scale", creator="Self-Management Institute", publisher="Self-Management Institute", source_type="case-study", query_id="early-inventory-case-studies", evidence="The retrieval backend could not find the public page, so the early lead is preserved without substantive evidence.", status="rejected"),
    ]
    for row in seeds:
        rows.append(row)
        retrievals.append({"stable_id": row["stable_id"], "lane": row["platform"], "attempted_at": now(), "method": row["retrieval_method"], "url": row["canonical_url"], "outcome": "retrieved" if row["status"] == "accepted" else "rejected", "http_status": None, "artifact_observed": row["artifact_level"], "note": row.get("rejection_reason") or "Early lead recovered with bounded evidence."})


def collect_lenny_transcripts(rows: list[dict], queries: list[dict], retrievals: list[dict]) -> None:
    qid = "github-citation-lennys-podcast-transcripts"
    with tempfile.TemporaryDirectory(prefix="web-media-podcasts-") as tmp:
        proc = subprocess.run(["gh", "repo", "clone", "ChatPRD/lennys-podcast-transcripts", tmp, "--", "--depth=1"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        files = sorted(Path(tmp).glob("episodes/*/transcript.md")) if proc.returncode == 0 else []
        scored = []
        for path in files:
            text = path.read_text(errors="replace")
            matches = list(KEYWORDS.finditer(text))
            distinct = len({m.group(0).casefold() for m in matches})
            if distinct >= 2 and len(matches) >= 4:
                scored.append((distinct, len(matches), path, text))
        scored.sort(key=lambda item: (-item[0], -item[1], item[2].parent.name))
        queries.append({"query_id": qid, "lane": "podcasts", "family": "citation-chasing-public-timestamped-transcripts", "backend": "GitHub CLI public repository", "query": "ChatPRD/lennys-podcast-transcripts episodes with multiple corpus mechanisms", "attempted_at": now(), "outcome": "blocked" if proc.returncode else "success", "result_count": len(scored), "error": clean(proc.stderr)[:500] if proc.returncode else None})
        for _, _, path, text in scored[:32]:
            head, body = text.split("---", 2)[1:]
            def field(name: str) -> str | None:
                match = re.search(rf"(?m)^{re.escape(name)}:\s*['\"]?(.*?)['\"]?$", head)
                return clean(match.group(1)) if match else None
            video_id = field("video_id")
            url = field("youtube_url") or f"https://github.com/ChatPRD/lennys-podcast-transcripts/tree/main/episodes/{path.parent.name}"
            match = None
            start = None
            timestamps = list(re.finditer(r"\(\d{1,2}:\d{2}(?::\d{2})?\)", body))
            for candidate in KEYWORDS.finditer(body):
                previous = [stamp for stamp in timestamps if stamp.start() <= candidate.start()]
                if previous and candidate.start() - previous[-1].start() <= 480:
                    match, start = candidate, previous[-1].start()
                    break
            if match is None or start is None:
                continue
            evidence = clean(body[start : min(len(body), start + 680)])
            sid = f"podcasts-lenny-{video_id or path.parent.name}"
            row = {
                "platform": "podcasts", "stable_id": sid, "title": field("title") or path.parent.name,
                "creator": field("guest") or "Unknown guest", "publisher": "Lenny's Podcast",
                "canonical_url": url, "published_date": iso_date(field("publish_date")), "date_precision": "day" if field("publish_date") else "unknown",
                "source_type": "episode", "status": "accepted", "artifact_level": "transcript",
                "retrieved_at": now(), "retrieval_method": "GitHub public transcript citation; original publisher video identified in front matter",
                "provenance": f"Public timestamped transcript at ChatPRD/lennys-podcast-transcripts/{path.parent.name}; original video ID {video_id or 'unknown'}.",
                "rights_status": "bounded-public-evidence", "rights_note": "The public transcript repository asserts no license; only a bounded timestamped span is preserved, and no complete transcript is copied.",
                "relevance_evidence": ["Multiple transcript passages match organizational feedback, experimentation, learning, memory, or AI-agent operating mechanisms."],
                "evidence": [{"locator": f"public transcript near matched timestamp ({path.parent.name})", "text": evidence, "kind": "transcript"}],
                "query_ids": [qid], "transcript_source": f"https://github.com/ChatPRD/lennys-podcast-transcripts/blob/main/episodes/{path.parent.name}/transcript.md",
                "rejection_reason": None,
            }
            rows.append(row)
            retrievals.append({"stable_id": sid, "lane": "podcasts", "attempted_at": now(), "method": "GitHub CLI public repository citation chasing", "url": row["transcript_source"], "outcome": "retrieved", "http_status": 200, "artifact_observed": "transcript", "note": "Timestamped transcript observed; bounded span retained."})


def fetch_public_page(url: str) -> tuple[str, str | None]:
    reader_url = "https://r.jina.ai/" + url
    errors = []
    try:
        request = urllib.request.Request(reader_url, headers={"User-Agent": "corpus-web-media-research/1.0"})
        with urllib.request.urlopen(request, timeout=35) as response:
            return response.read().decode("utf-8", "replace"), None
    except Exception as exc:
        errors.append(f"reader {type(exc).__name__}: {exc}")
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; corpus-web-media-research/1.0)"})
        with urllib.request.urlopen(request, timeout=35) as response:
            raw = response.read(750_000).decode("utf-8", "replace")
        title = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
        text = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", raw)
        text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", text))
        return (f"Title: {clean(title.group(1))}\n" if title else "") + clean(text), None
    except Exception as exc:
        errors.append(f"origin {type(exc).__name__}: {exc}")
        return "", "; ".join(errors)


def collect_citation_catalog(rows: list[dict], queries: list[dict], retrievals: list[dict], catalogs: list[tuple[str, list[str]]] | None = None) -> None:
    catalogs = catalogs or [("blogs", BLOG_CITATIONS), ("conferences", CONFERENCE_CITATIONS), ("case-studies", CASE_STUDY_CITATIONS)]
    for lane, urls in catalogs:
        qid = f"citation-catalog-{lane}"
        with ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(fetch_public_page, urls))
        success_count = sum(not error for _, error in results)
        queries.append({"query_id": qid, "lane": lane, "family": "citation-chasing-primary-sources", "backend": "agent-reach documented Jina public reader", "query": f"Previously discovered and manually audited primary {lane} URLs", "attempted_at": now(), "outcome": "success" if success_count else "blocked", "result_count": success_count, "error": None if success_count else "All public page retrievals failed; individual evidence is in retrieval ledger."})
        for url, (page, error) in zip(urls, results):
            title_match = re.search(r"(?m)^(?:Title:\s*|#\s+)(.+)$", page)
            title = clean(title_match.group(1)) if title_match else slug(urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1])
            evidence = bounded_evidence(page, 650) if page else ""
            relevant = bool(KEYWORDS.search(title + " " + evidence)) and len(evidence) >= 100
            status = "accepted" if relevant else ("blocked" if error else "rejected")
            sid = stable_id(lane, url)
            row = {
                "platform": lane, "stable_id": sid, "title": title, "creator": host(url), "publisher": host(url),
                "canonical_url": url, "published_date": iso_date(page[:1500]), "date_precision": "day" if iso_date(page[:1500]) else "unknown",
                "source_type": "talk" if lane == "conferences" else ("case-study" if lane == "case-studies" else "article"), "status": status,
                "artifact_level": "metadata_only" if status == "accepted" else "unavailable", "retrieved_at": now(),
                "retrieval_method": "agent-reach documented Jina public reader",
                "provenance": f"Primary URL recovered from earlier Exa discovery and citation chasing; catalog query {qid}.",
                "rights_status": "bounded-public-evidence" if status == "accepted" else "retrieval-evidence-only",
                "rights_note": "Only a bounded public evidence span is stored; no complete third-party page, PDF, or talk transcript is copied.",
                "relevance_evidence": ["Primary source evidence describes a learning, evaluation, feedback, adaptation, or agentic operating mechanism."] if status == "accepted" else [],
                "evidence": [{"locator": "public primary page", "text": evidence, "kind": "excerpt"}] if evidence else [],
                "query_ids": [qid], "rejection_reason": None if status == "accepted" else (error or "Page retrieval did not expose enough substantive topical evidence."),
            }
            rows.append(row)
            retrievals.append({"stable_id": sid, "lane": lane, "attempted_at": now(), "method": "agent-reach/Jina public reader", "url": url, "outcome": "retrieved" if status == "accepted" else status, "http_status": None, "artifact_observed": row["artifact_level"], "note": row.get("rejection_reason") or "Bounded primary-page evidence captured."})


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def bounded_evidence(text: str, limit: int = 620) -> str:
    text = clean(text.replace("...", " "))
    match = KEYWORDS.search(text)
    start = max(0, (match.start() if match else 0) - 120)
    span = text[start : start + limit]
    if start and " " in span:
        span = span.split(" ", 1)[1]
    if len(span) == limit and " " in span:
        span = span.rsplit(" ", 1)[0]
    return span


def host(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value[:80] or "source"


def stable_id(lane: str, url: str) -> str:
    return f"{lane}-{hashlib.sha256(url.encode()).hexdigest()[:16]}"


def parse_exa(text: str) -> list[dict]:
    records = []
    for block in re.split(r"\n---\n", text):
        title = re.search(r"(?:^|\n)Title: (.+)", block)
        url = re.search(r"(?:^|\n)URL: (https?://\S+)", block)
        if not title or not url:
            continue
        published = re.search(r"(?:^|\n)Published: (.+)", block)
        author = re.search(r"(?:^|\n)Author: (.+)", block)
        highlights = block.split("Highlights:\n", 1)[-1]
        records.append({
            "title": clean(title.group(1)), "url": url.group(1).rstrip(".,"),
            "published": clean(published.group(1)) if published else None,
            "author": clean(author.group(1)) if author else None,
            "highlights": highlights,
        })
    return records


def exa_search(query: str, limit: int = 12) -> tuple[list[dict], str | None]:
    payload = json.dumps({"query": query, "numResults": limit})
    proc = subprocess.run(
        ["mcporter", "call", "exa.web_search_exa", "--args", payload, "--output", "text", "--timeout", "30000"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45,
    )
    if proc.returncode:
        return [], clean(proc.stderr or proc.stdout)[:500]
    try:
        return parse_exa(proc.stdout), None
    except Exception as exc:
        return [], f"invalid Exa response: {type(exc).__name__}: {exc}"


def iso_date(value: str | None) -> str | None:
    if not value or value in {"N/A", "null"}:
        return None
    match = re.match(r"(\d{4}-\d{2}-\d{2})", value)
    if match:
        return match.group(1)
    match = re.match(r"(\d{4})", value)
    return f"{match.group(1)}-01-01" if match else None


def collect_exa(rows: list[dict], queries: list[dict], retrievals: list[dict]) -> None:
    seen = set()
    for lane, families in EXA_QUERIES.items():
        for family, query in families:
            query_id = f"exa-{lane}-{family}"
            results, error = exa_search(query)
            queries.append({"query_id": query_id, "lane": lane, "family": family, "backend": "agent-reach/exa", "query": query, "attempted_at": now(), "outcome": "blocked" if error else "success", "result_count": len(results), "error": error})
            for item in results:
                url = item["url"]
                key = (lane, url.split("#", 1)[0].rstrip("/"))
                if key in seen:
                    continue
                seen.add(key)
                evidence = bounded_evidence(item["highlights"])
                relevant = bool(KEYWORDS.search(item["title"] + " " + evidence))
                podcast_proof = lane != "podcasts" or bool(re.search(r"transcript|\b\d{1,2}:\d{2}\b", item["highlights"], re.I))
                rejected_host = host(url) in REJECT_HOSTS
                status = "accepted" if relevant and podcast_proof and not rejected_host and len(evidence) >= 120 else "rejected"
                kind = "transcript" if lane == "podcasts" and podcast_proof else "excerpt"
                sid = stable_id(lane, url)
                row = {
                    "platform": lane, "stable_id": sid, "title": item["title"],
                    "creator": item["author"] if item["author"] not in {None, "N/A"} else host(url),
                    "publisher": host(url), "canonical_url": url,
                    "published_date": iso_date(item["published"]), "date_precision": "day" if iso_date(item["published"]) else "unknown",
                    "source_type": {"blogs": "article", "case-studies": "case-study", "conferences": "talk", "podcasts": "episode"}[lane],
                    "status": status, "artifact_level": "transcript" if lane == "podcasts" and status == "accepted" else ("metadata_only" if status == "accepted" else "unavailable"),
                    "retrieved_at": now(), "retrieval_method": "agent-reach Exa public web search",
                    "provenance": f"Discovered by {query_id}; bounded public search evidence preserved.",
                    "rights_status": "bounded-public-evidence" if status == "accepted" else "retrieval-evidence-only",
                    "rights_note": "Only a short public evidence span is stored; no complete third-party page or transcript is copied.",
                    "relevance_evidence": [f"The public page evidence directly addresses the {family} query family and a learning/adaptation mechanism."] if status == "accepted" else [],
                    "evidence": [{"locator": "public page/search retrieval", "text": evidence, "kind": kind}] if evidence else [],
                    "query_ids": [query_id], "rejection_reason": None if status == "accepted" else "Insufficient substantive relevance, disallowed host, or no transcript/timestamp proof.",
                }
                rows.append(row)
                retrievals.append({"stable_id": sid, "lane": lane, "attempted_at": now(), "method": "agent-reach/exa", "url": url, "outcome": "retrieved" if evidence else "blocked", "http_status": None, "artifact_observed": row["artifact_level"], "note": row.get("rejection_reason") or "Bounded evidence captured."})


def collect_books(rows: list[dict], queries: list[dict], retrievals: list[dict]) -> None:
    seen = set()
    for index, query in enumerate(BOOK_QUERIES, 1):
        qid = f"google-books-{index:02d}"
        url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({"q": query, "maxResults": 20, "printType": "books"})
        try:
            with urllib.request.urlopen(url, timeout=25) as response:
                data = json.load(response)
            items, error = data.get("items", []), None
        except Exception as exc:  # network evidence is recorded, not hidden
            items, error = [], f"{type(exc).__name__}: {exc}"
        queries.append({"query_id": qid, "lane": "books", "family": slug(query), "backend": "Google Books public API", "query": query, "attempted_at": now(), "outcome": "blocked" if error else "success", "result_count": len(items), "error": error})
        if error:
            ol_qid = f"openlibrary-books-{index:02d}"
            ol_url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({"q": query, "limit": 20, "fields": "key,title,author_name,first_publish_year,publisher,isbn"})
            try:
                request = urllib.request.Request(ol_url, headers={"User-Agent": "corpus-web-media-research/1.0 (public metadata only)"})
                with urllib.request.urlopen(request, timeout=25) as response:
                    ol_data = json.load(response)
                ol_items, ol_error = ol_data.get("docs", []), None
            except Exception as exc:
                ol_items, ol_error = [], f"{type(exc).__name__}: {exc}"
            queries.append({"query_id": ol_qid, "lane": "books", "family": slug(query), "backend": "Open Library public Search API", "query": query, "attempted_at": now(), "outcome": "blocked" if ol_error else "success", "result_count": len(ol_items), "error": ol_error})
            for doc in ol_items:
                key = doc.get("key", "")
                if not key:
                    continue
                items.append({"id": key.rsplit("/", 1)[-1], "volumeInfo": {"title": doc.get("title"), "authors": doc.get("author_name", []), "publisher": (doc.get("publisher") or ["Unknown"])[0], "publishedDate": str(doc.get("first_publish_year") or ""), "industryIdentifiers": [{"identifier": value} for value in (doc.get("isbn") or [])[:3]], "canonical_openlibrary_key": key}, "_backend": "Open Library public Search API", "_query_id": ol_qid})
        for item in items:
            info = item.get("volumeInfo", {})
            gid = item.get("id")
            if not gid or gid in seen or not info.get("title"):
                continue
            seen.add(gid)
            description = bounded_evidence(info.get("description", ""))
            topical = bool(KEYWORDS.search(" ".join([query, info.get("title", ""), description])))
            status = "accepted" if topical else "rejected"
            is_openlibrary = item.get("_backend") is not None
            curl = f"https://openlibrary.org{info['canonical_openlibrary_key']}" if is_openlibrary else f"https://books.google.com/books?id={gid}"
            published = iso_date(info.get("publishedDate"))
            sid = f"books-google-{gid}"
            row = {
                "platform": "books", "stable_id": sid, "title": info["title"],
                "creator": "; ".join(info.get("authors", [])) or "Unknown", "publisher": info.get("publisher") or "Unknown",
                "canonical_url": curl, "published_date": published, "date_precision": "day" if published and re.match(r"\d{4}-\d{2}-\d{2}$", info.get("publishedDate", "")) else ("year" if published else "unknown"),
                "source_type": "book", "status": status, "artifact_level": "metadata_only" if status == "accepted" else "unavailable",
                "retrieved_at": now(), "retrieval_method": item.get("_backend", "Google Books public API"),
                "provenance": f"Public bibliographic record {gid}; discovered by {item.get('_query_id', qid)}.",
                "rights_status": "metadata-only", "rights_note": "Bibliographic metadata and at most a bounded publisher/API description are stored; no book text is copied.",
                "relevance_evidence": [f"Title/description matches the corpus query family: {query}."] if status == "accepted" else [],
                "evidence": [{"locator": "Google Books volume description", "text": description, "kind": "description"}] if description else [],
                "query_ids": [item.get("_query_id", qid)], "identifiers": {"catalog_id": gid, "isbn": [x.get("identifier") for x in info.get("industryIdentifiers", []) if x.get("identifier")]},
                "rejection_reason": None if status == "accepted" else "Metadata did not establish topical relevance.",
            }
            rows.append(row)
            retrievals.append({"stable_id": sid, "lane": "books", "attempted_at": now(), "method": item.get("_backend", "Google Books public API"), "url": curl, "outcome": "retrieved", "http_status": 200, "artifact_observed": row["artifact_level"], "note": "Metadata retrieved; complete text not requested."})


def dedupe_and_bound(rows: list[dict], retrievals: list[dict]) -> list[dict]:
    """Remove mirrors/duplicates and retain a reviewable accepted set near each gate."""
    targets = {"blogs": 85, "podcasts": 35, "books": 30, "conferences": 35, "case-studies": 55, "github": 35}
    accepted = defaultdict(int)
    seen_urls = set()
    seen_titles = set()
    result = []
    for row in rows:
        row_host = host(row["canonical_url"])
        forced_reason = None
        if row["platform"] == "blogs" and ("substack.com" in row_host or row_host == "doi.org" or row_host == "webflow.rootly.com"):
            forced_reason = "Wrong lane (newsletter/academic) or duplicate publisher mirror; preserved but not counted as a blog."
        if row["platform"] == "blogs" and re.search(r"page not found|\b404\b", row["title"], re.I):
            forced_reason = "Stale or missing publisher page; retrieval evidence preserved but not accepted."
        if row["platform"] == "books" and "organic chemistry" in row["title"].casefold():
            forced_reason = "Lexical false positive for 'learning organization'; unrelated chemistry book."
        if row["platform"] == "conferences" and row_host not in PRIMARY_CONFERENCE_HOSTS:
            forced_reason = "Third-party recap or general documentation, not a primary conference talk/proceeding page."
        if row["platform"] == "case-studies" and (row_host == "p.rst.im" or row["canonical_url"].rstrip("/").endswith(("/ai/generative-ai/customers", "/features/copilot/copilot-business")) or row["title"].startswith("Search code, repositories")):
            forced_reason = "Mirror, aggregate index, or product page rather than a distinct substantive case study."
        if forced_reason and row["status"] == "accepted":
            row["status"] = "rejected"
            row["artifact_level"] = "unavailable"
            row["rejection_reason"] = forced_reason
            row["relevance_evidence"] = []
        parts = urllib.parse.urlsplit(row["canonical_url"])
        query = urllib.parse.urlencode(sorted((key, value) for key, value in urllib.parse.parse_qsl(parts.query, keep_blank_values=True) if not key.casefold().startswith("utm_") and key.casefold() not in {"gh_src", "ref", "source"}))
        curl = urllib.parse.urlunsplit((parts.scheme.casefold(), parts.netloc.casefold().removeprefix("www."), parts.path.rstrip("/") or "/", query, "")).casefold()
        title_key = (re.sub(r"\W+", " ", row["title"].casefold()).strip(), row["publisher"].casefold())
        if curl in seen_urls or title_key in seen_titles:
            retrievals.append({"stable_id": row["stable_id"], "lane": row["platform"], "attempted_at": now(), "method": "deterministic deduplication", "url": row["canonical_url"], "outcome": "rejected", "http_status": None, "artifact_observed": row["artifact_level"], "note": "Duplicate URL or normalized title/publisher; retrieval evidence retained but no duplicate record materialized."})
            continue
        seen_urls.add(curl)
        seen_titles.add(title_key)
        if row["status"] == "accepted":
            lane = row["platform"]
            if accepted[lane] >= targets[lane]:
                row["status"] = "rejected"
                row["artifact_level"] = "unavailable"
                row["rejection_reason"] = "Relevant discovery held outside the bounded accepted review set; evidence preserved and not counted."
                row["relevance_evidence"] = []
            else:
                accepted[lane] += 1
        result.append(row)
    return result


def gh_json(args: list[str]) -> tuple[object | None, str | None]:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    if proc.returncode:
        return None, clean(proc.stderr)[:500]
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid gh JSON: {exc}"


def collect_github(rows: list[dict], queries: list[dict], retrievals: list[dict]) -> None:
    seen = set()
    for index, query in enumerate(GITHUB_QUERIES, 1):
        qid = f"github-repos-{index:02d}"
        items, error = gh_json(["search", "repos", query, "--sort", "stars", "--limit", "30", "--json", "fullName,url,description,createdAt,pushedAt,license,owner,stargazersCount,isFork,isArchived"])
        items = items or []
        queries.append({"query_id": qid, "lane": "github", "family": slug(query), "backend": "GitHub CLI/API", "query": query, "attempted_at": now(), "outcome": "blocked" if error else "success", "result_count": len(items), "error": error})
        for item in items:
            name = item["fullName"]
            if name in seen or item.get("isFork") or item.get("isArchived"):
                continue
            seen.add(name)
            readme, readme_error = gh_json(["api", f"repos/{name}/readme", "-H", "Accept: application/vnd.github.raw+json"])
            if isinstance(readme, str):
                readme_text = readme
            else:
                proc = subprocess.run(["gh", "api", f"repos/{name}/readme", "-H", "Accept: application/vnd.github.raw+json"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
                readme_text = proc.stdout if proc.returncode == 0 else ""
                readme_error = clean(proc.stderr)[:300] if proc.returncode else None
            evidence = bounded_evidence(" ".join([item.get("description") or "", readme_text]))
            relevant = bool(KEYWORDS.search(" ".join([query, item.get("description") or "", evidence]))) and len(evidence) >= 100
            status = "accepted" if relevant else "rejected"
            sid = f"github-{slug(name)}"
            license_name = item.get("license") or "NOASSERTION"
            row = {
                "platform": "github", "stable_id": sid, "title": name,
                "creator": item.get("owner", {}).get("login") if isinstance(item.get("owner"), dict) else name.split("/", 1)[0],
                "publisher": "GitHub", "canonical_url": item["url"], "published_date": iso_date(item.get("createdAt")), "date_precision": "day",
                "source_type": "repository", "status": status, "artifact_level": "metadata_only" if status == "accepted" else "unavailable",
                "retrieved_at": now(), "retrieval_method": "GitHub CLI/API repository search and README endpoint",
                "provenance": f"GitHub repository {name}; discovered by {qid}.",
                "rights_status": "open-license" if license_name != "NOASSERTION" else "bounded-public-evidence",
                "rights_note": f"Repository license reported by GitHub: {license_name}. Only a bounded README/description span is stored.",
                "relevance_evidence": [f"Repository supplies infrastructure for the {query} learning/evaluation mechanism."] if status == "accepted" else [],
                "evidence": [{"locator": "repository description/README", "text": evidence, "kind": "excerpt"}] if evidence else [],
                "query_ids": [qid], "repository": {"full_name": name, "stars_at_retrieval": item.get("stargazersCount"), "last_push": item.get("pushedAt"), "license": license_name},
                "rejection_reason": None if status == "accepted" else "README/description did not establish a substantive learning or evaluation mechanism.",
            }
            rows.append(row)
            retrievals.append({"stable_id": sid, "lane": "github", "attempted_at": now(), "method": "GitHub CLI/API", "url": item["url"], "outcome": "retrieved" if evidence else "blocked", "http_status": 200 if evidence else None, "artifact_observed": row["artifact_level"], "note": readme_error or "Bounded README/description evidence captured."})


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def collect() -> None:
    rows: list[dict] = []
    queries: list[dict] = []
    retrievals: list[dict] = []
    collect_early_leads(rows, queries, retrievals)
    collect_lenny_transcripts(rows, queries, retrievals)
    collect_citation_catalog(rows, queries, retrievals)
    collect_exa(rows, queries, retrievals)
    collect_books(rows, queries, retrievals)
    collect_github(rows, queries, retrievals)
    rows = dedupe_and_bound(rows, retrievals)
    dump_jsonl(MANIFEST, rows)
    dump_jsonl(QUERY_LEDGER, queries)
    dump_jsonl(RETRIEVAL_LEDGER, retrievals)
    print(f"collected candidates={len(rows)} queries={len(queries)} retrievals={len(retrievals)}")


def augment_cases() -> None:
    rows = [json.loads(line) for line in MANIFEST.read_text().splitlines() if line.strip()]
    queries = [json.loads(line) for line in QUERY_LEDGER.read_text().splitlines() if line.strip()]
    retrievals = [json.loads(line) for line in RETRIEVAL_LEDGER.read_text().splitlines() if line.strip()]
    collect_citation_catalog(rows, queries, retrievals, [("case-studies", CASE_STUDY_CITATIONS[-16:])])
    rows = dedupe_and_bound(rows, retrievals)
    dump_jsonl(MANIFEST, rows)
    dump_jsonl(QUERY_LEDGER, queries)
    dump_jsonl(RETRIEVAL_LEDGER, retrievals)
    print(f"augmented candidates={len(rows)}")


def refresh_podcasts() -> None:
    rows = [json.loads(line) for line in MANIFEST.read_text().splitlines() if line.strip() and not json.loads(line).get("stable_id", "").startswith("podcasts-lenny-")]
    queries = [json.loads(line) for line in QUERY_LEDGER.read_text().splitlines() if line.strip()]
    retrievals = [json.loads(line) for line in RETRIEVAL_LEDGER.read_text().splitlines() if line.strip()]
    collect_lenny_transcripts(rows, queries, retrievals)
    rows = dedupe_and_bound(rows, retrievals)
    dump_jsonl(MANIFEST, rows)
    dump_jsonl(QUERY_LEDGER, queries)
    dump_jsonl(RETRIEVAL_LEDGER, retrievals)
    print(f"refreshed podcast candidates={len(rows)}")


def materialize() -> None:
    rows = [json.loads(line) for line in MANIFEST.read_text().splitlines() if line.strip()]
    for lane in [*EXA_QUERIES, "books", "github"]:
        root = ROOT / "sources" / lane
        for status in ("accepted", "rejected", "blocked"):
            (root / status).mkdir(parents=True, exist_ok=True)
            for old in (root / status).glob("*.json"):
                old.unlink()
    for row in rows:
        evidence = row["evidence"]
        row["schema_version"] = 2
        row["content_sha256"] = hashlib.sha256(json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        # Human-readable title first; the stable ID suffix makes collisions impossible.
        filename = f"{slug(row['title'])}--{slug(row['stable_id'])}.json"
        out = ROOT / "sources" / row["platform"] / row["status"] / filename
        out.write_text(json.dumps(row, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"materialized records={len(rows)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--augment-cases", action="store_true")
    parser.add_argument("--refresh-podcasts", action="store_true")
    parser.add_argument("--materialize", action="store_true")
    args = parser.parse_args()
    if not args.collect and not args.augment_cases and not args.refresh_podcasts and not args.materialize:
        parser.error("choose --collect, --augment-cases, --refresh-podcasts, and/or --materialize")
    if args.collect:
        collect()
    if args.augment_cases:
        augment_cases()
    if args.refresh_podcasts:
        refresh_podcasts()
    if args.materialize:
        materialize()


if __name__ == "__main__":
    main()
