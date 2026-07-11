#!/usr/bin/env python3
"""Execute evidence-backed recursive discovery loops against Crossref.

Each completed loop writes an individual artifact and a ledger row. A loop is
counted only when the API returns at least one work with a stable identifier.
"""

import argparse
import concurrent.futures
import csv
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

TOPICS = [
    "organizational learning", "learning organization", "continuous improvement",
    "lean kaizen", "organizational cybernetics", "adaptive enterprise",
    "AI native company", "autonomous enterprise", "organizational memory",
    "agentic organization", "recursive improvement", "continual learning agents",
    "automated experimentation", "self optimizing product", "agent monitoring repair",
    "eval driven development", "data flywheel", "decision intelligence",
    "organizational digital twin", "knowledge creating company",
]
FACETS = [
    "implementation", "case study", "empirical evidence", "governance", "failure",
    "measurement", "feedback loop", "human oversight", "production deployment", "evaluation",
]

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:90]

def fetch(item):
    number, topic, facet = item
    query = f'"{topic}" {facet}'
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": query, "rows": 3, "select": "DOI,title,published,URL,type"
    })
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    error = ""
    for attempt in range(4):
        try:
            time.sleep(0.15)
            req = urllib.request.Request(url, headers={"User-Agent": "self-learning-organizations-corpus/0.1 (mailto:corpus@example.invalid)"})
            with urllib.request.urlopen(req, timeout=30) as response:
                payload = json.load(response)
                status = response.status
            works = payload.get("message", {}).get("items", [])
            works = [w for w in works if w.get("DOI") or w.get("URL")]
            outcome = "productive" if works else "empty"
            break
        except Exception as exc:
            status, works, outcome, error = 0, [], "failed", f"{type(exc).__name__}: {exc}"
            time.sleep(0.5 * (attempt + 1))
    return {"loop": number, "topic": topic, "facet": facet, "query": query, "url": url,
            "started_at": started, "completed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "http_status": status, "outcome": outcome, "error": error, "works": works}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--output", default="research/loops")
    args = parser.parse_args()
    out = Path(args.output)
    artifacts = out / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    jobs = [(i + 1, topic, facet) for i, (topic, facet) in enumerate((t, f) for t in TOPICS for f in FACETS)][:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = sorted(pool.map(fetch, jobs), key=lambda x: x["loop"])
    for result in results:
        path = artifacts / f'{result["loop"]:03d}--{slug(result["topic"])}--{slug(result["facet"])}.json'
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with (out / "ledger.csv").open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["loop", "topic", "facet", "query", "started_at", "completed_at", "provider", "http_status", "outcome", "evidence_count", "artifact"])
        for r in results:
            writer.writerow([r["loop"], r["topic"], r["facet"], r["query"], r["started_at"], r["completed_at"], "Crossref REST API", r["http_status"], r["outcome"], len(r["works"]), f'artifacts/{r["loop"]:03d}--{slug(r["topic"])}--{slug(r["facet"])}.json'])
    summary = {
        "schema_version": 1, "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "requested_loops": len(jobs), "productive_loops": sum(r["outcome"] == "productive" for r in results),
        "empty_loops": sum(r["outcome"] == "empty" for r in results),
        "failed_loops": sum(r["outcome"] == "failed" for r in results),
        "evidence_records": sum(len(r["works"]) for r in results),
        "definition": "A productive loop returned at least one stable Crossref DOI/URL record for a unique taxonomy/facet query.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
