#!/usr/bin/env python3
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/benchmark/public-competitor-benchmark.json"


def validate(path=PATH):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("largest_claim", {}).get("permitted") is not False:
        errors.append("largest claim must remain false until independently proven")
    rows = data.get("collections")
    if not isinstance(rows, list) or not rows:
        return ["collections must be a non-empty list"]
    required = {"id", "name", "url", "scope", "update_date", "update_date_precision", "schema", "raw_count", "raw_count_unit", "raw_count_method", "strict_like_for_like_organization_evidence_count", "strict_count_method", "exclusions", "retrieval_evidence"}
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
        if not row["schema"] or not row["exclusions"] or not row["retrieval_evidence"]:
            errors.append(f"{label} schema, exclusions and retrieval_evidence must be non-empty")
        if row["update_date"] is None:
            if row["update_date_precision"] != "unknown":
                errors.append(f"{label} null update_date requires unknown precision")
        else:
            try:
                date.fromisoformat(row["update_date"])
            except (TypeError, ValueError):
                errors.append(f"{label} update_date must be ISO date or null")
        for evidence in row["retrieval_evidence"]:
            if not all(isinstance(evidence.get(k), str) and evidence[k].strip() for k in ("retrieved_at", "method", "evidence")):
                errors.append(f"{label} retrieval evidence is incomplete")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        raise SystemExit("\n".join(problems))
    print(f"public competitor benchmark valid: {len(json.loads(PATH.read_text())['collections'])} collections")
