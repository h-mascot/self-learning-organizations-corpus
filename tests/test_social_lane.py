import shutil
import tempfile
import unittest
import re
from pathlib import Path

from scripts.validate_social_lane import QUOTAS, validate

ROOT = Path(__file__).resolve().parents[1]


class SocialLaneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / "sources" / "x", self.root / "sources" / "x")
        shutil.copytree(ROOT / "sources" / "reddit", self.root / "sources" / "reddit")
        shutil.copytree(ROOT / "sources" / "substack", self.root / "sources" / "substack")

    def tearDown(self):
        self.tmp.cleanup()

    def errors(self):
        return validate(self.root)[1]

    def mutate_newsletter(self, old, new):
        path = next((self.root / "sources" / "substack" / "accepted").glob("*.md"))
        path.write_text(path.read_text().replace(old, new), encoding="utf-8")

    def test_checked_in_lane_validates(self):
        counts, errors = validate()
        self.assertEqual(QUOTAS, counts)
        self.assertEqual([], errors)

    def test_homepage_only_newsletter_fails(self):
        self.mutate_newsletter("/p/", "/")
        self.assertTrue(any("not an individual /p/ article" in e for e in self.errors()))

    def test_generic_provenance_fails(self):
        self.mutate_newsletter(
            "Jina Reader direct fetch of the canonical individual article",
            "public search index bounded excerpt",
        )
        self.assertTrue(any("generic or unrecognized provenance" in e for e in self.errors()))

    def test_invalid_newsletter_domain_fails(self):
        path = next((self.root / "sources" / "substack" / "accepted").glob("*.md"))
        text = path.read_text()
        host = re.search(r"^canonical_url: https://([^/]+)", text, re.M).group(1)
        path.write_text(text.replace(host, "typo-invalid.example"), encoding="utf-8")
        self.assertTrue(any("domain is not in the retrieved allow-list" in e for e in self.errors()))

    def test_duplicate_resource_fails(self):
        source = next((self.root / "sources" / "reddit" / "accepted").glob("*.md"))
        shutil.copy2(source, source.with_name("duplicate--" + source.name))
        errors = self.errors()
        self.assertTrue(any("duplicate canonical resource" in e for e in errors))
        self.assertTrue(any("duplicate stable ID" in e for e in errors))

    def test_non_source_excerpt_fails(self):
        self.mutate_newsletter(
            "## Verified source excerpt\n\n",
            "## Verified source excerpt\n\nNewsletter analysis of AI and organizations.\n\n",
        )
        self.assertTrue(any("non-source/generic excerpt" in e for e in self.errors()))

    def test_missing_quota_fails(self):
        shutil.rmtree(self.root / "sources")
        counts, errors = validate(self.root)
        self.assertEqual({"x": 0, "reddit": 0, "substack": 0}, counts)
        self.assertEqual(3, len(errors))


if __name__ == "__main__":
    unittest.main()
