from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.corpus import CorpusError, audit, body_hash, expected_name, format_document, generate, migrate


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def meta(self, **overrides):
        body = "# Useful source\n\n0:00 start\n0:50 finish\n"
        result = {
            "schema_version": "1", "platform": "youtube", "stable_id": "abc123",
            "title": "Learning Loops", "publisher": "Example Org",
            "canonical_url": "https://www.youtube.com/watch?v=abc123",
            "published_date": "2026-01-02", "duration_seconds": "60",
            "content_type": "transcript", "status": "accepted", "relevance_status": "relevant",
            "provenance": "publisher captions", "rights_status": "third-party",
            "rights_holder": "Example Org", "content_sha256": body_hash(body),
            "transcript_source": "captions",
        }
        result.update(overrides)
        return result, body

    def write(self, meta=None, body=None, filename=None):
        base, default_body = self.meta()
        if meta: base.update(meta)
        body = default_body if body is None else body
        base["content_sha256"] = body_hash(body)
        path = self.root / "sources" / base["platform"] / base["status"] / (filename or expected_name(base))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(format_document(base, body), encoding="utf-8")
        return path

    def errors(self):
        return "\n".join(audit(self.root)[1])

    def write_web_media(self, *, status="accepted", **overrides):
        evidence = [{"kind": "excerpt", "locator": "publisher body", "text": (f"A concrete organizational learning loop retains {status} feedback, evaluates operating results, records what the organization learned, and changes the next operating decision. " * 2).strip()}]
        record = {
            "schema_version": 2, "platform": "blogs", "stable_id": f"blogs-{status}",
            "title": f"Web media {status}", "creator": "Example Author", "publisher": "Example Org",
            "canonical_url": f"https://example.com/{status}", "published_date": None,
            "date_precision": "unknown", "source_type": "article", "status": status,
            "artifact_level": "metadata_only" if status == "accepted" else "unavailable",
            "retrieved_at": "2026-07-12T12:00:00Z", "retrieval_method": "public page",
            "provenance": "publisher page", "rights_status": "bounded-public-evidence" if status == "accepted" else "retrieval-evidence-only",
            "rights_note": "Only bounded evidence is retained.", "relevance_evidence": ["organizational learning loop"],
            "evidence": evidence if status != "blocked" else [], "query_ids": ["q-1"],
            "rejection_reason": None if status == "accepted" else "not accepted",
        }
        record.update(overrides)
        record["content_sha256"] = hashlib.sha256(json.dumps(record["evidence"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        path = self.root / "sources" / record["platform"] / status / f"web-media-{status}--{record['stable_id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_duplicate_ids_and_urls_are_rejected(self):
        self.write()
        self.write({"title": "Other", "publisher": "Other", "published_date": "2026-02-02"})
        errors = self.errors()
        self.assertIn("duplicate stable_id", errors)
        self.assertIn("duplicate canonical_url", errors)

    def test_duplicate_content_hashes_are_rejected_globally(self):
        self.write()
        self.write({"stable_id": "other1", "title": "Other", "canonical_url": "https://www.youtube.com/watch?v=other1"})
        self.assertIn("duplicate content_sha256", self.errors())

    def test_gitkeep_is_not_a_record(self):
        path = self.root / "sources/x/.gitkeep"
        path.parent.mkdir(parents=True)
        path.touch()
        self.assertEqual(([], []), audit(self.root))

    def test_web_media_json_records_are_validated_and_counted_by_lifecycle(self):
        self.write_web_media(status="accepted")
        self.write_web_media(status="rejected")
        self.write_web_media(status="blocked")
        records, errors = audit(self.root)
        self.assertEqual([], errors)
        self.assertEqual(["accepted", "blocked", "rejected"], sorted(record["lifecycle"] for record in records))
        stats = generate(self.root)
        self.assertEqual({"accepted": 1, "blocked": 1, "rejected": 1}, stats["by_lifecycle"])
        self.assertEqual({"bounded-public-evidence": 1, "retrieval-evidence-only": 2}, stats["by_rights_status"])

    def test_web_media_json_hash_path_and_rights_are_strict(self):
        path = self.write_web_media(rights_status="invented-rights")
        bad_path = path.with_name("wrong-name.json")
        path.rename(bad_path)
        path = bad_path
        record = json.loads(path.read_text())
        record["content_sha256"] = "0" * 64
        path.write_text(json.dumps(record), encoding="utf-8")
        errors = self.errors()
        self.assertIn("invalid web/media rights_status", errors)
        self.assertIn("content_sha256 does not match evidence", errors)
        self.assertIn("filename must be title-derived", errors)

    def test_canonical_audit_preserves_strict_lane_semantics(self):
        self.write_web_media(
            evidence=[{"kind": "excerpt", "locator": "publisher body", "text": "too short"}],
            query_ids=[],
        )
        errors = self.errors()
        self.assertIn("accepted source lacks a substantive publisher excerpt", errors)
        self.assertIn("query_ids must be a non-empty list", errors)

    def test_malformed_web_media_field_types_are_rejected_without_crashing(self):
        self.write_web_media(evidence=[{"kind": "excerpt", "locator": "body", "text": 7}])
        errors = self.errors()
        self.assertIn("invalid web/media field types", errors)
        self.assertIn("web/media evidence spans require non-empty", errors)

    def test_schema_version_two_markdown_still_uses_canonical_markdown_lane(self):
        body = "# Post\n\nPreserved public excerpt.\n"
        meta = {
            "schema_version": 2, "platform": "reddit", "stable_id": "t3_compat",
            "title": "Compatibility", "publisher": "Example User", "canonical_url": "https://reddit.com/r/example/comments/compat/post",
            "published_date": "unknown", "content_type": "post", "lifecycle": "accepted", "relevance_status": "relevant",
            "artifact_level": "excerpt", "retrieved_at": "2026-07-12T12:00:00Z", "provenance": "public page",
            "rights_status": "short-evidence-spans-only", "rights_holder": "Example User", "content_sha256": body_hash(body),
        }
        path = self.root / "sources/reddit/accepted/compat.md"
        path.parent.mkdir(parents=True)
        path.write_text(format_document(meta, body), encoding="utf-8")
        self.assertEqual([], audit(self.root)[1])

    def test_generated_csv_keeps_embedded_title_whitespace_on_one_row(self):
        self.write_web_media(publisher="Publisher with\n  wrapped whitespace")
        generate(self.root)
        lines = (self.root / "metadata/sources.csv").read_text().splitlines()
        self.assertEqual(2, len(lines))
        self.assertIn("Publisher with wrapped whitespace", lines[1])

    def test_future_canonical_record_lifecycle_and_artifact_are_validated(self):
        body = "# Post\n\nPreserved public excerpt.\n"
        meta = {
            "schema_version": 2, "platform": "reddit", "stable_id": "t3_example",
            "title": "Learning systems", "publisher": "Example User",
            "canonical_url": "https://reddit.com/r/example/comments/example/post",
            "published_date": "unknown", "content_type": "post", "lifecycle": "accepted",
            "relevance_status": "relevant", "artifact_level": "excerpt",
            "retrieved_at": "2026-07-12T12:00:00+00:00", "provenance": "Reddit public page",
            "rights_status": "short-evidence-spans-only", "rights_holder": "Example User",
            "content_sha256": body_hash(body),
        }
        path = self.root / "sources/reddit/accepted/example.md"
        path.parent.mkdir(parents=True)
        path.write_text(format_document(meta, body), encoding="utf-8")
        self.assertEqual([], audit(self.root)[1])
        meta["artifact_level"] = "invented-fuller-text"
        path.write_text(format_document(meta, body), encoding="utf-8")
        self.assertIn("invalid artifact_level", self.errors())

    def test_empty_transcript_is_rejected(self):
        self.write(body="")
        self.assertIn("transcript is empty", self.errors())

    def test_malformed_metadata_is_rejected(self):
        path = self.root / "sources/youtube/accepted/bad.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\ntitle broken\n---\ntext", encoding="utf-8")
        self.assertIn("malformed metadata", self.errors())

    def test_bad_date_and_duration_are_rejected(self):
        self.write({"published_date": "2026-02-30", "duration_seconds": "nope"})
        errors = self.errors()
        self.assertIn("real YYYY-MM-DD", errors)
        self.assertIn("positive integer", errors)

    def test_missing_rights_is_rejected(self):
        self.write({"rights_status": ""})
        self.assertIn("rights_status", self.errors())

    def test_random_id_filename_is_rejected(self):
        self.write(filename="abc123.md")
        self.assertIn("noncanonical filename", self.errors())

    def test_filename_collision_is_detected_before_overwrite(self):
        legacy = self.root / "transcripts/youtube"
        legacy.mkdir(parents=True)
        legacy_meta = {"video_id": "abc123", "title": "Learning Loops", "channel": "Example Org", "source_url": "https://youtu.be/abc123", "duration_seconds": "60", "upload_date": "20260102", "transcript_source": "captions"}
        body = "# x\n\n0:00 start\n0:50 finish\n"
        (legacy / "one.md").write_text(format_document(legacy_meta, body))
        (legacy / "two.md").write_text(format_document(legacy_meta, body))
        with self.assertRaisesRegex(CorpusError, "migration collision"):
            migrate(self.root)
        self.assertEqual([], list((self.root / "sources").glob("**/*.md")))
        self.assertTrue((legacy / "one.md").exists())
        self.assertTrue((legacy / "two.md").exists())

    def test_noncanonical_and_mismatched_youtube_urls_are_rejected(self):
        self.write({"canonical_url": "https://youtu.be/abc123?t=3"})
        self.assertIn("canonical_url is not canonical", self.errors())
        self.temp.cleanup(); self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.write({"canonical_url": "https://www.youtube.com/watch?v=wrong"})
        self.assertIn("does not match stable_id", self.errors())

    def test_incomplete_transcript_is_rejected(self):
        self.write(body="# x\n\n0:00 only beginning\n")
        self.assertIn("transcript incomplete", self.errors())

    def test_irrelevant_source_is_logged_but_not_counted(self):
        self.write()
        self.write({"stable_id": "reject1", "title": "Restaurant Ad", "canonical_url": "https://www.youtube.com/watch?v=reject1", "status": "rejected", "relevance_status": "irrelevant", "rejection_reason": "off topic"}, body="# Restaurant ad\n\n0:00 unrelated\n0:50 finish\n")
        stats = generate(self.root)
        self.assertEqual(2, stats["discovered_sources"])
        self.assertEqual(1, stats["validated_relevant_sources"])
        self.assertEqual(1, stats["rejected_sources"])
        self.assertIn("reject1", (self.root / "metadata/rejected-sources.csv").read_text())


if __name__ == "__main__":
    unittest.main()
