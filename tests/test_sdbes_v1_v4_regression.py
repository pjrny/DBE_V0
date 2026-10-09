"""Pytest adapter for the frozen V1→V4 R2 regression suite."""

from tests.sdbes_v1_v4_regression import run_regression


def test_existing_cases_have_no_unexpected_regressions():
    report = run_regression()
    assert report["case_count"] == 15
    assert report["unexpected_regressions"] == 0
    assert report["release_gate"] == "PASS"
