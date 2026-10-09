"""Pytest adapter for the dependency-free V4 R2 acceptance checks."""

from tests.sdbes_v4_r2_core_logic_checks import run_checks


def test_v4_r2_core_logic():
    results = run_checks()
    assert results
    assert set(results.values()) == {"PASS"}
