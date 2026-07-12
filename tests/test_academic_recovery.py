from __future__ import annotations

import unittest

from scripts.academic_recovery import arxiv_id, canonical_url, deduplicate, reconstruct_abstract, relevance, source_type


class AcademicRecoveryTests(unittest.TestCase):
    def work(self, **overrides):
        result = {
            "id": "https://openalex.org/W1", "doi": "https://doi.org/10.1/example",
            "title": "Organizational learning and innovation in firms", "type": "article",
            "ids": {"openalex": "https://openalex.org/W1"},
            "primary_location": {"source": {"type": "journal"}, "landing_page_url": "https://doi.org/10.1/example"},
            "locations": [], "abstract_inverted_index": {"Firms": [0], "learn": [1]},
        }
        result.update(overrides)
        return result

    def test_abstract_reconstruction_uses_positions(self):
        self.assertEqual("Organizations learn continuously", reconstruct_abstract({"learn": [1], "continuously": [2], "Organizations": [0]}))

    def test_arxiv_requires_identifier_or_canonical_url(self):
        self.assertEqual("", arxiv_id(self.work()))
        work = self.work(ids={"openalex": "https://openalex.org/W1", "arxiv": "https://arxiv.org/abs/2401.12345"})
        self.assertEqual("2401.12345", arxiv_id(work))
        self.assertEqual("arxiv", source_type(work))
        self.assertEqual("https://arxiv.org/abs/2401.12345", canonical_url(work))

    def test_source_type_precedence(self):
        self.assertEqual("journal-article", source_type(self.work()))
        self.assertEqual("thesis", source_type(self.work(type="dissertation")))
        self.assertEqual("conference-paper", source_type(self.work(type="proceedings-article")))
        self.assertEqual("book-chapter", source_type(self.work(type="book-chapter")))
        self.assertEqual("repository-preprint", source_type(self.work(type="preprint")))

    def test_dedupe_uses_doi_url_and_normalized_title(self):
        first = self.work()
        second = self.work(id="https://openalex.org/W2", ids={"openalex": "https://openalex.org/W2"}, doi="https://doi.org/10.1/EXAMPLE")
        duplicates = deduplicate([first, second])
        self.assertEqual(1, len(duplicates))
        self.assertIn(next(iter(duplicates.values())), {"W1", "W2"})

    def test_relevance_requires_organizational_and_learning_signals(self):
        self.assertTrue(relevance(self.work(), "Firms build knowledge and improve innovation.")[0])
        irrelevant = self.work(title="On the Dangers of Stochastic Parrots")
        self.assertFalse(relevance(irrelevant, "Language models have environmental costs.")[0])


if __name__ == "__main__":
    unittest.main()
