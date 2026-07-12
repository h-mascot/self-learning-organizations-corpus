import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_web_media", ROOT / "scripts/validate_web_media.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class WebMediaValidatorTests(unittest.TestCase):
    def test_evidence_hash_is_canonical(self):
        evidence = [{"text": "feedback", "locator": "page", "kind": "excerpt"}]
        reordered = [{"kind": "excerpt", "locator": "page", "text": "feedback"}]
        self.assertEqual(MODULE.evidence_hash(evidence), MODULE.evidence_hash(reordered))

    def test_evidence_hash_matches_compact_sorted_json(self):
        evidence = [{"locator": "README", "text": "learning loop", "kind": "excerpt"}]
        expected = hashlib.sha256(
            json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(expected, MODULE.evidence_hash(evidence))

    def test_canonical_url_drops_tracking_and_normalizes_host(self):
        self.assertEqual(
            "https://example.com/path",
            MODULE.canonical_url("https://www.EXAMPLE.com/path/?utm_source=test"),
        )

    def test_canonical_url_preserves_identity_query(self):
        self.assertEqual(
            "https://youtube.com/watch?v=abc123",
            MODULE.canonical_url("https://www.youtube.com/watch?v=abc123&utm_source=test"),
        )


if __name__ == "__main__":
    unittest.main()
