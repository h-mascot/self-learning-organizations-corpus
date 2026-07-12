#!/usr/bin/env python3
"""Run bounded, auditable cross-channel saturation searches.

Search results are discovery evidence, never organization evidence. New URLs are
therefore blocked for manual review; exact canonical-URL matches are rejected as
duplicates. This makes the runner safe to repeat without mutating accepted corpus.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "saturation"
UA = "self-learning-organizations-corpus/0.3 (public research; contact unavailable)"

ROUNDS = {
    "x": [
        ("bounded-doctrine", 'site:x.com ("company AGI" OR "self-improving company")'),
        ("mechanism-language", 'site:x.com ("organizational memory" OR "eval-driven") company AI'),
        ("named-entity-chase", 'site:x.com (Brex OR Ramp OR "Y Combinator") agents feedback evals'),
    ],
    "reddit": [
        ("bounded-doctrine", 'site:reddit.com "AI-native company" operations'),
        ("mechanism-language", 'site:reddit.com ("organizational memory" OR postmortem) company learning'),
        ("named-entity-chase", 'site:reddit.com (Brex OR Ramp OR Klarna) AI agents operations'),
    ],
    "substack": [
        ("bounded-doctrine", 'site:substack.com "self-improving company"'),
        ("mechanism-language", 'site:substack.com organizational memory evals feedback loops company'),
        ("named-entity-chase", 'site:substack.com (Brex OR Ramp OR Every) "AI-native"'),
    ],
    "blogs": [
        ("bounded-doctrine", 'engineering blog "self-improving company" AI'),
        ("mechanism-language", 'engineering blog production evals feedback loop organizational learning'),
        ("named-entity-chase", '(Brex OR Ramp OR Klarna OR Spotify) engineering AI feedback evals'),
    ],
    "podcasts": [
        ("bounded-doctrine", 'podcast transcript "AI-native company" operations'),
        ("mechanism-language", 'podcast transcript organizational learning experimentation feedback loops'),
        ("named-entity-chase", 'podcast transcript (Pedro Franceschi OR Geoff Charles OR Dan Shipper) AI'),
    ],
    "books": [
        ("bounded-doctrine", 'book "self-improving organization"'),
        ("mechanism-language", 'book organizational memory experimentation learning organization'),
        ("citation-chase", 'book (Argyris OR Senge OR Edmondson OR Spear) organizational learning'),
    ],
    "conferences": [
        ("bounded-doctrine", 'conference talk "AI-native company"'),
        ("mechanism-language", 'conference talk eval-driven agents feedback organizational learning'),
        ("named-entity-chase", 'conference talk (Brex OR Ramp OR Spotify OR Toyota) continuous improvement'),
    ],
    "case-studies": [
        ("bounded-doctrine", 'customer case study AI agents operational improvement measured'),
        ("mechanism-language", 'case study organizational learning experimentation feedback measurable outcome'),
        ("named-entity-chase", '(Brex OR Ramp OR Klarna OR Toyota) case study AI continuous improvement'),
    ],
    "github": [
        ("organization-artifacts", "postmortem decision-record"),
        ("mechanism-language", "organizational-memory feedback-loop"),
        ("named-entity-chase", "company agents evals"),
    ],
    "academic": [
        ("bounded-doctrine", '"self-improving organization" artificial intelligence'),
        ("mechanism-language", 'organizational learning memory experimentation feedback evaluation'),
        ("citation-chase", 'Argyris March Senge absorptive capacity organizational learning'),
    ],
    "youtube": [
        ("bounded-doctrine", '"self-improving company" AI'),
        ("mechanism-language", 'organizational memory eval-driven company agents'),
        ("named-entity-chase", 'Pedro Franceschi Geoff Charles Dan Shipper AI company'),
    ],
}


def canonical(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower() or "https", host, path, "", ""))


def accepted_urls() -> set[str]:
    urls: set[str] = set()
    for path in ROOT.glob("sources/**/*"):
        if not path.is_file() or path.name == ".gitkeep" or "accepted" not in path.parts:
            continue
        try:
            if path.suffix == ".json":
                url = json.loads(path.read_text()).get("canonical_url")
            else:
                text = path.read_text(errors="replace")
                url = next((line.split(":", 1)[1].strip() for line in text.splitlines()
                            if line.startswith("canonical_url:")), None)
            if url:
                urls.add(canonical(str(url).strip('"\'')))
        except (OSError, ValueError):
            continue
    return urls


def bing(query: str, limit: int) -> list[dict]:
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query, "format": "rss"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        root = ET.fromstring(response.read())
    return [{"title": (item.findtext("title") or "").strip(),
             "url": (item.findtext("link") or "").strip(),
             "snippet": (item.findtext("description") or "").strip()}
            for item in root.findall("./channel/item")[:limit]]


def github(query: str, limit: int) -> list[dict]:
    run = subprocess.run(
        ["gh", "search", "repos", query, "--limit", str(limit),
         "--json", "fullName,url,description"], check=True, capture_output=True, text=True)
    return [{"title": row["fullName"], "url": row["url"],
             "snippet": row.get("description") or ""} for row in json.loads(run.stdout)]


CHANNEL_HOSTS = {
    "x": {"x.com", "twitter.com"}, "reddit": {"reddit.com"},
    "substack": {"substack.com"}, "github": {"github.com"},
    "youtube": {"youtube.com", "youtu.be"},
}
SIGNALS = ("organiz", "learn", "improv", "feedback", "experiment", "memory",
           "postmortem", "eval", "agent", "adaptive", "brex", "ramp", "klarna",
           "spotify", "toyota", "senge", "argyris", "edmondson", "pedro franceschi")


def discovery_disposition(channel: str, result: dict, url: str, seen: set[str]) -> tuple[str, str, bool]:
    if url in seen:
        return "rejected", "duplicate canonical URL", True
    host = urllib.parse.urlsplit(url).netloc
    if channel in CHANNEL_HOSTS and not any(host == h or host.endswith("." + h) for h in CHANNEL_HOSTS[channel]):
        return "rejected", "search-backend drift: result is outside the requested channel", False
    haystack = f"{result['title']} {result['snippet']}".lower()
    if channel not in {"github"} and not any(signal in haystack for signal in SIGNALS):
        return "rejected", "search-backend drift: title/snippet has no topical signal", False
    return "blocked", "new discovery requires primary-source relevance and organization-evidence review", False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--channels", nargs="*", choices=sorted(ROUNDS), default=sorted(ROUNDS))
    args = parser.parse_args()
    known = accepted_urls()
    seen = set(known)
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidates, rounds = [], []
    OUT.mkdir(parents=True, exist_ok=True)
    for channel in args.channels:
        for number, (family, query) in enumerate(ROUNDS[channel], 1):
            backend = "GitHub CLI/API" if channel == "github" else "Bing public RSS search"
            error = None
            try:
                results = github(query, args.limit) if channel == "github" else bing(query, args.limit)
            except Exception as exc:  # the precise access failure belongs in the ledger
                results, error = [], f"{type(exc).__name__}: {exc}"
            counts = {"accepted": 0, "rejected": 0, "blocked": 0, "duplicates": 0}
            for rank, result in enumerate(results, 1):
                url = canonical(result["url"])
                disposition, reason, duplicate = discovery_disposition(channel, result, url, seen)
                if duplicate:
                    counts["duplicates"] += 1
                if url not in seen:
                    seen.add(url)
                counts[disposition] += 1
                candidates.append({
                    "searched_at": now, "channel": channel, "round": number,
                    "query_family": family, "backend": backend, "query": query,
                    "rank": rank, "title": result["title"], "canonical_url": url,
                    "snippet": result["snippet"], "disposition": disposition,
                    "reason": reason,
                })
            rounds.append({
                "searched_at": now, "channel": channel, "round": number,
                "query_family": family, "backend": backend, "query": query,
                "result_count": len(results), **counts,
                "net_new_accepted_rate": 0.0,
                "status": "blocked" if error else "completed",
                "error": error,
                "saturation_eligible": False,
                "eligibility_note": "New results remain blocked for manual evidence review; zero auto-acceptance is not saturation proof.",
            })
    (OUT / "rounds.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rounds))
    (OUT / "candidates.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in candidates))
    summary = {
        "generated_at": now, "channels": len(args.channels), "rounds": len(rounds),
        "results": len(candidates), "accepted": sum(x["accepted"] for x in rounds),
        "rejected": sum(x["rejected"] for x in rounds),
        "blocked": sum(x["blocked"] for x in rounds),
        "duplicate_results": sum(x["duplicates"] for x in rounds),
        "channels_saturated": [],
        "note": "Three rounds were executed per channel, but no channel is marked saturated until blocked discoveries are reviewed and three eligible rounds remain below 5% net-new accepted unique sources.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
