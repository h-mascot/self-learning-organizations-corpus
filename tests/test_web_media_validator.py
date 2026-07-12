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

    def test_filename_slug_is_human_readable_and_bounded(self):
        self.assertEqual("a-learning-organization", MODULE.slug("A Learning Organization"))
        self.assertLessEqual(len(MODULE.slug("x" * 200)), 80)

    def test_navigation_boilerplate_is_detected(self):
        self.assertRegex("Skip to content and log in", MODULE.BOILERPLATE)

    def test_podcast_sponsor_boilerplate_is_detected(self):
        failures = [
            "This episode is brought to you by Eppo, a next-generation A/B testing platform.",
            "This episode is brought to you by Datadog, now home to Eppo.",
            "Companies like Twitch rely on Eppo to power their experiments.",
        ]
        for failure in failures:
            with self.subTest(failure=failure):
                self.assertTrue(MODULE.is_podcast_ad(failure))

    def test_podcast_requires_separated_substantive_spans(self):
        evidence = [
            {"kind": "transcript_excerpt", "locator": "transcript", "text": "Guest (00:20:00): We review failed launches and feed the findings into the next product experiment."},
            {"kind": "transcript_excerpt", "locator": "transcript", "text": "Guest (00:20:25): That evaluation changes the rubric used by every product team."},
        ]
        self.assertFalse(MODULE.has_separated_podcast_spans(evidence))
        evidence[1]["text"] = "Guest (01:02:00): The organization stores those decisions so new teams learn why the policy changed."
        self.assertTrue(MODULE.has_separated_podcast_spans(evidence))

    def test_generic_repository_boilerplate_is_not_a_mechanism(self):
        failures = [
            "XWiki Platform is a generic wiki platform offering runtime services for applications.",
            "Examples and guides for using the OpenAI API.",
            "An all-in-one developer platform for building successful products.",
        ]
        for failure in failures:
            with self.subTest(failure=failure):
                self.assertFalse(MODULE.has_explicit_organizational_mechanism(failure))

    def test_current_corpus_passes_strict_validation(self):
        errors, counts, artifacts = MODULE.validate()
        self.assertEqual([], errors)
        self.assertTrue(all(counts[lane] >= quota for lane, quota in MODULE.LANES.items()))
        self.assertEqual(30, artifacts[("podcasts", "metadata_only")])


if __name__ == "__main__":
    unittest.main()
