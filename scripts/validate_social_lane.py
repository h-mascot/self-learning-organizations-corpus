#!/usr/bin/env python3
"""Validate only the X, Reddit, and Substack/newsletter acquisition lane."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUOTAS = {"x": 50, "reddit": 25, "substack": 25}


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing YAML front matter")
    head, body = text[4:].split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key] = value.strip().strip('"')
    return meta, body.lstrip("\n")


def validate(root: Path = ROOT):
    errors, seen_urls, seen_ids, counts = [], set(), set(), {}
    required = {"platform", "stable_id", "title", "publisher", "canonical_url", "published_date",
                "status", "availability", "provenance", "rights_status", "content_sha256"}
    for platform, quota in QUOTAS.items():
        paths = sorted((root / "sources" / platform / "accepted").glob("*.md"))
        counts[platform] = len(paths)
        if len(paths) < quota:
            errors.append(f"{platform}: {len(paths)} accepted, quota {quota}")
        for path in paths:
            try:
                meta, body = parse(path)
            except ValueError as exc:
                errors.append(f"{path}: {exc}")
                continue
            missing = required - meta.keys()
            if missing:
                errors.append(f"{path}: missing {sorted(missing)}")
            if meta.get("platform") != platform:
                errors.append(f"{path}: platform/path mismatch")
            if meta.get("status") != "accepted":
                errors.append(f"{path}: accepted path without accepted status")
            if meta.get("availability") != "metadata_only":
                errors.append(f"{path}: bounded index excerpt must be metadata_only")
            url = meta.get("canonical_url", "")
            if not re.match(r"^https://", url):
                errors.append(f"{path}: non-HTTPS canonical URL")
            if url in seen_urls:
                errors.append(f"{path}: duplicate canonical URL")
            seen_urls.add(url)
            key = (platform, meta.get("stable_id"))
            if key in seen_ids:
                errors.append(f"{path}: duplicate stable ID")
            seen_ids.add(key)
            if hashlib.sha256(body.encode()).hexdigest() != meta.get("content_sha256"):
                errors.append(f"{path}: content hash mismatch")
            if "## Bounded evidence excerpt" not in body or "## Acquisition limits" not in body:
                errors.append(f"{path}: evidence/limits section missing")
    return counts, errors


if __name__ == "__main__":
    counts, errors = validate()
    print(counts)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
