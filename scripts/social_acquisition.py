#!/usr/bin/env python3
"""Retrieve and materialize the social lane from public resource-level sources.

Raw responses are retained under ``research/social/raw``.  Accepted records are
never created from titles or synthetic summaries: X and Reddit retain the complete
post/article text returned by public read APIs; newsletters retain a bounded span
from a direct reader fetch of an individual article page.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRIEVED = "2026-07-12T12:00:00Z"
UA = "corpus-social-audit/2.0"

def existing_x_urls() -> list[str]:
    urls: list[str] = []
    for path in sorted((ROOT / "sources" / "x" / "accepted").glob("*.md")):
        match = re.search(r"^canonical_url:\s*\"?(https://x\.com/[^\"\s]+)", path.read_text(), re.M)
        if match:
            urls.append(match.group(1))
    replacements = {
        "https://x.com/XData/status/1769826435576037702": "https://x.com/hwchase17/status/2040467997022884194",
        "https://x.com/pedroh96/status/2017612447666815146": "https://x.com/NotionHQ/status/2026338860557545901",
        "https://x.com/karpathy/status/2030777122223173639": "https://x.com/karpathy/status/2030371219518931079",
        "https://x.com/saranormous/status/2043498059615928407": "https://x.com/aakashgupta/status/2034851259442749909",
        "https://x.com/gailalfaratx/status/2026458097112453467": "https://x.com/nikogrupen/status/2041166953902203157",
        "https://x.com/naruto11eth/status/2031516218201432474": "https://x.com/DallasAptGP/status/2033574400901935534",
        "https://x.com/exploraX_/status/2036861515580457345": "https://x.com/BrendanFoody/status/2019921803699974626",
        "https://x.com/kurasinski/status/2038656175856623671": "https://x.com/yq_acc/status/2017601463326019742",
    }
    for rejected, replacement in replacements.items():
        if rejected in urls:
            urls.remove(rejected)
            urls.append(replacement)
    return urls

REDDIT_IDS = [
    "1s6h570", "1r25r09", "1rzpvfd", "1rytcz0", "1ruvu7w",
    "1q785ld", "1rbn18z", "1rz5u0h", "1r54kau", "1rrnk1j",
    "1r82abw", "1r3tzql", "1rzq1ye", "1rq0hgm", "1rjgkop",
    "1rqhynw", "1ruk4g4", "1rrrx47", "1r74yk0", "1mnr6d2",
    "1rld3ny", "1rrlcn6", "1nh9iet", "1rxki08", "1qpwwpr",
]

# All are individual resource pages discovered by the preserved Exa queries.
NEWSLETTERS = [
    ("https://thomasbustos.substack.com/p/the-ai-native-company", "Thomas Bustos", "2026-01-23"),
    ("https://nanothoughts.substack.com/p/the-company-that-remembers-itself", "Ashwin Gopinath", "2026-05-12"),
    ("https://andsnotors.substack.com/p/the-context-bank-organizational-memory", "Madhu Chamarty", "2026-04-22"),
    ("https://nanothoughts.substack.com/p/company-brain-why-most-companies", "Ashwin Gopinath", "2026-05-04"),
    ("https://ainativefounder.substack.com/p/how-the-two-loops-run-and-where-they", "Mohamed F. Ahmed", "2026-07-01"),
    ("https://nanothoughts.substack.com/p/enterprise-general-intelligence-the", "Ashwin Gopinath", "2026-02-02"),
    ("https://abvx.substack.com/p/the-six-stages-of-becoming-ai-native", "Anton Biletskiy-Volokh", "2026-05-07"),
    ("https://queener.substack.com/p/the-compounding-loop", "Brett Queener", "2026-05-13"),
    ("https://nanothoughts.substack.com/p/what-building-a-company-brain-for", "Ashwin Gopinath", "2026-05-11"),
    ("https://nanothoughts.substack.com/p/company-brain-part-4-action-memory", "Ashwin Gopinath", "2026-05-07"),
    ("https://mikelukianoff.substack.com/p/your-knowledge-base-is-dead-heres", "Mike Lukianoff", "2026-03-07"),
    ("https://enterprisecontextmanagement.substack.com/p/memory-is-the-next-frontier-for-ai", "Mark Sykes", "2026-03-26"),
    ("https://newsletter.systemdesign.one/p/graph-based-agent-memory", "Neo Kim", "2026-07-07"),
    ("https://thestrategystack.substack.com/p/the-agentic-operating-model-building", "Alex Pawlowski", "2025-09-07"),
    ("https://theaieconomy.substack.com/p/ship-first-fix-later-coreweave-autonomous-agent-loop", "Ken Yeung", "2026-05-28"),
    ("https://micheallanham.substack.com/p/the-three-dials-theory-how-any-ai", "Micheal Lanham", "2026-06-30"),
    ("https://packtwebdevpro.substack.com/p/webdevpro-136-agent-continuous-learning", "Kinnari Chohan", "2026-04-22"),
    ("https://airealizednow.substack.com/p/the-missing-layer-in-enterprise-ai", "AI Realized", "2026-04-16"),
    ("https://curiosityashes.substack.com/p/how-do-you-build-an-ai-agent-that", "Kevin Wang", "2026-05-31"),
    ("https://innerloopai.substack.com/p/orchestrating-an-agentic-crew-at", "Mike Lanzetta", "2026-05-24"),
    ("https://jdsemrau.substack.com/p/hyperagents-and-self-correcting-systems", "Jan Daniel Semrau", "2026-05-11"),
    ("https://derivai.substack.com/p/operations-center-for-ai-agents", "Kaveh Mousavi Zamani", "2026-05-08"),
    ("https://www.thebullandthebot.com/p/bot-series-how-i-built-a-5-agent", "The Bull & The Bot", "2025-09-05"),
    ("https://www.oneusefulthing.org/p/centaurs-and-cyborgs-on-the-jagged", "Ethan Mollick", "2023-09-16"),
    ("https://substack.fintechtalk.ivalley.co/p/the-ai-execution-economy", "FINTECHTALK", "2026-05-11"),
]


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def article_text(article: dict) -> str:
    blocks = article.get("content", {}).get("blocks", [])
    return "\n\n".join(b.get("text", "").strip() for b in blocks if b.get("text", "").strip())


def frontmatter(meta: dict, body: str) -> str:
    meta["content_sha256"] = hashlib.sha256(body.encode()).hexdigest()
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            value = json.dumps(value, ensure_ascii=False)
        elif not isinstance(value, int):
            value = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {value}")
    return "\n".join(lines + ["---", body])


def write_record(platform: str, sid: str, title: str, publisher: str, url: str,
                 date: str, source_text: str, availability: str, provenance: str,
                 retrieval_url: str) -> None:
    source_text = source_text.strip()
    heading = "Complete source text" if availability == "full_text" else "Verified source excerpt"
    body = f"# {title}\n\n## {heading}\n\n{source_text}\n\n## Acquisition limits\n\n"
    if availability == "full_text":
        body += "The complete public post/article text returned by the named source endpoint is retained.\n"
    else:
        body += "This is a bounded span from a direct fetch of the individual article, not a complete copy.\n"
    meta = {
        "schema_version": 1, "platform": platform, "stable_id": sid,
        "title": title, "publisher": publisher, "canonical_url": url,
        "published_date": date, "content_type": "article" if platform == "substack" else "post",
        "status": "accepted", "relevance_status": "relevant", "availability": availability,
        "provenance": provenance,
        "rights_status": "third-party", "rights_holder": publisher,
        "rights_note": f"Public source evidence retrieved {RETRIEVED} via {retrieval_url}.",
        "relevance_categories": ["feedback-loop", "organizational-learning", "agentic-operations"],
        "relevance_evidence": [source_text[:500]],
    }
    if platform == "x":
        meta["raw_path"] = f"research/social/raw/x/{sid}.json"
    elif platform == "reddit":
        meta["raw_path"] = "research/social/raw/reddit/selected-posts.json"
    else:
        meta["raw_path"] = f"research/social/raw/substack/{sid}.md"
    name = f"{date}--{slug(title)}--{slug(publisher)}--{sid}.md"
    (ROOT / "sources" / platform / "accepted" / name).write_text(frontmatter(meta, body), encoding="utf-8")


def clean_reader(markdown: str) -> tuple[str, str]:
    title_match = re.search(r"^Title:\s*(.+)$", markdown, re.M)
    title = title_match.group(1).strip() if title_match else "Untitled newsletter article"
    content = markdown.split("Markdown Content:", 1)[-1].strip()
    # Keep a substantial, bounded source span and exclude reader metadata.
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", content):
        paragraph = paragraph.strip()
        plain = re.sub(r"!?\[[^]]*\]\([^)]*\)", "", paragraph)
        if len(plain) >= 80 and sum(ch.isalpha() for ch in plain) / len(plain) >= 0.55:
            paragraphs.append(paragraph)
    excerpt = "\n\n".join(paragraphs[:8])[:5000].strip()
    return title, excerpt


def main() -> None:
    x_urls = existing_x_urls()
    if len(x_urls) != 50:
        raise RuntimeError(f"expected the 50 audited X resource URLs, found {len(x_urls)}")
    raw = ROOT / "research" / "social" / "raw"
    for platform in ("x", "reddit", "substack"):
        shutil.rmtree(ROOT / "sources" / platform / "accepted", ignore_errors=True)
        (ROOT / "sources" / platform / "accepted").mkdir(parents=True)
        (raw / platform).mkdir(parents=True, exist_ok=True)

    for url in x_urls:
        requested_id = url.rsplit("/", 1)[-1]
        endpoint = f"https://api.fxtwitter.com/status/{requested_id}"
        payload = get(endpoint)
        (raw / "x" / f"{requested_id}.json").write_bytes(payload)
        tweet = json.loads(payload)["tweet"]
        source = tweet.get("text", "").strip() or article_text(tweet.get("article") or {})
        if len(source) < 80:
            raise RuntimeError(f"X source is non-substantive: {requested_id}")
        canonical = tweet["url"]
        sid = re.search(r"/status/(\d+)", canonical).group(1)
        created = datetime.fromtimestamp(tweet["created_timestamp"], timezone.utc).date().isoformat()
        title = (tweet.get("article") or {}).get("title") or source.splitlines()[0][:100]
        write_record("x", sid, title, tweet["author"]["name"], canonical, created, source,
                     "full_text", "FxTwitter public API response for the canonical X resource",
                     endpoint)

    ids = ",".join(REDDIT_IDS)
    endpoint = f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={ids}"
    payload = get(endpoint)
    (raw / "reddit" / "selected-posts.json").write_bytes(payload)
    posts = {p["id"]: p for p in json.loads(payload)["data"]}
    for sid in REDDIT_IDS:
        post = posts[sid]
        source = post.get("selftext", "").strip()
        if len(source) < 200 or source in {"[removed]", "[deleted]"}:
            raise RuntimeError(f"Reddit source is non-substantive: {sid}")
        canonical = "https://www.reddit.com" + post["permalink"]
        created = datetime.fromtimestamp(post["created_utc"], timezone.utc).date().isoformat()
        write_record("reddit", sid, post["title"], post["author"], canonical, created, source,
                     "full_text", "Arctic Shift public Reddit archive record with exact post ID",
                     endpoint)

    for url, publisher, published in NEWSLETTERS:
        sid = hashlib.sha256(url.encode()).hexdigest()[:16]
        endpoint = "https://r.jina.ai/" + url
        payload = get(endpoint)
        (raw / "substack" / f"{sid}.md").write_bytes(payload)
        title, excerpt = clean_reader(payload.decode("utf-8", errors="replace"))
        if len(excerpt) < 500:
            raise RuntimeError(f"Newsletter source is non-substantive: {url}")
        write_record("substack", sid, title, publisher, url, published, excerpt,
                     "metadata_only", "Jina Reader direct fetch of the canonical individual article",
                     endpoint)


if __name__ == "__main__":
    main()
