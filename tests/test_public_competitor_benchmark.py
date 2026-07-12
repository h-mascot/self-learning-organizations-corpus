import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_public_competitor_benchmark import PATH, validate


class PublicCompetitorBenchmarkTests(unittest.TestCase):
    def test_canonical_benchmark_validates(self):
        self.assertEqual([], validate())

    def test_validator_rejects_inflation_and_largest_claim(self):
        data = json.loads(PATH.read_text())
        data["largest_claim"]["permitted"] = True
        data["collections"][0]["strict_like_for_like_organization_evidence_count"] = data["collections"][0]["raw_count"] + 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("largest claim must remain false", errors)
        self.assertIn("0 <= strict <= raw", errors)

    def test_every_zero_strict_count_has_method_and_exclusions(self):
        data = json.loads(PATH.read_text())
        zeros = [r for r in data["collections"] if r["strict_like_for_like_organization_evidence_count"] == 0]
        self.assertTrue(zeros)
        for row in zeros:
            self.assertTrue(row["strict_count_method"].strip())
            self.assertTrue(row["exclusions"])

    def test_scope_only_counts_are_unknown_not_zero(self):
        data = json.loads(PATH.read_text())
        scoped = [r for r in data["collections"] if r["audit"]["coverage"] == "scope_only"]
        self.assertTrue(scoped)
        self.assertTrue(all(r["strict_like_for_like_organization_evidence_count"] is None for r in scoped))

    def test_validator_rejects_scope_only_numeric_zero(self):
        data = json.loads(PATH.read_text())
        scoped = next(r for r in data["collections"] if r["audit"]["coverage"] == "scope_only")
        scoped["strict_like_for_like_organization_evidence_count"] = 0
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("scope_only audit requires unknown null strict count", errors)

    def test_validator_handles_malformed_raw_count_without_crashing(self):
        data = json.loads(PATH.read_text())
        data["collections"][0]["raw_count"] = "805"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("raw_count must be a non-negative integer", errors)

    def test_validator_handles_malformed_retrieval_evidence_without_crashing(self):
        data = json.loads(PATH.read_text())
        data["collections"][0]["retrieval_evidence"] = "not-a-list"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("retrieval_evidence must be a non-empty list", errors)

    def test_validator_recomputes_strict_count_from_audit(self):
        data = json.loads(PATH.read_text())
        audited = next(r for r in data["collections"] if r["audit"]["coverage"] == "complete")
        audited["strict_like_for_like_organization_evidence_count"] += 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("strict count must equal unique included audit organizations", errors)

    def test_validator_rejects_incomplete_complete_audit(self):
        data = json.loads(PATH.read_text())
        audited = next(r for r in data["collections"] if r["audit"]["coverage"] == "complete")
        audited["audit"]["rows"].pop()
        audited["audit"]["audited_unit_count"] -= 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("complete audit must cover raw_count units", errors)

    def test_validator_rejects_bad_urls_dates_and_scope_only_rows(self):
        data = json.loads(PATH.read_text())
        scoped = next(r for r in data["collections"] if r["audit"]["coverage"] == "scope_only")
        scoped["retrieval_evidence"][0]["url"] = "https:missing-host"
        scoped["retrieval_evidence"][0]["retrieved_at"] = "tomorrow-ish"
        scoped["audit"]["rows"] = [{"label":"x","url":"https:bad","decision":"exclude","reason":"x"}]
        scoped["audit"]["audited_unit_count"] = 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "benchmark.json"
            path.write_text(json.dumps(data))
            errors = "\n".join(validate(path))
        self.assertIn("url must be public https", errors)
        self.assertIn("retrieved_at must be an ISO date or datetime", errors)
        self.assertIn("scope_only audit cannot have rows", errors)


if __name__ == "__main__":
    unittest.main()
