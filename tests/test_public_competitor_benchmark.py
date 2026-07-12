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


if __name__ == "__main__":
    unittest.main()
