import tempfile
import unittest
from pathlib import Path

from scripts.social_acquisition import RECORDS
from scripts.validate_social_lane import QUOTAS, validate


class SocialLaneTests(unittest.TestCase):
    def test_seed_meets_quotas_and_has_unique_urls(self):
        urls = [row[1] for row in RECORDS]
        self.assertEqual(len(urls), len(set(urls)))
        for platform, quota in QUOTAS.items():
            self.assertGreaterEqual(sum(row[0] == platform for row in RECORDS), quota)

    def test_checked_in_lane_validates(self):
        counts, errors = validate()
        self.assertEqual({"x": 50, "reddit": 25, "substack": 25}, counts)
        self.assertEqual([], errors)

    def test_missing_quota_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            counts, errors = validate(Path(tmp))
        self.assertEqual({"x": 0, "reddit": 0, "substack": 0}, counts)
        self.assertEqual(3, len(errors))


if __name__ == "__main__":
    unittest.main()

