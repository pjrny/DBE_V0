"""Pytest adapter for the V4 R2 second-pass requirement audit."""

from tests.sdbes_v4_r2_requirement_audit import run_audit


def test_v4_r2_requirement_audit():
    report = run_audit()
    assert report["status"] == "PASS"
    assert all(report["checks"].values())
