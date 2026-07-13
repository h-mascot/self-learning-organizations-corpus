#!/usr/bin/env python3
"""Human-in-the-loop review server and overlay tooling for the corpus.

The review layer never mutates ``sources/``. Only ``apply --yes`` does that;
``apply`` without the flag prints a dry-run plan.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import threading
from collections import Counter, defaultdict
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.corpus import parse_document  # noqa: E402

PLATFORMS = ("youtube", "academic", "x", "reddit", "substack", "blogs", "podcasts", "conferences", "books", "case-studies", "github")
DECISIONS = {"accept", "maybe", "reject"}
CATEGORY_LABELS = {"works": "Works", "maybe": "Maybe", "doesnt_fit": "Doesn't fit"}
SUBSTANTIVE_ARTIFACTS = {"transcript", "full_text", "abstract", "excerpt"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                parts.append(str(item.get("text") or item.get("phrase") or ""))
            else:
                parts.append(str(item))
        value = " ".join(parts)
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text


def _lifecycle(meta: dict[str, object], path: Path) -> str:
    return str(meta.get("lifecycle") or meta.get("status") or (path.parent.name if path.parent.name in {"accepted", "rejected", "blocked"} else "retrieved"))


def _artifact(meta: dict[str, object], path: Path) -> str:
    explicit = meta.get("artifact_level")
    if explicit:
        return str(explicit)
    if str(meta.get("platform")) == "youtube":
        return "transcript"
    availability = str(meta.get("availability") or "")
    if availability in {"full_text", "transcript"}:
        return availability
    return "excerpt" if path.suffix == ".md" else "metadata_only"


def ada_categorize(lifecycle: str, relevance: str, artifact: str, evidence_text: str) -> tuple[str, str]:
    """Return a conservative, deterministic Ada pre-review category and reason."""
    if lifecycle in {"rejected", "blocked"}:
        return "doesnt_fit", f"Canonical lifecycle is {lifecycle}; preserve the rejection unless new evidence overturns it."
    if relevance == "irrelevant":
        return "doesnt_fit", "Canonical relevance is irrelevant."
    if artifact in {"unavailable", "retrieval_evidence"}:
        return "doesnt_fit", f"Artifact level is {artifact}, so there is no reviewable source evidence."
    evidence_len = len(evidence_text.strip())
    if lifecycle == "accepted" and relevance == "relevant" and artifact in SUBSTANTIVE_ARTIFACTS:
        return "works", f"Accepted + relevant with {artifact} evidence ({evidence_len} reviewable characters)."
    if lifecycle == "accepted" and relevance == "relevant":
        evidence_note = "retained evidence is present" if evidence_len >= 80 else "retained evidence is thin"
        return "maybe", f"Accepted and relevant, but artifact level is {artifact}; {evidence_note} ({evidence_len} characters), so human confirmation is useful."
    return "maybe", f"Lifecycle/relevance is {lifecycle}/{relevance} with {artifact} evidence; human judgment is required."


def _read_resource(root: Path, path: Path) -> dict[str, object]:
    relative = path.relative_to(root).as_posix()
    body = ""
    if path.suffix == ".json":
        meta = json.loads(path.read_text(encoding="utf-8"))
        evidence = meta.get("evidence", [])
        evidence_text = _clean_text(evidence)
    else:
        meta, body = parse_document(path)
        evidence_text = " ".join(filter(None, (
            _clean_text(meta.get("relevance_reason")),
            _clean_text(meta.get("relevance_evidence")),
            _clean_text(meta.get("relevance_spans")),
            _clean_text(body),
        )))
    platform = str(meta.get("platform") or ("academic" if "academic_schema_version" in meta else path.relative_to(root / "sources").parts[0]))
    lifecycle = _lifecycle(meta, path)
    inferred_relevance = "relevant" if lifecycle == "accepted" and meta.get("relevance_evidence") else ("irrelevant" if lifecycle == "rejected" else "unknown")
    relevance = str(meta.get("relevance_status") or inferred_relevance)
    artifact = _artifact(meta, path)
    ada_category, ada_reason = ada_categorize(lifecycle, relevance, artifact, evidence_text)
    stable_id = str(meta.get("stable_id") or hashlib.sha256(relative.encode()).hexdigest()[:20])
    resource_id = hashlib.sha256(relative.encode()).hexdigest()[:20]
    title = _clean_text(meta.get("title")) or path.stem
    summary_parts = [
        _clean_text(meta.get("relevance_reason")),
        _clean_text(meta.get("relevance_evidence")),
        _clean_text(meta.get("evidence")),
        _clean_text(body),
    ]
    summary = next((part for part in summary_parts if part), "No retained summary or evidence text.")[:3000]
    keys = ("publisher", "creator", "authors", "published_date", "source_type", "content_type", "rights_status", "rights_holder", "provenance", "retrieved_at", "query_ids", "relevance_categories", "rejection_reason")
    metadata = {key: meta[key] for key in keys if key in meta and meta[key] not in (None, "", [])}
    return {
        "id": resource_id,
        "stable_id": stable_id,
        "title": title,
        "platform": platform,
        "lifecycle": lifecycle,
        "relevance_status": relevance,
        "artifact_level": artifact,
        "source_url": str(meta.get("canonical_url") or ""),
        "path": relative,
        "summary": summary,
        "evidence": evidence_text[:12000] or summary,
        "metadata": metadata,
        "ada_category": ada_category,
        "ada_label": CATEGORY_LABELS[ada_category],
        "ada_reason": ada_reason,
    }


class ResourceIndex:
    def __init__(self, root: Path = ROOT):
        self.root = Path(root).resolve()
        self._resources: list[dict[str, object]] | None = None

    def all(self) -> list[dict[str, object]]:
        if self._resources is None:
            source_root = self.root / "sources"
            paths = sorted(
                path for path in source_root.glob("**/*")
                if path.is_file() and path.suffix in {".md", ".json"} and path.name != "README.md" and path.name != ".gitkeep"
            )
            self._resources = [_read_resource(self.root, path) for path in paths]
        return self._resources

    def by_id(self) -> dict[str, dict[str, object]]:
        return {str(item["id"]): item for item in self.all()}


class DecisionStore:
    _lock = threading.RLock()

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.decisions_path = self.data_dir / "decisions.json"
        self.feedback_path = self.data_dir / "feedback.json"

    def _load_document(self) -> dict[str, object]:
        if not self.decisions_path.exists():
            return {"schema_version": 1, "updated_at": None, "decisions": {}}
        loaded = json.loads(self.decisions_path.read_text(encoding="utf-8"))
        if not isinstance(loaded.get("decisions"), dict):
            raise ValueError("decisions.json must contain a decisions object")
        return loaded

    def all(self) -> dict[str, dict[str, object]]:
        return dict(self._load_document()["decisions"])

    def get(self, resource_id: str) -> dict[str, object] | None:
        return self.all().get(resource_id)

    def save(self, resource: dict[str, object], decision: str, comment: str = "", *, export: bool = True) -> dict[str, object]:
        if decision not in DECISIONS:
            raise ValueError(f"decision must be one of {sorted(DECISIONS)}")
        now = utc_now()
        saved = {
            "resource_id": resource["id"],
            "stable_id": resource["stable_id"],
            "path": resource["path"],
            "platform": resource["platform"],
            "ada_category": resource["ada_category"],
            "decision": decision,
            "comment": str(comment).strip(),
            "updated_at": now,
        }
        with self._lock:
            document = self._load_document()
            document["schema_version"] = 1
            document["updated_at"] = now
            document["decisions"][str(resource["id"])] = saved
            self._atomic_json(self.decisions_path, document)
            if export:
                self.export_feedback()
        return saved

    def export_feedback(self) -> dict[str, object]:
        decisions = self.all()
        resources = ResourceIndex(self.data_dir.parents[1]).by_id()
        positive, negative, queue = [], [], []
        platform_preferences: dict[str, Counter] = defaultdict(Counter)
        category_preferences: dict[str, Counter] = defaultdict(Counter)
        for resource_id, decision in sorted(decisions.items()):
            resource = resources.get(resource_id)
            if not resource:
                continue
            choice = str(decision["decision"])
            platform_preferences[str(resource["platform"])][choice] += 1
            category_preferences[str(resource["ada_category"])][choice] += 1
            if choice not in {"accept", "reject"}:
                continue
            polarity = "positive" if choice == "accept" else "negative"
            seed = {
                "resource_id": resource_id,
                "stable_id": resource["stable_id"],
                "platform": resource["platform"],
                "title": resource["title"],
                "source_url": resource["source_url"],
                "text": resource["summary"],
                "comment": decision.get("comment", ""),
                "polarity": polarity,
            }
            (positive if choice == "accept" else negative).append(seed)
            queue.append({"resource_id": resource_id, "polarity": polarity, "platform": resource["platform"], "text": resource["summary"], "comment": decision.get("comment", "")})
        feedback = {
            "schema_version": 1,
            "generated_at": utc_now(),
            "description": "Review-derived similarity seeds and category preferences for future corpus research.",
            "positive_similarity_seeds": positive,
            "negative_similarity_seeds": negative,
            "category_preferences": {
                "platforms": {key: dict(sorted(value.items())) for key, value in sorted(platform_preferences.items())},
                "ada_categories": {key: dict(sorted(value.items())) for key, value in sorted(category_preferences.items())},
            },
            "feedback_queue": queue,
        }
        self._atomic_json(self.feedback_path, feedback)
        return feedback

    def _atomic_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, path)


def bulk_save(store: DecisionStore, resources: list[dict[str, object]], decision: str, comment: str = "") -> dict[str, list[str]]:
    if decision not in {"accept", "reject"}:
        raise ValueError("bulk decision must be accept or reject")
    safe_category = "works" if decision == "accept" else "doesnt_fit"
    saved, skipped = [], []
    for resource in resources:
        resource_id = str(resource["id"])
        if resource["ada_category"] != safe_category:
            skipped.append(resource_id)
            continue
        store.save(resource, decision, comment, export=False)
        saved.append(resource_id)
    if saved:
        store.export_feedback()
    return {"saved": saved, "skipped": skipped}


def _destination_for(path: Path, decision: str) -> Path:
    parts = list(path.parts)
    target = "accepted" if decision == "accept" else "rejected"
    for current in ("accepted", "rejected", "blocked", "retrieved", "discovered"):
        if current in parts:
            parts[parts.index(current)] = target
            return Path(*parts)
    return path.parent / target / path.name


def _updated_content(path: Path, decision: str, comment: str) -> str:
    target = "accepted" if decision == "accept" else "rejected"
    if path.suffix == ".json":
        record = json.loads(path.read_text(encoding="utf-8"))
        key = "lifecycle" if "lifecycle" in record else "status"
        record[key] = target
        if "relevance_status" in record:
            record["relevance_status"] = "relevant" if decision == "accept" else "irrelevant"
        if decision == "reject":
            record["rejection_reason"] = comment or "Rejected in human review."
        else:
            record["rejection_reason"] = None
        return json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    text = path.read_text(encoding="utf-8")
    key = "status" if re.search(r"(?m)^status:", text) else "lifecycle"
    text = re.sub(rf"(?m)^{key}:.*$", f'{key}: "{target}"', text, count=1)
    if re.search(r"(?m)^relevance_status:", text):
        relevance = "relevant" if decision == "accept" else "irrelevant"
        text = re.sub(r"(?m)^relevance_status:.*$", f'relevance_status: "{relevance}"', text, count=1)
    if decision == "reject":
        reason = json.dumps(comment or "Rejected in human review.", ensure_ascii=False)
        if re.search(r"(?m)^rejection_reason:", text):
            text = re.sub(r"(?m)^rejection_reason:.*$", f"rejection_reason: {reason}", text, count=1)
        else:
            text = text.replace("\n---\n", f"\nrejection_reason: {reason}\n---\n", 1)
    else:
        text = re.sub(r"(?m)^rejection_reason:.*\n", "", text, count=1)
    return text


def apply_decisions(root: Path, data_dir: Path, yes: bool = False) -> dict[str, object]:
    root, data_dir = Path(root).resolve(), Path(data_dir).resolve()
    decisions = DecisionStore(data_dir).all()
    resources = ResourceIndex(root).by_id()
    actions = []
    for resource_id, decision in sorted(decisions.items()):
        choice = str(decision.get("decision"))
        if choice == "maybe" or resource_id not in resources:
            continue
        resource = resources[resource_id]
        current = root / str(resource["path"])
        destination = _destination_for(current, choice)
        target_lifecycle = "accepted" if choice == "accept" else "rejected"
        if current == destination and resource["lifecycle"] == target_lifecycle:
            continue
        action = {
            "resource_id": resource_id,
            "decision": choice,
            "source": current.relative_to(root).as_posix(),
            "destination": destination.relative_to(root).as_posix(),
            "comment": decision.get("comment", ""),
        }
        actions.append(action)
        if yes:
            if destination.exists() and destination != current:
                raise FileExistsError(f"refusing to overwrite {destination}")
            content = _updated_content(current, choice, str(decision.get("comment", "")))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
            if destination != current:
                current.unlink()
    return {"dry_run": not yes, "planned": len(actions), "applied": len(actions) if yes else 0, "actions": actions}


def _filter_resources(resources: list[dict[str, object]], decisions: dict[str, dict[str, object]], query: dict[str, list[str]]) -> list[dict[str, object]]:
    search = query.get("search", [""])[0].strip().lower()
    platform = query.get("platform", ["all"])[0]
    category = query.get("category", ["all"])[0]
    pending = query.get("pending", ["false"])[0].lower() in {"1", "true", "yes"}
    result = []
    for resource in resources:
        if platform != "all" and resource["platform"] != platform:
            continue
        if category != "all" and resource["ada_category"] != category:
            continue
        if pending and resource["id"] in decisions:
            continue
        haystack = " ".join(str(resource.get(key, "")) for key in ("title", "stable_id", "path", "summary", "platform")).lower()
        if search and search not in haystack:
            continue
        item = dict(resource)
        item["decision"] = decisions.get(str(resource["id"]))
        result.append(item)
    return result


def _progress(resources: list[dict[str, object]], decisions: dict[str, dict[str, object]]) -> dict[str, int]:
    counts = Counter(str(item["decision"]) for item in decisions.values())
    return {"total": len(resources), "decided": len(decisions), "pending": max(0, len(resources) - len(decisions)), "accept": counts["accept"], "maybe": counts["maybe"], "reject": counts["reject"]}


class ReviewHandler(BaseHTTPRequestHandler):
    server_version = "CorpusReview/1.0"

    @property
    def root(self) -> Path:
        return self.server.root  # type: ignore[attr-defined]

    @property
    def data_dir(self) -> Path:
        return self.server.data_dir  # type: ignore[attr-defined]

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/resources":
            index = ResourceIndex(self.root)
            all_resources = index.all()
            decisions = DecisionStore(self.data_dir).all()
            filtered = _filter_resources(all_resources, decisions, parse_qs(parsed.query))
            query = parse_qs(parsed.query)
            page = max(1, int(query.get("page", ["1"])[0]))
            page_size = min(100, max(1, int(query.get("page_size", ["25"])[0])))
            start = (page - 1) * page_size
            platform_counts = Counter(str(item["platform"]) for item in all_resources)
            category_counts = Counter(str(item["ada_category"]) for item in all_resources)
            self._json({"items": filtered[start:start + page_size], "page": page, "page_size": page_size, "filtered_total": len(filtered), "progress": _progress(all_resources, decisions), "platform_counts": dict(platform_counts), "category_counts": dict(category_counts)})
            return
        if parsed.path == "/api/health":
            resources = ResourceIndex(self.root).all()
            decisions = DecisionStore(self.data_dir).all()
            self._json({"status": "ok", "resources": len(resources), "decisions": len(decisions)})
            return
        if parsed.path.startswith("/api/resources/"):
            resource_id = unquote(parsed.path.rsplit("/", 1)[-1])
            resource = ResourceIndex(self.root).by_id().get(resource_id)
            if not resource:
                self._json({"error": "resource not found"}, HTTPStatus.NOT_FOUND); return
            result = dict(resource)
            result["decision"] = DecisionStore(self.data_dir).get(resource_id)
            self._json(result); return
        if parsed.path == "/api/feedback":
            store = DecisionStore(self.data_dir)
            self._json(store.export_feedback()); return
        if parsed.path == "/api/report":
            resources = ResourceIndex(self.root).all()
            store = DecisionStore(self.data_dir)
            feedback = store.export_feedback()
            self._json({"progress": _progress(resources, store.all()), "decisions": list(store.all().values()), "feedback_queue": feedback["feedback_queue"]}); return
        if parsed.path in {"/", "/index.html"}:
            self._file(self.root / "review-ui" / "index.html", "text/html; charset=utf-8"); return
        if parsed.path == "/app.js":
            self._file(self.root / "review-ui" / "app.js", "text/javascript; charset=utf-8"); return
        if parsed.path == "/styles.css":
            self._file(self.root / "review-ui" / "styles.css", "text/css; charset=utf-8"); return
        self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._body()
            if self.path == "/api/decisions":
                resource_id = str(payload.get("resource_id", ""))
                resource = ResourceIndex(self.root).by_id().get(resource_id)
                if not resource:
                    self._json({"error": "resource not found"}, HTTPStatus.NOT_FOUND); return
                saved = DecisionStore(self.data_dir).save(resource, str(payload.get("decision", "")), str(payload.get("comment", "")))
                self._json({"saved": saved}, HTTPStatus.CREATED); return
            if self.path == "/api/bulk":
                by_id = ResourceIndex(self.root).by_id()
                ids = payload.get("resource_ids", [])
                if not isinstance(ids, list):
                    raise ValueError("resource_ids must be an array")
                selected = [by_id[item] for item in ids if item in by_id]
                result = bulk_save(DecisionStore(self.data_dir), selected, str(payload.get("decision", "")), str(payload.get("comment", "")))
                self._json(result, HTTPStatus.CREATED); return
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def _body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 1_000_000:
            raise ValueError("request too large")
        value = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(value, dict):
            raise ValueError("JSON body must be an object")
        return value

    def _json(self, value: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._json({"error": "asset not found"}, HTTPStatus.NOT_FOUND); return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def serve(root: Path, data_dir: Path, host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), ReviewHandler)
    server.root = Path(root).resolve()  # type: ignore[attr-defined]
    server.data_dir = Path(data_dir).resolve()  # type: ignore[attr-defined]
    print(f"Corpus review UI: http://{host}:{port}", flush=True)
    print(f"Decisions: {server.data_dir / 'decisions.json'}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def print_report(root: Path, data_dir: Path, as_json: bool = False) -> None:
    resources = ResourceIndex(root).all()
    store = DecisionStore(data_dir)
    feedback = store.export_feedback()
    report = {"progress": _progress(resources, store.all()), "decisions": list(store.all().values()), "feedback_queue": feedback["feedback_queue"]}
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False)); return
    progress = report["progress"]
    print(f"Review progress: {progress['decided']}/{progress['total']} decided; {progress['pending']} pending")
    print(f"Accept {progress['accept']} | Maybe {progress['maybe']} | Reject {progress['reject']}")
    print("\nDecisions:")
    for item in report["decisions"]:
        print(f"- {str(item['decision']).upper():6} {item['platform']:12} {item['path']} :: {item.get('comment') or '—'}")
    print(f"\nFeedback queue: {len(report['feedback_queue'])} similarity seed(s)")
    for item in report["feedback_queue"]:
        print(f"- {str(item['polarity']).upper():8} {item['platform']:12} {item['resource_id']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--data-dir", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    serve_parser = sub.add_parser("serve", help="run the local review UI")
    serve_parser.add_argument("--host", default="0.0.0.0")
    serve_parser.add_argument("--port", type=int, default=8765)
    report_parser = sub.add_parser("report", help="show decisions and feedback queue")
    report_parser.add_argument("--json", action="store_true")
    sub.add_parser("export-feedback", help="regenerate the machine-readable feedback artifact")
    apply_parser = sub.add_parser("apply", help="plan source updates; mutates only with --yes")
    apply_parser.add_argument("--yes", action="store_true", help="apply planned moves and metadata updates")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    data_dir = (args.data_dir or root / "review-ui" / "data").resolve()
    if args.command == "serve":
        serve(root, data_dir, args.host, args.port)
    elif args.command == "report":
        print_report(root, data_dir, args.json)
    elif args.command == "export-feedback":
        print(json.dumps(DecisionStore(data_dir).export_feedback(), indent=2, ensure_ascii=False))
    elif args.command == "apply":
        result = apply_decisions(root, data_dir, args.yes)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not args.yes:
            print("Dry run only. Re-run with --yes to mutate canonical sources.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
