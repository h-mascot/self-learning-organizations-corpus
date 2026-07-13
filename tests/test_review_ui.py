from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "review-ui" / "review.py"
spec = importlib.util.spec_from_file_location("corpus_review", MODULE_PATH)
review = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(review)


class ReviewUITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = self.root / "review-ui" / "data"

    def tearDown(self):
        self.temp.cleanup()

    def write_json_resource(self, *, status="accepted", stable_id="blogs-one", artifact="metadata_only"):
        record = {
            "schema_version": 2,
            "platform": "blogs",
            "stable_id": stable_id,
            "title": "A learning loop in practice",
            "creator": "Ada Example",
            "publisher": "Example Org",
            "canonical_url": f"https://example.com/{stable_id}",
            "published_date": "2026-01-01",
            "date_precision": "day",
            "source_type": "article",
            "status": status,
            "artifact_level": artifact,
            "retrieved_at": "2026-01-02T00:00:00Z",
            "retrieval_method": "public page",
            "provenance": "publisher page",
            "rights_status": "bounded-public-evidence",
            "rights_note": "bounded excerpt",
            "content_sha256": "0" * 64,
            "relevance_evidence": ["Teams review outcomes and change the next decision."],
            "evidence": [{"kind": "excerpt", "locator": "body", "text": "A team captures failures, reviews evidence, records what it learned, and changes its operating process before the next decision."}],
            "query_ids": ["learning-loop"],
            "rejection_reason": "off topic" if status == "rejected" else None,
        }
        path = self.root / "sources" / "blogs" / status / f"{stable_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_indexes_real_corpus_at_documented_scale(self):
        corpus_root = Path(__file__).resolve().parents[1]
        resources = review.ResourceIndex(corpus_root).all()
        self.assertEqual(1053, len(resources))
        self.assertEqual(
            {"youtube", "academic", "x", "reddit", "substack", "blogs", "podcasts", "conferences", "books", "case-studies", "github"},
            {item["platform"] for item in resources},
        )
        self.assertTrue(all(item["source_url"].startswith("http") for item in resources))
        self.assertTrue(all(item["ada_category"] in {"works", "maybe", "doesnt_fit"} for item in resources))
        self.assertTrue(all(item["ada_reason"] for item in resources))

    def test_decisions_persist_and_feedback_is_exported(self):
        self.write_json_resource()
        resource = review.ResourceIndex(self.root).all()[0]
        store = review.DecisionStore(self.data)
        saved = store.save(resource, "accept", "Strong operating feedback loop.")
        self.assertEqual("accept", saved["decision"])

        reloaded = review.DecisionStore(self.data)
        self.assertEqual("accept", reloaded.get(resource["id"])["decision"])
        feedback = json.loads((self.data / "feedback.json").read_text())
        self.assertEqual(resource["id"], feedback["positive_similarity_seeds"][0]["resource_id"])
        self.assertEqual(1, feedback["category_preferences"]["platforms"]["blogs"]["accept"])
        self.assertEqual("positive", feedback["feedback_queue"][0]["polarity"])

    def test_reject_emits_negative_similarity_seed(self):
        self.write_json_resource(stable_id="blogs-negative")
        resource = review.ResourceIndex(self.root).all()[0]
        review.DecisionStore(self.data).save(resource, "reject", "No organizational mechanism.")
        feedback = json.loads((self.data / "feedback.json").read_text())
        self.assertEqual([], feedback["positive_similarity_seeds"])
        self.assertEqual(resource["id"], feedback["negative_similarity_seeds"][0]["resource_id"])

    def test_apply_defaults_to_dry_run_and_does_not_mutate_sources(self):
        path = self.write_json_resource(status="accepted", stable_id="blogs-reject-me")
        original = path.read_bytes()
        resource = review.ResourceIndex(self.root).all()[0]
        review.DecisionStore(self.data).save(resource, "reject", "Not a learning organization resource.")

        result = review.apply_decisions(self.root, self.data, yes=False)

        self.assertTrue(result["dry_run"])
        self.assertEqual(1, result["planned"])
        self.assertEqual(original, path.read_bytes())
        self.assertTrue(path.exists())
        self.assertIn("sources/blogs/rejected/", result["actions"][0]["destination"])

    def test_bulk_only_allows_safe_matches_to_ada_category(self):
        accepted_path = self.write_json_resource(status="accepted", stable_id="works", artifact="excerpt")
        rejected_path = self.write_json_resource(status="rejected", stable_id="no-fit", artifact="unavailable")
        resources = review.ResourceIndex(self.root).all()
        by_path = {item["path"]: item for item in resources}
        works = by_path[accepted_path.relative_to(self.root).as_posix()]
        no_fit = by_path[rejected_path.relative_to(self.root).as_posix()]
        store = review.DecisionStore(self.data)

        result = review.bulk_save(store, [works, no_fit], "accept", "Safe Ada bulk review")

        self.assertEqual([works["id"]], result["saved"])
        self.assertEqual([no_fit["id"]], result["skipped"])


if __name__ == "__main__":
    unittest.main()
