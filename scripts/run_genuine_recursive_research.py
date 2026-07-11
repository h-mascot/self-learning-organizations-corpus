#!/usr/bin/env python3
"""Build a dependent, evidence-bearing research DAG from OpenAlex relationships.

The old Crossref topic/facet matrix is intentionally not read or overwritten.
Every non-seed loop selects an OpenAlex related work exposed by an earlier loop.
"""

import argparse, datetime as dt, hashlib, html, json, re, time, urllib.parse, urllib.request
from pathlib import Path

SEEDS = [
    "https://doi.org/10.1287/orsc.2.1.71",
    "https://doi.org/10.2307/2393553",
    "https://doi.org/10.1016/j.riob.2017.10.002",
    "https://doi.org/10.1145/3442188.3445922",
    "https://arxiv.org/abs/2210.03629",
]
OUT = Path("research/recursive-loops")
SOURCES = Path("sources/arxiv")
UA = "self-learning-organizations-corpus/0.2 (mailto:corpus@example.invalid)"

def get_json(url, attempts=5):
    error = ""
    for n in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=35) as r:
                return json.load(r), r.status, ""
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.5 * (n + 1))
    return {}, 0, error

def inv_abstract(index):
    if not index: return ""
    words = []
    for word, positions in index.items():
        for pos in positions: words.append((pos, word))
    return " ".join(w for _, w in sorted(words))

def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value or ""))).strip()

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:100] or "source"

def openalex_id(value):
    if value.startswith("https://doi.org/"):
        value = "doi:" + value.removeprefix("https://doi.org/")
    elif value.startswith("https://arxiv.org/abs/"):
        value = "https://arxiv.org/abs/" + value.rsplit("/", 1)[-1]
    elif value.startswith("https://openalex.org/"):
        value = value.rsplit("/", 1)[-1]
    api = "https://api.openalex.org/works/" + urllib.parse.quote(value, safe=":/.") + "?mailto=corpus@example.invalid"
    data, status, error = get_json(api)
    return data, api, status, error

def question(loop_no, title, authors, concepts, parent_title):
    lead = authors[0] if authors else "the authors"
    concept = concepts[0] if concepts else "organizational adaptation"
    stems = [
        f"What mechanism does {lead} identify in “{title}” that deepens the evidence from “{parent_title}”?",
        f"Which measurable boundary in “{title}” changes how {concept} should be evaluated after “{parent_title}”?",
        f"Where does “{title}” support or contradict the causal account advanced by “{parent_title}”?",
        f"What operational artifact in “{title}” could make the {concept} feedback loop auditable?",
        f"How does the evidence in “{title}” constrain claims about transfer from individual to organizational learning?",
    ]
    return stems[(loop_no - 1) % len(stems)]

def source_record(work, loop_no, canonical, excerpt, claims):
    title = clean(work.get("title")) or work.get("id", "Untitled")
    year = work.get("publication_year") or "unknown"
    authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", []) if a.get("author")]
    stable = (work.get("id") or hashlib.sha256(canonical.encode()).hexdigest()[:12]).rsplit("/", 1)[-1].lower()
    path = SOURCES / f"{year}--{slug(title)}--{slug(authors[0] if authors else 'unknown')}--{stable}.md"
    body = f"""---
title: {json.dumps(title, ensure_ascii=False)}
platform: arxiv-academic
canonical_url: {canonical}
openalex_url: {work.get('id','')}
publication_year: {year}
authors: {json.dumps(authors, ensure_ascii=False)}
rights_status: metadata-and-short-evidence-span-only
recursive_loop: {loop_no}
---

# {title}

## Evidence span

> {excerpt}

## Learned claims

""" + "\n".join(f"- {c}" for c in claims) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return str(path)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=200); args = ap.parse_args()
    artifacts = OUT / "artifacts"; artifacts.mkdir(parents=True, exist_ok=True); SOURCES.mkdir(parents=True, exist_ok=True)
    frontier = []
    for seed in SEEDS:
        frontier.append({"selected": seed, "parent_loop": None, "parent_source": "research/discovery-inventory.md", "discovered_as": "validated foundation seed"})
    queued = set(SEEDS); visited = set(); rows = []; children_by_loop = {}
    while frontier and len(rows) < args.limit:
        item = frontier.pop(0); selected = item["selected"]
        work, retrieval, status, error = openalex_id(selected)
        wid = work.get("id")
        if not wid or wid in visited: continue
        visited.add(wid); loop_no = len(rows) + 1
        title = clean(work.get("title"))
        abstract = clean(inv_abstract(work.get("abstract_inverted_index")))
        excerpt = (abstract or title)[:900]
        if len(excerpt) < 25: continue
        authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", []) if a.get("author")]
        concepts = [x.get("display_name", "") for x in work.get("concepts", [])[:4] if x.get("display_name")]
        parent_no = item["parent_loop"]
        parent_title = rows[parent_no - 1]["selected_title"] if parent_no else "the seed inventory"
        canonical = work.get("doi") or (work.get("primary_location") or {}).get("landing_page_url") or wid
        claims = [f"The inspected source addresses {', '.join(concepts[:2]) or 'organizational learning'} through the evidence summarized in the preserved span."]
        if abstract: claims.append(f"The abstract supplies a direct evidence span of {len(abstract.split())} words; interpretation remains bounded to that span.")
        else: claims.append("Only bibliographic primary metadata was available; no full-text inference is made.")
        related = [r for r in work.get("related_works", []) if r not in visited]
        generated = []
        for child in related[:8]:
            if child not in queued:
                queued.add(child); generated.append(child)
        record = source_record(work, loop_no, canonical, excerpt, claims)
        artifact = {
            "schema_version": 2, "loop": loop_no, "parent_loop": parent_no,
            "parent_source": item["parent_source"], "selected_item": selected,
            "selected_title": title, "discovered_as": item["discovered_as"],
            "question": question(loop_no, title, authors, concepts, parent_title),
            "retrieval_url": retrieval, "canonical_url": canonical, "http_status": status,
            "retrieval_error": error, "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "evidence_spans": [{"kind": "abstract-or-title", "text": excerpt}],
            "learned_claims": claims, "contradictions": [], "generated_children": generated,
            "corpus_changes": [record], "selected_openalex_id": wid,
        }
        path = artifacts / f"{loop_no:03d}--{slug(title)}.json"; path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n")
        artifact["artifact"] = str(path.relative_to(OUT)); rows.append(artifact)
        for child in generated:
            frontier.append({"selected": child, "parent_loop": loop_no, "parent_source": canonical, "discovered_as": f"related_works link exposed by loop {loop_no}"})
        if loop_no % 20 == 0: print(f"checkpoint {loop_no}: frontier={len(frontier)} unique={len(visited)}", flush=True)
    ledger = OUT / "ledger.jsonl"; ledger.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    summary = {"schema_version": 2, "requested_loops": args.limit, "productive_loops": len(rows), "seed_loops": sum(r["parent_loop"] is None for r in rows), "edges": sum(r["parent_loop"] is not None for r in rows), "unique_sources": len({r["canonical_url"] for r in rows})}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if len(rows) != args.limit: raise SystemExit(f"only built {len(rows)} loops")

if __name__ == "__main__": main()
