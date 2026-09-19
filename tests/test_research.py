import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research" / "catalog.json"

REQUIRED_FIELDS = {
    "anyons",
    "tqc",
    "majorana",
    "braid-knot",
    "topology",
    "fracton",
    "time-crystal",
    "plasma",
    "holography",
    "fusion-quantum",
}


class ResearchCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_has_papers_and_pillars(self):
        self.assertGreaterEqual(len(self.data["papers"]), 20)
        self.assertTrue(any(p["status"] == "established" for p in self.data["pillars"]))
        self.assertTrue(any(p["status"] == "suggested" for p in self.data["pillars"]))

    def test_every_program_field_is_tagged(self):
        seen = set()
        for paper in self.data["papers"]:
            seen.update(paper["fields"])
            self.assertTrue(paper["coreIdea"])
            self.assertTrue(paper["whyItMatters"])
            self.assertTrue(paper["limitation"])
            for key in ("importance", "confidence", "popularity"):
                self.assertGreaterEqual(paper[key], 0)
                self.assertLessEqual(paper[key], 100)
        self.assertTrue(REQUIRED_FIELDS.issubset(seen))

    def test_internal_sources_are_honest(self):
        internals = [p for p in self.data["papers"] if p.get("role") == "internal"]
        self.assertGreaterEqual(len(internals), 2)
        for paper in internals:
            self.assertLess(paper["confidence"], 70)


if __name__ == "__main__":
    unittest.main()
