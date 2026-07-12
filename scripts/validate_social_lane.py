#!/usr/bin/env python3
"""Strict validator for resource identity and source evidence in the social lane."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.social_acquisition import NEWSLETTERS, article_text, clean_reader
QUOTAS = {"x": 50, "reddit": 25, "substack": 25}
NEWSLETTER_HOSTS = {urlsplit(row[0]).hostname for row in NEWSLETTERS}
PROVENANCE = {
    "x": "FxTwitter public API response for the canonical X resource",
    "reddit": "Arctic Shift public Reddit archive record with exact post ID",
    "substack": "Jina Reader direct fetch of the canonical individual article",
}


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


def normalized_url(url: str) -> str:
    parts = urlsplit(url)
    path = re.sub(r"/+", "/", parts.path).rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def source_span(body: str) -> str:
    match = re.search(r"## (?:Complete source text|Verified source excerpt)\n\n(.*?)\n\n## Acquisition limits", body, re.S)
    return match.group(1).strip() if match else ""


def validate(root: Path = ROOT):
    errors, seen_urls, seen_ids, seen_hashes, counts = [], set(), set(), set(), {}
    required = {
        "platform", "stable_id", "title", "publisher", "canonical_url", "published_date",
        "status", "availability", "provenance", "raw_path", "rights_status", "content_sha256",
    }
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
                continue
            if meta["platform"] != platform or meta["status"] != "accepted":
                errors.append(f"{path}: platform/status does not match accepted path")
            try:
                published = date.fromisoformat(meta["published_date"])
                if published.year <= 1:
                    raise ValueError
            except ValueError:
                errors.append(f"{path}: misleading or invalid publication date")
            if not path.name.startswith(meta["published_date"] + "--"):
                errors.append(f"{path}: filename/date mismatch")

            url = normalized_url(meta["canonical_url"])
            parts = urlsplit(url)
            if parts.scheme != "https":
                errors.append(f"{path}: canonical URL must use HTTPS")
            if url in seen_urls:
                errors.append(f"{path}: duplicate canonical resource")
            seen_urls.add(url)
            key = (platform, meta["stable_id"])
            if key in seen_ids:
                errors.append(f"{path}: duplicate stable ID")
            seen_ids.add(key)

            if platform == "x":
                match = re.fullmatch(r"/[^/]+/status/(\d+)", parts.path)
                if parts.hostname != "x.com" or not match or match.group(1) != meta["stable_id"]:
                    errors.append(f"{path}: invalid/non-canonical X resource URL")
                if meta["availability"] != "full_text":
                    errors.append(f"{path}: complete X source must be full_text")
            elif platform == "reddit":
                match = re.search(r"/comments/([a-z0-9]+)/", parts.path + "/")
                if parts.hostname != "www.reddit.com" or not match or match.group(1) != meta["stable_id"]:
                    errors.append(f"{path}: invalid/non-canonical Reddit resource URL")
                if meta["availability"] != "full_text":
                    errors.append(f"{path}: complete Reddit self-post must be full_text")
            else:
                if parts.hostname not in NEWSLETTER_HOSTS:
                    errors.append(f"{path}: newsletter domain is not in the retrieved allow-list")
                if not re.match(r"^/p/[^/]+/?$", parts.path):
                    errors.append(f"{path}: newsletter URL is not an individual /p/ article")
                if meta["availability"] != "metadata_only":
                    errors.append(f"{path}: bounded newsletter excerpt must be metadata_only")

            if meta["provenance"] != PROVENANCE[platform]:
                errors.append(f"{path}: generic or unrecognized provenance")
            span = source_span(body)
            minimum = 500 if platform == "substack" else (200 if platform == "reddit" else 80)
            if len(span) < minimum:
                errors.append(f"{path}: source evidence is non-substantive ({len(span)} chars)")
            span_hash = hashlib.sha256(span.encode()).hexdigest()
            if span_hash in seen_hashes:
                errors.append(f"{path}: duplicate source evidence")
            seen_hashes.add(span_hash)
            raw_path = root / meta["raw_path"]
            if not raw_path.is_file():
                errors.append(f"{path}: preserved raw source is missing")
            else:
                try:
                    if platform == "x":
                        tweet = json.loads(raw_path.read_text())["tweet"]
                        raw_span = tweet.get("text", "").strip() or article_text(tweet.get("article") or {})
                    elif platform == "reddit":
                        posts = json.loads(raw_path.read_text())["data"]
                        raw_span = next(p["selftext"].strip() for p in posts if p["id"] == meta["stable_id"])
                    else:
                        raw_span = clean_reader(raw_path.read_text())[1]
                    if span != raw_span:
                        errors.append(f"{path}: evidence is not an exact span from preserved source")
                except (KeyError, StopIteration, ValueError, json.JSONDecodeError):
                    errors.append(f"{path}: preserved raw source cannot prove the excerpt")
            if hashlib.sha256(body.encode()).hexdigest() != meta["content_sha256"]:
                errors.append(f"{path}: content hash mismatch")
            if "public search index bounded excerpt" in body.lower() or "newsletter analysis" in span.lower():
                errors.append(f"{path}: non-source/generic excerpt")
    return counts, errors


if __name__ == "__main__":
    counts, errors = validate()
    print(counts)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
