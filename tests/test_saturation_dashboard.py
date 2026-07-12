import unittest

from scripts.generate_saturation_dashboard import ROOT, build


class SaturationDashboardTests(unittest.TestCase):
    def test_canonical_cross_wave_qualification_is_honest(self):
        data, markdown, errors = build(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(data["unsaturated_channels"], [])
        self.assertIn("academic", data["channels"])
        self.assertTrue(data["channels"]["academic"]["saturated"])
        self.assertIn("post-acceptance", data["academic_status"])
        self.assertIn("Academic: **met**", markdown)

    def test_every_claim_has_three_distinct_consecutive_qualifying_rounds(self):
        data, _, _ = build(ROOT)
        for channel in data["saturated_channels"]:
            proof = data["channels"][channel]["qualifying_rounds"]
            self.assertEqual(len(proof), 3)
            self.assertEqual([row["round"] for row in proof], [1, 2, 3])
            self.assertEqual(len({row["query_family"] for row in proof}), 3)
            self.assertTrue(all(row["candidate_count"] > 0 for row in proof))
            self.assertTrue(all(row["novelty_rate"] < data["threshold"] for row in proof))
            self.assertTrue(all(row["blocked"] == 0 for row in proof))

    def test_all_historical_and_wave_four_inputs_are_included(self):
        data, _, _ = build(ROOT)
        self.assertEqual(data["input_waves"], [
            "initial-saturation", "web-media-followup", "native-saturation-3",
            "web-media-saturation-4", "academic-saturation-5", "academic-saturation-6", "native-saturation-4",
        ])
