import json, unittest
from scripts.generate_organization_index import ROOT, VOCABULARY, build

class OrganizationIndexTests(unittest.TestCase):
    def test_valid_exact_mechanisms_and_exclusions(self):
        dashboard, markdown, errors = build(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(tuple(dashboard["by_mechanism"]), VOCABULARY)
        self.assertTrue(all(dashboard["by_mechanism"].values()))
        self.assertGreaterEqual(dashboard["sampled_exclusion_count"], 10)
        self.assertIn("Generic evaluation toolkit", markdown)

    def test_generated_files_are_deterministic(self):
        dashboard, markdown, errors = build(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(json.loads((ROOT/"metadata/organization-index.json").read_text()), dashboard)
        self.assertEqual((ROOT/"research/company-index.md").read_text(), markdown)

    def test_generic_sources_are_not_promoted(self):
        manifest = json.loads((ROOT/"research/organization-evidence.json").read_text())
        evidence = {x["source_id"] for x in manifest["evidence"]}
        generic = {x["source_id"] for x in manifest["exclusions"]}
        self.assertTrue(generic.isdisjoint(evidence))
        self.assertTrue(any(x.startswith("github-") for x in generic))
