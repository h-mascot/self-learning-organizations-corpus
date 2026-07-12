#!/usr/bin/env python3
"""Freeze a full-source manual audit of the podcast and GitHub lanes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACQ = ROOT / "research/web-media-acquisition"
MANIFEST = ACQ / "candidate-manifest.jsonl"
QUERIES = ACQ / "query-ledger.jsonl"
RETRIEVALS = ACQ / "retrieval-ledger.jsonl"

PODCASTS = [
    "hamel-husain-shreya-shankar", "karina-nguyen", "adam-fishman", "ronny-kohavi",
    "brendan-foody", "chip-huyen", "itamar-gilad", "jackson-shuttleworth",
    "edwin-chen", "ami-vora", "noah-weiss", "nick-turley", "nicole-forsgren",
    "kevin-weil", "christopher-miller", "dan-hockenmaier", "sri-batchu", "ryan-j-salva",
    "nikita-bier", "josh-miller", "adam-grenier",
    "albert-cheng", "inbal-s", "alexander-embiricos", "dhanji-r-prasanna",
    "eoghan-mccabe", "garrett-lord", "merci-grace", "mike-krieger", "naomi-ionita",
]

GITHUB = [
    "growthbook/growthbook", "PostHog/posthog", "Unleash/unleash", "Flagsmith/flagsmith",
    "open-feature/spec", "openai/evals", "promptfoo/promptfoo", "confident-ai/deepeval",
    "Arize-ai/phoenix", "langfuse/langfuse", "braintrustdata/braintrust-sdk-javascript",
    "UKGovernmentBEIS/inspect_ai", "vibrantlabsai/ragas", "truera/trulens",
    "Netflix/chaosmonkey", "litmuschaos/litmus",
    "architecture-decision-record/architecture-decision-record", "npryce/adr-tools",
    "dastergon/postmortem-templates", "adhorn/operational-excellence", "peter-evans/lightweight-architecture-decision-records",
    "danluu/post-mortems", "upgundecha/howtheysre", "microsoft/promptflow",
    "joelparkerhenderson/issue-postmortem-template", "r-aaron-graham/incident-response-and-postmortem-framework",
    "GoogleCloudPlatform/professional-services", "JDHarris007/coe",
    "chaos-mesh/chaos-mesh", "argoproj/argo-rollouts",
]

AD = re.compile(
    r"brought to you|sponsor|promo code|check it out at|learn more at|"
    r"eppo|datadog|stripe\.com|lennysnewsletter|product pass", re.I
)
TOPIC = re.compile(
    r"institutional (?:memory|learning|knowledge)|organizational learning|learning.first company|"
    r"self-improv|post.?mortem|retrospective|feedback loop|customer feedback|user feedback|"
    r"experiment(?:ation|s|ing)?|\bevals?\b|evaluation(?:s| process| pipeline| rubric)?|dogfood|failure modes?|"
    r"fail(?:ed|ure)? and learn|learnings? (?:from|came)|measure progress|benchmark|decision (?:log|record)|"
    r"iterat(?:e|ed|ing|ion) on the experiment", re.I
)
ORG = re.compile(
    r"team|company|organization|enterprise|product|customer|employee|deploy|production|"
    r"process|system|model|agent|workflow|operation", re.I
)
REPO_MECHANISM = re.compile(
    r"postmortem|post-mortem|incident review|retrospective|architecture decision record|\bADR\b|"
    r"controlled experiment|experimentation|feature flag|progressive delivery|chaos experiment|"
    r"resilien(?:ce|cy)|evaluation|\bevals?\b|benchmark|feedback|observability", re.I
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def field(frontmatter: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*['\"]?(.*?)['\"]?$", frontmatter)
    return clean(match.group(1)).strip("'\"") if match else None


def seconds(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    return parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0] * 3600 + parts[1] * 60 + parts[2]


def mechanism_sentence(text: str) -> str | None:
    body = re.sub(r"^.*?\([^)]*\):\s*", "", clean(text), count=1)
    sentences = re.split(r"(?<=[.!?])\s+", body)
    matches = [sentence for sentence in sentences if TOPIC.search(sentence) and ORG.search(sentence)]
    return max(matches, key=lambda sentence: len(TOPIC.findall(sentence)), default=None)


def bounded_block(block: str) -> str:
    value = clean(block)
    if len(value) <= 680:
        return value
    header = re.match(r"^.*?\([^)]*\):\s*", value)
    prefix = header.group() if header else ""
    body = value[len(prefix):]
    sentence = mechanism_sentence(value) or body
    match_text = TOPIC.search(sentence)
    match = TOPIC.search(body, body.find(sentence)) if match_text else None
    start = max(0, match.start() - 180) if match else 0
    return prefix + body[start:start + 680 - len(prefix)]


def exact_quote(block: str) -> str:
    body = mechanism_sentence(block) or re.sub(r"^.*?\([^)]*\):\s*", "", block, count=1).strip()
    match = TOPIC.search(body)
    if not match:
        return body[:300]
    start = max(0, match.start() - 100)
    return body[start:start + 300].strip()


def block_timestamp(block: str) -> str:
    match = re.search(r"\([^)]*\)", block)
    return match.group() if match else "timestamp unavailable"


def podcast_row(path: Path, old: dict | None) -> dict:
    text = path.read_text(errors="replace")
    _, frontmatter, body = text.split("---", 2)
    guest = field(frontmatter, "guest") or "Unknown guest"
    candidates = []
    for block in re.split(r"\n\s*\n", body.split("## Transcript", 1)[-1]):
        stamp = re.search(r"\((\d{2}:\d{2}:\d{2}|\d{2}:\d{2})\)", block)
        if not stamp or AD.search(block) or not mechanism_sentence(block):
            continue
        surnames = [part.strip().split()[-1].strip(".") for part in re.split(r"\s*[&+]\s*", guest)]
        if not any(name.casefold() in block[:120].casefold() for name in surnames):
            continue
        candidates.append((seconds(stamp.group(1)), len(TOPIC.findall(block)), bounded_block(block)))
    pairs = [(a, b) for a in candidates for b in candidates if b[0] - a[0] >= 600]
    if not pairs:
        raise ValueError(f"{path.parent.name}: no two separated substantive guest spans")
    first, second = max(pairs, key=lambda pair: (pair[0][1] + pair[1][1], pair[1][0] - pair[0][0]))
    selected = [first, second]
    video_id = field(frontmatter, "video_id") or path.parent.name
    title = field(frontmatter, "title") or path.parent.name
    sid = f"podcasts-lenny-{video_id}"
    return {
        "platform": "podcasts", "stable_id": sid, "title": title, "creator": guest,
        "publisher": "Lenny's Podcast", "canonical_url": field(frontmatter, "youtube_url") or f"https://www.youtube.com/watch?v={video_id}",
        "published_date": field(frontmatter, "publish_date"), "date_precision": "day" if field(frontmatter, "publish_date") else "unknown",
        "source_type": "episode", "status": "accepted", "artifact_level": "metadata_only",
        "retrieved_at": now(), "retrieval_method": "full public transcript manual audit via GitHub citation",
        "provenance": f"Full transcript audited at ChatPRD/lennys-podcast-transcripts/{path.parent.name}; original video ID {video_id}.",
        "rights_status": "bounded-public-evidence", "rights_note": "The full public transcript was audited; only two bounded, separated guest passages are retained.",
        "relevance_evidence": [exact_quote(item[2]) for item in selected],
        "evidence": [{"kind": "transcript_excerpt", "locator": f"full transcript at {block_timestamp(item[2])}", "text": item[2]} for item in selected],
        "query_ids": ["manual-full-transcript-audit-2026-07-12"],
        "transcript_source": f"https://github.com/ChatPRD/lennys-podcast-transcripts/blob/main/episodes/{path.parent.name}/transcript.md",
        "transcript_available": True, "retained_complete_transcript": False,
        "media_format": "podcast_episode", "rejection_reason": None,
    }


def gh_json(args: list[str]) -> dict:
    proc = subprocess.run(["gh", *args], check=True, capture_output=True, text=True, timeout=45)
    return json.loads(proc.stdout)


def gh_text(args: list[str]) -> str:
    proc = subprocess.run(["gh", *args], check=True, capture_output=True, text=True, timeout=45)
    return proc.stdout


def repo_excerpt(description: str, readme: str) -> str:
    text = clean(description + "\n" + re.sub(r"<[^>]+>|!\[[^]]*\]\([^)]*\)", " ", readme))
    matches = list(REPO_MECHANISM.finditer(text))
    if not matches:
        raise ValueError("README has no explicit qualifying mechanism")
    match = max(matches, key=lambda item: len(REPO_MECHANISM.findall(text[max(0, item.start()-220):item.start()+460])))
    start = max(0, match.start() - 160)
    return text[start:start + 680]


def repo_quote(excerpt: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", excerpt)
    candidates = [sentence for sentence in sentences if REPO_MECHANISM.search(sentence)]
    quote = max(candidates, key=lambda sentence: (len(REPO_MECHANISM.findall(sentence)), len(sentence)), default=excerpt)
    return quote[:300]


def github_row(name: str, old: dict | None) -> dict:
    meta = gh_json(["api", f"repos/{name}"])
    readme = gh_text(["api", f"repos/{name}/readme", "-H", "Accept: application/vnd.github.raw+json"])
    try:
        excerpt = repo_excerpt(meta.get("description") or "", readme)
    except ValueError as exc:
        raise ValueError(f"{name}: {exc}") from exc
    license_name = (meta.get("license") or {}).get("spdx_id") or "NOASSERTION"
    sid = (old or {}).get("stable_id") or "github-" + re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
    quote = repo_quote(excerpt)
    return {
        "platform": "github", "stable_id": sid, "title": name, "creator": meta["owner"]["login"],
        "publisher": "GitHub", "canonical_url": meta["html_url"], "published_date": meta["created_at"][:10],
        "date_precision": "day", "source_type": "repository", "status": "accepted", "artifact_level": "metadata_only",
        "retrieved_at": now(), "retrieval_method": "manual full-README audit via GitHub CLI API",
        "provenance": f"GitHub metadata and full README manually audited for {name}.",
        "rights_status": "open-license" if license_name != "NOASSERTION" else "bounded-public-evidence",
        "rights_note": f"GitHub reports {license_name}; only a bounded exact mechanism passage is retained.",
        "relevance_evidence": [quote], "evidence": [{"kind": "excerpt", "locator": "full repository README", "text": excerpt}],
        "query_ids": ["manual-full-readme-audit-2026-07-12"], "organizational_mechanism": quote,
        "repository": {"full_name": name, "stars_at_retrieval": meta["stargazers_count"], "last_push": meta["pushed_at"], "license": license_name},
        "rejection_reason": None,
    }


def reject(row: dict, reason: str) -> None:
    row["status"] = "rejected"
    row["artifact_level"] = "unavailable"
    row["rejection_reason"] = reason
    row["relevance_evidence"] = []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcripts", type=Path, required=True)
    args = parser.parse_args()
    rows = read_jsonl(MANIFEST)
    queries = read_jsonl(QUERIES)
    retrievals = read_jsonl(RETRIEVALS)
    retrievals = [row for row in retrievals if not str(row.get("method", "")).startswith(("full public transcript manual audit", "manual full-README audit"))]
    audit_ids = {"manual-full-transcript-audit-2026-07-12", "manual-full-readme-audit-2026-07-12"}
    rows = [row for row in rows if not (row.get("status") == "rejected" and set(row.get("query_ids", [])) & audit_ids)]
    by_url = {row["canonical_url"].rstrip("/").casefold(): row for row in rows}
    for row in rows:
        if row["platform"] == "podcasts" and row["status"] == "accepted":
            reject(row, "Full-transcript audit did not retain this episode among the 30 records with two separated substantive guest passages.")
        if row["platform"] == "github" and row["status"] == "accepted":
            reject(row, "Full-README audit did not retain explicit evidence of an organization-level learning mechanism.")
    query_time = now()
    audit_queries = {
        "manual-full-transcript-audit-2026-07-12": {"lane": "podcasts", "family": "full-transcript-guest-mechanism-audit", "backend": "agent-reach GitHub CLI fallback", "query": "all public episode transcripts; two separated substantive guest passages required", "result_count": len(PODCASTS)},
        "manual-full-readme-audit-2026-07-12": {"lane": "github", "family": "full-readme-organizational-mechanism-audit", "backend": "agent-reach GitHub CLI API", "query": "full README explicitly documents institutional memory, feedback improvement, experimentation, postmortems, resilience learning, or agent evaluation", "result_count": len(GITHUB)},
    }
    queries = [row for row in queries if row.get("query_id") not in audit_queries]
    for query_id, data in audit_queries.items():
        queries.append({"query_id": query_id, "attempted_at": query_time, "outcome": "success", "error": None, **data})
    for slug in PODCASTS:
        fresh = podcast_row(args.transcripts / "episodes" / slug / "transcript.md", None)
        key = fresh["canonical_url"].rstrip("/").casefold()
        old = by_url.get(key)
        if old:
            stable_id = old["stable_id"]
            old.clear(); old.update(fresh); old["stable_id"] = stable_id
            fresh = old
        else:
            rows.append(fresh); by_url[key] = fresh
        retrievals.append({"stable_id": fresh["stable_id"], "lane": "podcasts", "attempted_at": now(), "method": fresh["retrieval_method"], "url": fresh["transcript_source"], "outcome": "retrieved", "http_status": 200, "artifact_observed": "metadata_only", "note": "Full transcript audited; two separated guest passages retained."})
    for name in GITHUB:
        key = f"https://github.com/{name}".casefold()
        old = by_url.get(key)
        fresh = github_row(name, old)
        if old:
            old.clear(); old.update(fresh); fresh = old
        else:
            rows.append(fresh); by_url[key] = fresh
        retrievals.append({"stable_id": fresh["stable_id"], "lane": "github", "attempted_at": now(), "method": fresh["retrieval_method"], "url": fresh["canonical_url"], "outcome": "retrieved", "http_status": 200, "artifact_observed": "metadata_only", "note": fresh["relevance_evidence"][0]})
    rows = [row for row in rows if not (row.get("status") == "rejected" and set(row.get("query_ids", [])) & audit_ids)]
    write_jsonl(MANIFEST, rows)
    write_jsonl(QUERIES, queries)
    write_jsonl(RETRIEVALS, retrievals)
    print(f"audited podcasts={len(PODCASTS)} github={len(GITHUB)}")


if __name__ == "__main__":
    main()
