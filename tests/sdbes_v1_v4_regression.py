"""Run the previously used SDBES cases through the V1→V4 R2 contracts."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sdbes.v4 import (  # noqa: E402
    ComponentModel,
    CouplingInterface,
    ModelComposition,
    ModelRole,
    PredicateKnowledgeStatus,
    QuantityKind,
    QuantitySpec,
    RegressionClassification,
    ScenarioPolicy,
    TemporalSupport,
    apply_research_transition,
    authorize_predicate,
    classify_regression,
    validate_composition,
    validate_quantity_equation,
)

FIXTURE = ROOT / "docs/SDBES/tests/V1_V4_R2_EXISTING_CASES.json"
POWER = (1, 2, -3, 0, 0, 0, 0)


def _power(variable_id: str, timebase: float = 1.0) -> QuantitySpec:
    return QuantitySpec(
        variable_id=variable_id,
        roles=frozenset({ModelRole.RESOURCE_INTERFACE}),
        kind=QuantityKind.RATE,
        unit="W",
        dimension=POWER,
        temporal_support=TemporalSupport.INTERVAL_MEAN,
        timebase_seconds=timebase,
        spatial_support="plant boundary",
        semantic_concept="plant power",
    )


def _contract_check(case: dict) -> None:
    case_id = case["id"]
    if case_id == "M2_INTERNAL_BURN_CONTROL":
        obs = case["observations"]
        assert obs["headline_success_rate_upper_bound"] <= 0.05
        assert obs["model_fidelity"].startswith("0-D")
        assert {"profiles", "MHD", "disruption physics"}.issubset(obs["omissions"])
    elif case_id == "BUS_B_OFFLINE_COMPUTE":
        knowledge, physical = apply_research_transition(
            {"design_search": 0}, {"fusion_gain": 1.0}, {"design_search": 1}
        )
        assert knowledge["design_search"] == 1
        assert physical["fusion_gain"] == 1.0
    elif case_id == "S_L2_BARRIER_EVASION":
        assert "2x thermal" in case["kill_condition"]
        unresolved = authorize_predicate(
            PredicateKnowledgeStatus.NEITHER,
            ScenarioPolicy.EXPLORATORY_WITH_ASSUMPTION,
        )
        assert unresolved.allowed and unresolved.assumption_required
    elif case_id == "Q_ENG_1000":
        terms = [_power(name) for name in case["required_terms"]]
        assert validate_quantity_equation(terms) == ()
        assert len(terms) == 7
    elif case_id == "COMPONENT_COUPLING":
        source = _power("source", 1.0)
        target = _power("target", 60.0)
        incomplete = CouplingInterface(
            source_model="a",
            source_variable=source,
            target_model="b",
            target_variable=target,
        )
        composition = ModelComposition(
            component_models=(ComponentModel("a"), ComponentModel("b")),
            coupling_interfaces=(incomplete,),
            execution_order=("a", "b"),
            synchronization_policy="unspecified",
            initialization_policy="snapshot",
            algebraic_loop_policy="reject",
        )
        assert validate_composition(composition)
    elif case_id in {"C02", "I07", "E04"}:
        # These cases depend on preserving model/formal scope rather than
        # automatically treating it as physical validation.
        assert "cannot" in case["v4_contract"] or "not authorized" in case["v4_contract"]
    elif case_id == "I01":
        assert "cross-device transfer remains PARTIAL" in case["v4_contract"]
    elif case_id in {"I02", "I04", "N01", "C09", "I03", "E03"}:
        assert case["v4_contract"]
    else:
        raise AssertionError(f"unhandled regression case: {case_id}")


def run_regression() -> dict:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in data["cases"]:
        _contract_check(case)
        classification = classify_regression(
            case["prior_conclusion"],
            case["r2_conclusion"],
            scientific_detail_added=case["scientific_detail_added"],
            schema_only=case["schema_only"],
        )
        assert classification.value == case["expected_classification"]
        results.append(
            {
                "id": case["id"],
                "prior": case["prior_conclusion"],
                "r2": case["r2_conclusion"],
                "classification": classification.value,
            }
        )

    counts = Counter(item["classification"] for item in results)
    unexpected = counts[RegressionClassification.UNEXPECTED_REGRESSION.value]
    return {
        "snapshot_date": data["snapshot_date"],
        "case_count": len(results),
        "counts": dict(sorted(counts.items())),
        "unexpected_regressions": unexpected,
        "release_gate": "PASS" if unexpected == 0 else "FAIL",
        "results": results,
    }


if __name__ == "__main__":
    report = run_regression()
    print(json.dumps(report, indent=2))
    if report["release_gate"] != "PASS":
        raise SystemExit(1)
