from __future__ import annotations

import hashlib
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
