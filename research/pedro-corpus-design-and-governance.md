## Priority finding: the YC “Pedro” video

**Identified:** [“The Most AI-Pilled CEO We Know”](https://youtu.be/mPAHvz8kW24), a Y Combinator/Lightcone interview with **Pedro Franceschi**, Brex co-founder and CEO.

- **Official YC Library page and transcript:**  
  https://www.ycombinator.com/library/RB-the-ceo-must-be-the-chief-ai-officer
- **YouTube:**  
  https://youtu.be/mPAHvz8kW24
- **Relevant official chapter:** **43:50 — “Building Company AGI”**

### Pedro’s knowledge-gathering approach

Pedro does **not** advocate putting every company document indiscriminately into one monolithic model. His approach is:

1. **Capture broad raw context**, but curate aggressively.
   - His personal system contained roughly **350,000 Markdown pages** at **48:05–48:14**.
   - At **50:46–51:09**, Garry Tan describes ingesting a **60 GB Google Takeout**, then using code to select only about **4,000 consequential emails**. This latter example is Garry’s, not Pedro’s, but Pedro agrees that organizing context is the bottleneck.

2. **Organize knowledge around bounded domains and operational objects.**
   - **43:57–44:33:** Pedro rejects “a single company model that has every piece of data … with no judgment or lens.”
   - Instead, build a specialized virtual employee/world model that understands **everything material about one customer**, with explicit boundaries, APIs, consumers, and dependencies.

3. **Compose the company brain from multiple specialized models/agents.**
   - **44:35–45:11:** A customer-world agent can feed a separate product-roadmap agent.
   - He explicitly separates:
     - systems that talk to customers,
     - systems that reason over those conversations and propose roadmap changes,
     - systems that emit code.

4. **Validate knowledge through actual operational use.**
   - **45:12–46:12:** Pedro calls this a “Tesla for AI” philosophy: a model matters only if people use it and it demonstrably saves labor or time.
   - Brex’s sales organization uses a customer world model combining account information and support signals; Pedro says it surfaced facts even the team had missed.

5. **Turn every human exception into an evaluation case.**
   - **46:31–47:42:** Human intervention in a KYC exception becomes a new eval.
   - A problematic conversation with Brex’s expense agent creates a bug; another agent modifies code/prompts to make the eval pass, escalating to an engineer if automation cannot.
   - Pedro’s core criticism: companies build an agent but fail to design how it will **improve every day**.

6. **Run a recurring “dream cycle.”**
   - **47:44–47:59:** Review interactions, failures, and patterns—ideally nightly—and incorporate what was learned into product behavior and evals.

7. **Treat context architecture as the bottleneck.**
   - **49:22–49:33:** “How do you organize the context for the model … that is the bottleneck for most things.”

**Compact formulation:**  
`capture → filter/structure by domain → deploy bounded world models → observe real use → convert exceptions into evals → repair code/prompts → rerun evals → repeat nightly`

---

# Six research lanes

## 1. Self-driving/autonomous company visions

### Strong primary evidence

- **YC: Pedro Franceschi, “The Most AI-Pilled CEO We Know”**  
  https://youtu.be/mPAHvz8kW24  
  https://www.ycombinator.com/library/RB-the-ceo-must-be-the-chief-ai-officer  
  The company is decomposed into domain-specific virtual employees/world models, not one undifferentiated corporate AGI.

- **YC talk: recursive, self-improving AI company**  
  https://youtu.be/X_JsIHUfUjc  
  Particularly:
  - **1:44–2:43:** make domain knowledge in heads, Slack, email, and Notion legible; reconceive the company as recursive self-improving AI loops.
  - **2:45–3:50:** loop architecture: sensors → policy/decision rules → deterministic tools → quality gates → learning mechanism.
  - **~9:00 onward:** record organizational activity, synthesize it, and maintain living knowledge artifacts.
  
- **Jack Dorsey / Block: “From Hierarchy to Intelligence”**  
  https://block.xyz/inside/from-hierarchy-to-intelligence  
  Primary corporate articulation of replacing hierarchical information routing with an intelligence layer.

- **Dorsey interview: “Every Company Can Now Be a Mini-AGI”**  
  https://sequoiacap.com/podcast/jack-dorsey-every-company-can-now-be-a-mini-agi/

### Synthesis

The credible “autonomous company” vision is not a CEO-replacement chatbot. It is an organization with:

- machine-readable institutional context,
- domain-bounded agents,
- explicit tools and authority limits,
- event/sensor streams from operations,
- automated evaluation and repair,
- humans retained for judgment, accountability, novelty, ethics, and high-stakes relationships.

---

## 2. Recursive self-improvement in organizations

### Evidence and precedents

- **YC recursive loop talk:** https://youtu.be/X_JsIHUfUjc
  - Sensors: customer email, tickets, churn, telemetry, code changes.
  - Policy layer: what may run autonomously, what needs approval, what must be logged.
  - Tool layer: deterministic APIs.
  - Quality gate: evals, safety filters, human review.
  - Learning mechanism: detect failure and feed it back into system improvement.
  - The cited YC implementation monitored unsuccessful employee queries, diagnosed missing tools/skills/indexes, generated a code change, reviewed it, and deployed it overnight.

- **Pedro/Brex “human interaction becomes an eval”:**  
  https://youtu.be/mPAHvz8kW24?t=2791  
  Approximately **46:31–47:42**.

- **Chris Argyris: double-loop learning background**  
  https://infed.org/dir/welcome/chris-argyris-theories-of-action-double-loop-learning-and-organizational-learning/  
  Useful distinction:
  - single-loop: improve actions while holding goals/rules fixed;
  - double-loop: revise the governing assumptions, policies, or goals themselves.

### Design implication

Use two improvement loops:

- **Inner loop:** repair prompts, tools, retrieval, routing, or code against fixed evals.
- **Outer loop:** humans periodically review whether the objectives, metrics, policies, and eval set themselves remain valid.

Purely automated self-improvement without the outer loop risks optimizing a stale or harmful proxy.

---

## 3. Knowledge management and organizational memory

### Sources

- **GitLab Handbook:**  
  https://handbook.gitlab.com/handbook/  
  GitLab describes its handbook as the central repository for how the company operates.

- **GitLab handbook-first practice:**  
  https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/

- **YC living-company-memory example:**  
  https://youtu.be/X_JsIHUfUjc  
  The speaker describes:
  - recording email, Slack, DMs, and office hours;
  - diarizing and synthesizing recordings;
  - turning approximately 2,000 hours of office hours into a 150-page updated YC user manual;
  - continuously comparing new advice with the existing manual and incorporating or rejecting it.

### Recommended memory architecture

Do not collapse everything into embeddings. Maintain five linked layers:

1. **Immutable evidence:** source documents, recordings, messages, events.
2. **Normalized observations:** diarized utterances, decisions, customer facts.
3. **Canonical knowledge:** current policies, playbooks, entities, skills.
4. **Derived artifacts:** summaries, reports, dashboards, agent context bundles.
5. **Provenance graph:** every claim points back to source spans and transformations.

Preserve disagreement and supersession. A “company brain” that silently overwrites old decisions destroys auditability.

---

## 4. Experimentation cultures

### Sources

- **Microsoft, “Online Experimentation at Microsoft”**  
  https://robotics.stanford.edu/~ronnyk/ExPThinkWeek2009Public.pdf

- **Microsoft Research, “7 Lessons Learned from Enabling A/B Testing as a Product Offering at Scale”**  
  https://www.microsoft.com/en-us/research/wp-content/uploads/2023/05/ICSE2023-Integrating-AB-testing-Offering-at-Scale-Preprint.pdf

- **ExP Platform—trustworthy online controlled experiments:**  
  https://exp-platform.com/

- **Systematic literature review of A/B testing:**  
  https://www.sciencedirect.com/science/article/pii/S0164121224000542

### Cultural requirements

An autonomous experimentation loop needs:

- explicit hypotheses and decision rules before launch,
- randomized assignment where feasible,
- guardrail metrics in addition to the target metric,
- checks for sample-ratio mismatch and instrumentation defects,
- minimum detectable effect/power planning,
- exposure logging and reproducibility,
- a registry of all experiments, including negative results,
- human approval for experiments affecting rights, pricing, employment, safety, or vulnerable users.

The YC “agent identifies funnel friction, researches practices, launches an A/B test, selects a winner, and deploys” vision is viable only with these statistical and governance controls.

---

## 5. Governance, safety, and risks

### Authoritative sources

- **NIST AI Risk Management Framework:**  
  https://www.nist.gov/itl/ai-risk-management-framework  
  PDF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf  
  Organizes risk management around **Govern, Map, Measure, Manage**.

- **NIST Generative AI Profile:**  
  https://doi.org/10.6028/NIST.AI.600-1

- **EU AI Act overview:**  
  https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

- **Binding EU regulation text:**  
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689

### Principal autonomous-company risks

- reward hacking and metric gaming;
- compounding retrieval errors or false organizational memories;
- unauthorized disclosure across customer/team boundaries;
- agents acquiring broader privileges through generated code;
- automated discrimination in employment, credit, or customer treatment;
- irreversible actions without a rollback path;
- feedback loops that train on the system’s own mistakes;
- surveillance and chilling effects from “record everything” policies;
- lack of accountability when multiple agents contribute to a decision;
- prompt injection and poisoned internal content;
- monoculture risk—one incorrect worldview propagating across every function.

### Minimum controls

- least-privilege tools and scoped credentials;
- immutable event and decision logs;
- policy-as-code authorization;
- approval thresholds based on reversibility and harm;
- sandbox/canary deployment;
- rollback and kill switches;
- independent evals not editable by the optimizing agent;
- periodic red-team and privacy review;
- separation between proposer, evaluator, and deployer;
- named human owner for every autonomous loop.

---

## 6. Corpus design, licensing, and evaluation

### Useful corpus-design sources

- **Datasheets for Datasets:**  
  https://cacm.acm.org/research/datasheets-for-datasets/  
  Documents motivation, composition, collection, processing, intended uses, and limitations.

- **Data Statements for NLP guide:**  
  https://techpolicylab.uw.edu/wp-content/uploads/2021/10/Data_Statements_Guide_V2.pdf

- **Large-scale audit of dataset licensing and attribution:**  
  https://www.nature.com/articles/s42256-024-00878-8

- **Common Corpus—open/public-domain approach:**  
  https://arxiv.org/html/2506.01732v3

- **U.S. Copyright Office, Generative AI Training report:**  
  https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf  
  The Office concludes that fair use depends on the work, source, purpose, and output controls; commercial use of unlawfully accessed works to generate competing expressive content may exceed established fair-use boundaries. It recommends allowing licensing markets to develop.

## Proposed corpus schema

```yaml
corpus_item:
  item_id: stable UUID
  tenant_id: organization/customer boundary
  source:
    uri: canonical source locator
    source_system: slack|email|notion|meeting|crm|code|web|manual
    native_id: original platform ID
    author_ids: []
    created_at: timestamp
    ingested_at: timestamp
    content_hash: sha256
    version: source version
  content:
    media_type: text|audio|video|image|code|structured
    raw_object_uri: immutable object location
    normalized_text: text
    language: BCP-47
    segments:
      - segment_id:
        start_time_or_offset:
        end_time_or_offset:
        speaker_or_author:
        text:
  classification:
    domain: sales|product|support|legal|finance|engineering|people
    entity_ids: []
    document_type:
    confidentiality: public|internal|confidential|restricted
    personal_data_categories: []
    sensitivity_tags: []
  provenance:
    acquisition_method:
    transformations: []
    parent_item_ids: []
    extractor_model:
    extractor_version:
    confidence:
    human_verified: boolean
  rights:
    copyright_owner:
    license_id:
    license_url:
    license_text_snapshot:
    permission_basis: owned|contract|open_license|public_domain|consent|fair_use_claim
    permitted_uses: [search, rag, evaluation, fine_tuning, redistribution]
    attribution_required: boolean
    attribution_text:
    commercial_use_allowed: boolean
    derivatives_allowed: boolean
    share_alike: boolean
    territory:
    expiration_at:
    opt_out_status:
    deletion_obligation:
  governance:
    retention_policy:
    legal_hold: boolean
    consent_record_ids: []
    access_policy_id:
    allowed_agent_roles: []
    human_owner:
  knowledge:
    factual_claims: []
    supersedes_item_ids: []
    contradicted_by_item_ids: []
    valid_from:
    valid_until:
  evaluation:
    train_dev_test_split: train|dev|test|holdout|none
    contamination_group_id:
    benchmark_exclusion: boolean
    quality_scores:
      accuracy:
      completeness:
      freshness:
      toxicity:
      pii_risk:
```

### Licensing cautions

- **Availability is not permission.** Public web access does not establish a training, redistribution, or commercial-use license.
- Record rights at the **item/version level**, not only at dataset level.
- Separate permissions for **retrieval**, **fine-tuning**, **evaluation**, and **redistribution**.
- Preserve the exact license text/version and acquisition date; web terms change.
- Do not merge incompatible copyleft/share-alike content into a corpus without legal analysis.
- Respect database rights, contract/ToS restrictions, robots directives where applicable, and technical access controls.
- Internal Slack, email, meetings, and calls raise privacy, employment, wiretap/recording-consent, privilege, and trade-secret issues even when the company owns the systems.
- Create deletion and opt-out propagation so removals reach raw objects, indexes, derived summaries, caches, and future training snapshots.
- Keep licensed/consented material physically and logically separable from fair-use-claimed material.
- Obtain counsel for production training decisions; a metadata field labeled “fair use” is not a legal determination.

## Evaluation design

Maintain distinct suites for:

- retrieval recall and citation precision;
- factual consistency against source spans;
- authorization and tenant-boundary violations;
- stale/superseded knowledge;
- tool-use correctness and reversibility;
- policy compliance;
- long-horizon task success;
- calibration/abstention;
- adversarial prompt injection;
- privacy leakage and memorization;
- business outcome plus harm/guardrail metrics.

Every production failure or human override should be eligible to become a regression eval—but only after deduplication, privacy review, and confirmation that the desired human response was correct.

---

### Work completed

- Identified and transcript-verified the YC/Pedro video and exact relevant timestamps.
- Researched all six lanes using primary institutional, corporate, academic, and regulatory sources.
- Proposed an auditable corpus schema and licensing/evaluation controls.
- **Files modified:** none.
- **Issue:** one seed URL, https://youtu.be/fVut0ceg2IY, currently resolved to a 20-second OpenTable advertisement transcript and appears unrelated, likely a mistaken or changed seed.
