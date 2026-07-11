#!/usr/bin/env python3
import json, sys
from pathlib import Path

root = Path("research/recursive-loops"); errors = []
rows = [json.loads(line) for line in (root / "ledger.jsonl").read_text().splitlines() if line.strip()]
seen_ids = set(); seen_urls = set(); questions = set(); seeds = 0; edges = 0
for expected, row in enumerate(rows, 1):
    n = row.get("loop"); parent = row.get("parent_loop")
    if n != expected: errors.append(f"loop sequence mismatch at {expected}: {n}")
    if parent is None: seeds += 1
    elif not isinstance(parent, int) or parent >= n: errors.append(f"loop {n}: parent does not precede child")
    else:
        edges += 1; p = rows[parent - 1]
        if row.get("selected_item") not in p.get("generated_children", []): errors.append(f"loop {n}: selected item absent from parent {parent} children")
    if not row.get("parent_source"): errors.append(f"loop {n}: missing parent source")
    if not row.get("question") or row["question"] in questions: errors.append(f"loop {n}: empty/duplicate question")
    questions.add(row.get("question"))
    spans = row.get("evidence_spans", [])
    if not spans or not all(s.get("text", "").strip() for s in spans): errors.append(f"loop {n}: empty evidence")
    if not row.get("learned_claims") or not all(x.strip() for x in row["learned_claims"]): errors.append(f"loop {n}: empty findings")
    if row.get("http_status") != 200 and not row.get("retrieval_error"): errors.append(f"loop {n}: unresolved URL lacks preserved retrieval evidence")
    url = row.get("canonical_url"); wid = row.get("selected_openalex_id")
    if not url: errors.append(f"loop {n}: missing canonical URL")
    if url in seen_urls: errors.append(f"loop {n}: duplicate canonical URL")
    if wid in seen_ids: errors.append(f"loop {n}: duplicate selected work")
    seen_urls.add(url); seen_ids.add(wid)
    for change in row.get("corpus_changes", []):
        p = Path(change)
        if not p.exists() or f"recursive_loop: {n}" not in p.read_text(): errors.append(f"loop {n}: corpus change missing/unlinked: {change}")
result = {"loops": len(rows), "seeds": seeds, "edges": edges, "unique_sources": len(seen_urls), "unique_questions": len(questions), "errors": errors}
print(json.dumps(result, indent=2)); sys.exit(bool(errors or len(rows) != 200))
