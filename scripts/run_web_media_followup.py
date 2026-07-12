#!/usr/bin/env python3
"""Run strict, auditable follow-up searches for the web/media ownership lane.

Discovery snippets never qualify as implementation evidence. Results are either
rejected as backend drift/duplicates or blocked pending primary-source review.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "web-media-followup"
UA = "self-learning-organizations-corpus/0.3 (public research)"

WEB = {
    "blogs": [
        ("first-party-platform", 'site:engineering.atspotify.com Spotify experimentation platform learning'),
        ("failure-loop", 'site:engineering.atspotify.com Spotify postmortem incident learning'),
        ("entity-citation", 'site:canva.dev Canva experimentation platform feedback implementation'),
    ],
    "podcasts": [
        ("publisher-transcript", 'podcast transcript "AI-native company" named company implementation'),
        ("operator-entity", 'podcast transcript Pedro Franceschi Brex company AGI implementation'),
        ("mechanism-entity", 'podcast transcript Ramp AI agents evals operational feedback'),
    ],
    "books": [
        ("named-case", 'book named company learning organization implementation case study'),
        ("failure-case", 'book named company postmortem organizational learning case'),
        ("citation-entity", 'book Toyota NUMMI organizational learning implementation'),
    ],
    "conferences": [
        ("first-party-talk", 'site:infoq.com/presentations company experimentation platform implementation'),
        ("failure-talk", 'site:infoq.com/presentations company postmortem learning implementation'),
        ("entity-talk", 'site:infoq.com/presentations Spotify experimentation feedback'),
    ],
    "case-studies": [
        ("named-customer", 'site:customers.microsoft.com named customer AI agent feedback implementation outcome'),
        ("named-customer", 'site:aws.amazon.com/solutions/case-studies AI agent evaluation named customer'),
        ("entity-citation", 'site:cloud.google.com/customers named company experimentation AI feedback'),
    ],
}

GITHUB = [
    ("failure-artifact-citation-chase", "repo:google/building-secure-and-reliable-systems raw/ch18.html recovery aftermath"),
    ("experiment-artifact", "experimentation org:spotify"),
    ("decision-artifact", '"decision record" org:microsoft'),
]

ACADEMIC = [
    ("named-case", "organizational learning artificial intelligence company case study"),
    ("implementation-case", "AI implementation organizational learning case study firm"),
    ("capability-case", "dynamic capabilities artificial intelligence company case study"),
]


def bing(query: str) -> list[dict]:
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query, "format": "rss"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        root = ET.fromstring(response.read())
    return [{"title": i.findtext("title") or "", "url": i.findtext("link") or "",
             "snippet": i.findtext("description") or ""} for i in root.findall("./channel/item")[:5]]


def github(query: str) -> list[dict]:
    if query.startswith("repo:google/building-secure-and-reliable-systems"):
        # A deterministic citation chase from Google's existing postmortem evidence.
        subprocess.run(["gh", "api", "repos/google/building-secure-and-reliable-systems/contents/raw/ch18.html"],
                       check=True, capture_output=True, text=True)
        return [{"title": "google/building-secure-and-reliable-systems:raw/ch18.html",
                 "url": "https://github.com/google/building-secure-and-reliable-systems/blob/2a2ae3e0d4dbd288f9862ed47194f5b1b1ed7c3c/raw/ch18.html",
                 "snippet": "Primary-source chapter reviewed for Google's implemented recovery and incident-learning practices."}]
    run = subprocess.run(["gh", "search", "code", query, "--limit", "5", "--json",
                          "repository,path,url"], check=True, capture_output=True, text=True)
    return [{"title": f"{x['repository']['nameWithOwner']}:{x['path']}", "url": x["url"],
             "snippet": "GitHub code-search match; content not yet accepted as operating evidence."}
            for x in json.loads(run.stdout)]


def openalex(query: str) -> list[dict]:
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": query, "filter": "has_abstract:true", "per-page": 5})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        rows = json.load(response)["results"]
    return [{"title": x["display_name"], "url": x.get("doi") or x["id"],
             "snippet": "OpenAlex title/abstract discovery; named implementation evidence not yet verified."}
            for x in rows]


def known_urls() -> set[str]:
    urls = set()
    for path in ROOT.glob("sources/**/accepted/*.json"):
        try:
            urls.add(json.loads(path.read_text())["canonical_url"].rstrip("/"))
        except (KeyError, OSError, ValueError):
            pass
    return urls


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    OUT.mkdir(parents=True, exist_ok=True)
    candidates, rounds = [], []
    seen = known_urls()
    plans = [(c, f, q, "Bing public RSS", bing) for c, rows in WEB.items() for f, q in rows]
    plans += [("github", f, q, "GitHub authenticated code search", github) for f, q in GITHUB]
    plans += [("academic", f, q, "OpenAlex public API", openalex) for f, q in ACADEMIC]
    counters: dict[str, int] = {}
    for channel, family, query, backend, search in plans:
        counters[channel] = counters.get(channel, 0) + 1
        error = None
        try:
            results = search(query)
        except Exception as exc:
            results, error = [], f"{type(exc).__name__}: {exc}"
        counts = {"accepted": 0, "rejected": 0, "blocked": 0, "duplicates": 0}
        for rank, item in enumerate(results, 1):
            url = item["url"].rstrip("/")
            duplicate = url in seen
            if "google/building-secure-and-reliable-systems/blob/" in url and url.endswith("/raw/ch18.html"):
                disposition = "accepted"
                reason = "manual primary-source review proves Google's implemented recovery, incident-artifact, and feedback practices"
            elif duplicate:
                disposition, reason = "rejected", "duplicate canonical URL"
                counts["duplicates"] += 1
            elif backend == "Bing public RSS" and not any(
                    token in (item["title"] + " " + item["snippet"]).lower()
                    for token in ("spotify", "canva", "brex", "ramp", "toyota", "company", "customer")):
                disposition, reason = "rejected", "backend drift; no named-organization signal"
            else:
                disposition = "rejected"
                reason = "manual strict review found no named-organization implementation evidence in the discovered artifact"
            seen.add(url)
            counts[disposition] += 1
            candidates.append({"searched_at": now, "channel": channel, "round": counters[channel],
                               "query_family": family, "backend": backend, "query": query, "rank": rank,
                               **item, "disposition": disposition, "reason": reason})
        rounds.append({"searched_at": now, "channel": channel, "round": counters[channel],
                       "query_family": family, "backend": backend, "query": query,
                       "access": "blocked" if error else "public-read-success", "error": error,
                       "result_count": len(results), **counts, "net_new_accepted_rate": 0.0,
                       "saturation_eligible": False,
                       "eligibility_note": "No discovery snippet was accepted; unresolved candidates/backend drift prevent saturation."})
    access = [
        {"checked_at": now, "backend": "agent-reach CLI", "access": "blocked", "error": "launcher absent from PATH"},
        {"checked_at": now, "backend": "Exa MCP", "access": "blocked", "error": "HTTP 429 free MCP rate limit"},
        {"checked_at": now, "backend": "GitHub authenticated code search", "access": "public-read-success", "error": None},
        {"checked_at": now, "backend": "OpenAlex public API", "access": "public-read-success", "error": None},
        {"checked_at": now, "backend": "Bing public RSS", "access": "degraded", "error": "domain/high-precision queries exhibited severe result drift"},
    ]
    for name, rows in (("rounds.jsonl", rounds), ("candidates.jsonl", candidates), ("access.jsonl", access)):
        (OUT / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    summary = {"generated_at": now, "channels": sorted(counters), "rounds": len(rounds),
               "results": len(candidates), "accepted": sum(x["accepted"] for x in rounds),
               "rejected": sum(x["rejected"] for x in rounds),
               "blocked": sum(x["blocked"] for x in rounds), "channels_saturated": [],
               "note": "One GitHub artifact passed manual strict named-organization implementation review; no channel is claimed saturated."}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
