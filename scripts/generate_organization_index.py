#!/usr/bin/env python3
"""Validate annotations and generate the canonical organization index/dashboard."""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.corpus import audit  # noqa: E402

VOCABULARY = ("feedback/evals", "organizational memory", "experimentation", "decision systems", "failure/postmortem learning", "specialized agents", "workflow adaptation", "knowledge curation", "governance", "measurable outcome")

def build(root: Path = ROOT):
    manifest = json.loads((root / "research/organization-evidence.json").read_text())
    records, errors = audit(root)
    by_id = {str(r["stable_id"]): r for r in records}
    if manifest.get("schema_version") != 1: errors.append("organization evidence schema_version must be 1")
    if tuple(manifest.get("mechanism_vocabulary", ())) != VOCABULARY: errors.append("mechanism_vocabulary must contain the exact canonical tags in canonical order")
    seen, indexed, mechanisms, platforms, outcomes = set(), defaultdict(list), Counter(), Counter(), 0
    for entry in manifest.get("evidence", []):
        org, source_id = entry.get("organization"), str(entry.get("source_id", ""))
        if not isinstance(org, str) or not org.strip() or org != org.strip(): errors.append(f"invalid organization name for {source_id}")
        pair = (str(org).casefold(), source_id)
        if pair in seen: errors.append(f"duplicate organization/source link: {org}/{source_id}")
        seen.add(pair); record = by_id.get(source_id)
        if not record: errors.append(f"organization evidence references missing source: {source_id}"); continue
        if record.get("lifecycle") != "accepted" or record.get("relevance_status") != "relevant": errors.append(f"organization evidence source is not accepted+relevant: {source_id}")
        tags = entry.get("mechanisms")
        if not isinstance(tags, list) or not tags or len(tags) != len(set(tags)): errors.append(f"mechanisms must be a nonempty unique list: {source_id}"); continue
        invalid = sorted(set(tags) - set(VOCABULARY))
        if invalid: errors.append(f"invalid mechanism tags for {source_id}: {', '.join(invalid)}")
        if tags != [tag for tag in VOCABULARY if tag in tags]: errors.append(f"mechanism tags are not in canonical order: {source_id}")
        for field in ("claim", "evidence_locator", "evidence_basis"):
            if not isinstance(entry.get(field), str) or not entry[field].strip(): errors.append(f"missing {field}: {source_id}")
        if record.get("platform") in {"github", "reddit"}: errors.append(f"generic-tooling-prone platform requires exclusion, not organization evidence: {source_id}")
        mechanisms.update(tags); platforms.update([str(record["platform"])]); outcomes += "measurable outcome" in tags
        indexed[str(org)].append({"source_id":source_id,"source_title":record["title"],"source_url":record["canonical_url"],"platform":record["platform"],"artifact_level":record["artifact_level"],"mechanisms":tags,"claim":entry["claim"],"evidence_locator":entry["evidence_locator"],"evidence_basis":entry["evidence_basis"],"source_path":record["path"]})
    exclusion_ids = set()
    evidence_ids = {str(e.get("source_id")) for e in manifest.get("evidence", [])}
    for item in manifest.get("exclusions", []):
        source_id = str(item.get("source_id", ""))
        if source_id in exclusion_ids: errors.append(f"duplicate organization-evidence exclusion: {source_id}")
        exclusion_ids.add(source_id); record = by_id.get(source_id)
        if not record: errors.append(f"exclusion references missing source: {source_id}")
        elif record.get("lifecycle") != "accepted": errors.append(f"sampled exclusion is not accepted: {source_id}")
        if not isinstance(item.get("reason"), str) or len(item["reason"].strip()) < 30: errors.append(f"exclusion needs a substantive reason: {source_id}")
        if source_id in evidence_ids: errors.append(f"source cannot be both evidence and excluded: {source_id}")
    if len(exclusion_ids) < 10: errors.append("at least 10 independently sampled exclusions are required")
    organizations = [{"organization":org,"source_count":len(rows),"mechanisms":[tag for tag in VOCABULARY if any(tag in row["mechanisms"] for row in rows)],"sources":sorted(rows,key=lambda r:r["source_id"])} for org, rows in sorted(indexed.items())]
    dashboard = {"schema_version":1,"organization_count":len(organizations),"organization_evidence_source_count":sum(x["source_count"] for x in organizations),"sampled_exclusion_count":len(exclusion_ids),"sources_with_measurable_outcome":outcomes,"by_mechanism":{tag:mechanisms[tag] for tag in VOCABULARY},"by_platform":dict(sorted(platforms.items())),"organizations":organizations}
    lines = ["# Canonical Organization Evidence Index","","Generated from `research/organization-evidence.json`. Only accepted evidence about a named organization's implemented operating practice is indexed; generic tooling and theory are excluded.","",f"- Organizations: **{dashboard['organization_count']}**",f"- Organization-evidence source links: **{dashboard['organization_evidence_source_count']}**",f"- Sources with a measurable outcome: **{outcomes}**",f"- Independently sampled generic/theory exclusions: **{len(exclusion_ids)}**","","## Mechanism dashboard","","| Mechanism | Source links |","| --- | ---: |"]
    lines += [f"| {tag} | {mechanisms[tag]} |" for tag in VOCABULARY]; lines += ["","## Organizations",""]
    for item in organizations:
        lines += [f"### {item['organization']}",""]
        for row in item["sources"]: lines.append(f"- [{row['source_title']}]({row['source_url']}) — {', '.join(row['mechanisms'])}. {row['claim']} Evidence: {row['evidence_basis']}")
        lines.append("")
    lines += ["## Exclusion audit sample","","These records remain accepted as topical corpus sources but do not count as organization evidence.",""]
    for item in manifest["exclusions"]: lines.append(f"- `{item['source_id']}` — {by_id.get(str(item['source_id']), {}).get('title', 'missing source')}: {item['reason']}")
    return dashboard, "\n".join(lines)+"\n", errors

def main():
    dashboard, markdown, errors = build()
    if errors: print("\n".join(errors), file=sys.stderr); return 1
    (ROOT/"metadata/organization-index.json").write_text(json.dumps(dashboard,indent=2,sort_keys=True)+"\n")
    (ROOT/"research/company-index.md").write_text(markdown)
    print(f"generated {dashboard['organization_count']} organizations from {dashboard['organization_evidence_source_count']} source links"); return 0
if __name__ == "__main__": raise SystemExit(main())
