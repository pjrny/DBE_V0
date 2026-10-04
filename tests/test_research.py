import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research" / "catalog.json"
SCORE = ROOT / "research" / "score.py"


def _load_score():
    spec = importlib.util.spec_from_file_location("dbe_research_score", SCORE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

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


class ScoreVenueTests(unittest.TestCase):
    """score.py venue gate: bare arXiv never passes A5 or raises C, whatever the case."""

    ARXIV_SPELLINGS = ("arXiv", "ARXIV", "arxiv", "  arXiv ", "arXiv preprint", "Preprint")

    @classmethod
    def setUpClass(cls):
        cls.score = _load_score()

    def test_bare_arxiv_any_case_is_preprint(self):
        for venue in self.ARXIV_SPELLINGS:
            with self.subTest(venue=venue):
                self.assertTrue(self.score.is_bare_preprint(venue))
                self.assertEqual(self.score.normalize_venue(venue).split()[0], venue.split()[0].lower())

    def test_bare_arxiv_include_is_queued_not_auto_merged(self):
        for venue in self.ARXIV_SPELLINGS:
            for status in ("KEEP", "HOLD"):
                with self.subTest(venue=venue, status=status):
                    r = self.score.route("INCLUDE", status, venue)
                    self.assertFalse(r["a5"])
                    self.assertFalse(r["auto"])
                    self.assertEqual(r["route"], "QUEUE")

    def test_bare_arxiv_never_raises_c(self):
        for venue in self.ARXIV_SPELLINGS:
            with self.subTest(venue=venue):
                r = self.score.route("STRENGTHEN", "KEEP", venue)
                self.assertFalse(r["a5"])
                self.assertFalse(r["canRaiseC"])
                self.assertNotEqual(r["route"], "AUTO-MERGED PATCH")

    def test_journal_venue_still_patches(self):
        for venue in ("nature", "Nature", " Phys. Rev. X "):
            with self.subTest(venue=venue):
                r = self.score.route("INCLUDE", "KEEP", venue)
                self.assertTrue(r["a5"])
                self.assertEqual(r["route"], "AUTO-MERGED PATCH")

    def test_cli_arxiv_include_does_not_print_auto_merge(self):
        for venue in ("arXiv", "ARXIV", "arxiv"):
            with self.subTest(venue=venue):
                out = subprocess.run(
                    [sys.executable, str(SCORE), "--bind", "E-S3", "--action", "INCLUDE",
                     "--paper", "test-paper", "--venue", venue],
                    capture_output=True, text=True, check=True,
                ).stdout
                self.assertNotIn("AUTO-MERGED PATCH", out)
                self.assertIn("ROUTE QUEUE", out)
                self.assertIn("A5 FAIL", out)


if __name__ == "__main__":
    unittest.main()
