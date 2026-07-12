#!/usr/bin/env python3
import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/benchmark/public-competitor-benchmark.json"


def validate(path=PATH):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    try:
        as_of = date.fromisoformat(data.get("as_of", ""))
    except (TypeError, ValueError):
        as_of = None
        errors.append("as_of must be an ISO date")
    if data.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if data.get("largest_claim", {}).get("permitted") is not False:
        errors.append("largest claim must remain false until independently proven")
    rows = data.get("collections")
    if not isinstance(rows, list) or not rows:
        return ["collections must be a non-empty list"]
    required = {"id", "name", "url", "scope", "update_date", "update_date_precision", "schema", "raw_count", "raw_count_relation", "raw_count_unit", "raw_count_method", "strict_like_for_like_organization_evidence_count", "strict_count_method", "exclusions", "retrieval_evidence", "audit"}
    ids = set()
    for i, row in enumerate(rows):
        label = f"collections[{i}]"
        missing = required - set(row)
        if missing:
            errors.append(f"{label} missing {sorted(missing)}")
            continue
        if row["id"] in ids:
            errors.append(f"duplicate id: {row['id']}")
        ids.add(row["id"])
        parsed = urlparse(row["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{label} url must be public https")
        for field in ("scope", "raw_count_unit", "raw_count_method", "strict_count_method"):
            if not isinstance(row[field], str) or not row[field].strip():
                errors.append(f"{label} {field} must be non-empty")
        raw = row["raw_count"]
        strict = row["strict_like_for_like_organization_evidence_count"]
        if type(raw) is not int or raw < 0 or type(strict) is not int or strict < 0 or strict > raw:
            errors.append(f"{label} counts must be integers with 0 <= strict <= raw")
        if row["raw_count_relation"] not in {"exact", "publisher_floor"}:
            errors.append(f"{label} raw_count_relation is invalid")
        if not row["schema"] or not row["exclusions"] or not row["retrieval_evidence"]:
            errors.append(f"{label} schema, exclusions and retrieval_evidence must be non-empty")
        for field in ("schema", "exclusions"):
            if not isinstance(row[field], list) or not all(isinstance(v, str) and v.strip() for v in row[field]):
                errors.append(f"{label} {field} must be a non-empty string list")
        audit = row["audit"]
        if not isinstance(audit, dict):
            errors.append(f"{label} audit must be an object")
        else:
            coverage = audit.get("coverage")
            audit_rows = audit.get("rows")
            if coverage not in {"complete", "sample", "scope_only"}:
                errors.append(f"{label} audit coverage is invalid")
            if not isinstance(audit.get("selection_method"), str) or not audit["selection_method"].strip():
                errors.append(f"{label} audit selection_method must be non-empty")
            if type(audit.get("audited_unit_count")) is not int or audit["audited_unit_count"] < 0:
                errors.append(f"{label} audit audited_unit_count must be a non-negative integer")
            if not isinstance(audit_rows, list) or len(audit_rows) != audit.get("audited_unit_count"):
                errors.append(f"{label} audit row count must equal audited_unit_count")
            else:
                included = set()
                for j, item in enumerate(audit_rows):
                    item_label = f"{label}.audit.rows[{j}]"
                    if item.get("decision") not in {"include", "exclude", "duplicate"}:
                        errors.append(f"{item_label} decision is invalid")
                    if not all(isinstance(item.get(k), str) and item[k].strip() for k in ("label", "url", "reason")):
                        errors.append(f"{item_label} label, url and reason must be non-empty")
                    elif urlparse(item["url"]).scheme != "https" or not urlparse(item["url"]).netloc:
                        errors.append(f"{item_label} url must be public https")
                    if item.get("decision") == "include":
                        org = item.get("organization")
                        if not isinstance(org, str) or not org.strip():
                            errors.append(f"{item_label} included row requires organization")
                        else:
                            included.add(org.casefold())
                    if item.get("decision") == "duplicate":
                        org = item.get("organization")
                        if not isinstance(org, str) or org.casefold() not in included:
                            errors.append(f"{item_label} duplicate must name a previously included organization")
                if len(included) != strict:
                    errors.append(f"{label} strict count must equal unique included audit organizations")
                if coverage == "complete" and audit.get("audited_unit_count") != raw:
                    errors.append(f"{label} complete audit must cover raw_count units")
                if coverage == "sample" and not 0 < audit.get("audited_unit_count", 0) <= raw:
                    errors.append(f"{label} sample audit must cover between 1 and raw_count units")
                if coverage == "scope_only" and (audit_rows or strict != 0):
                    errors.append(f"{label} scope_only audit cannot have rows or a strict count")
        if row["update_date"] is None:
            if row["update_date_precision"] != "unknown":
                errors.append(f"{label} null update_date requires unknown precision")
        else:
            try:
                date.fromisoformat(row["update_date"])
            except (TypeError, ValueError):
                errors.append(f"{label} update_date must be ISO date or null")
        for evidence in row["retrieval_evidence"]:
            if not all(isinstance(evidence.get(k), str) and evidence[k].strip() for k in ("retrieved_at", "url", "method", "evidence")):
                errors.append(f"{label} retrieval evidence is incomplete")
                continue
            evidence_url = urlparse(evidence["url"])
            if evidence_url.scheme != "https" or not evidence_url.netloc:
                errors.append(f"{label} retrieval evidence url must be public https")
            try:
                retrieved = datetime.fromisoformat(evidence["retrieved_at"].replace("Z", "+00:00"))
                retrieved_date = retrieved.astimezone(timezone.utc).date() if retrieved.tzinfo else retrieved.date()
                if as_of and retrieved_date > as_of:
                    errors.append(f"{label} retrieval date cannot be after as_of")
            except (TypeError, ValueError):
                errors.append(f"{label} retrieved_at must be an ISO date or datetime")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        raise SystemExit("\n".join(problems))
    print(f"public competitor benchmark valid: {len(json.loads(PATH.read_text())['collections'])} collections")
