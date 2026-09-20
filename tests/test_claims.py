import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "claims.json"
CATALOG = ROOT / "research" / "catalog.json"
VERSIONS = ROOT / "research" / "versions.json"


class ProtocolFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claims = json.loads(CLAIMS.read_text())
        cls.catalog = json.loads(CATALOG.read_text())
        cls.versions = json.loads(VERSIONS.read_text())

    def test_named_claims_exist(self):
        ids = {c["id"] for c in self.claims["claims"]}
        for required in ("E-S3", "E-QEC", "E-RL", "E-MZM", "E-TC", "E-FR", "E-HOL", "E-5", "S-L2", "S-Q"):
            self.assertIn(required, ids)

    def test_keep_claims_pass_rule(self):
        for c in self.claims["claims"]:
            if c["status"] != "KEEP":
                continue
            self.assertGreaterEqual(int(c["C"][1]), 3, c["id"])
            self.assertGreaterEqual(int(c["T"][1]), 2, c["id"])
            self.assertGreaterEqual(int(c["D"][1]), 2, c["id"])

    def test_q1000_is_not_an_output(self):
        sq = next(c for c in self.claims["claims"] if c["id"] == "S-Q")
        self.assertEqual(sq["status"], "CUT")

    def test_holography_cut_from_engine(self):
        hol = next(c for c in self.claims["claims"] if c["id"] == "E-HOL")
        self.assertEqual(hol["status"], "CUT")

    def test_heuristic_is_not_c(self):
        note = (self.catalog.get("protocol") or {}).get("note", "")
        lowered = note.lower()
        self.assertIn("harvest metadata", lowered)
        self.assertTrue("c/t/d/a" in lowered or "cannot raise c" in lowered)

    def test_version_lines_exist(self):
        self.assertTrue(self.versions["current"]["DBE"].startswith("DBE-"))
        self.assertTrue(self.versions["current"]["DBES"].startswith("DBES-"))


if __name__ == "__main__":
    unittest.main()
