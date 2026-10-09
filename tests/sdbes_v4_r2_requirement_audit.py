"""Second-pass audit that every mandatory V4 R2 layer is present and passing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sdbes.v4 as v4  # noqa: E402
from tests.sdbes_v1_v4_regression import run_regression  # noqa: E402
from tests.sdbes_v4_r2_core_logic_checks import run_checks  # noqa: E402


REQUIRED_SYMBOLS = {
    "LocalLinearization",
    "FiniteHorizonResponse",
    "IdentificationStatus",
    "DataIdentificationAssessment",
    "MechanisticDerivationAssessment",
    "ExpertAssumptionAssessment",
    "QuantitySpec",
    "ModelComposition",
    "CouplingInterface",
    "PredicateVariableBinding",
    "ResourceBalance",
    "ModelUseAuthorization",
    "ModelPropertyType",
    "ModelPropertyAssessment",
    "MultiFidelityModelFamily",
    "TransferAssessment",
    "InfluenceProjectionType",
    "NormalizationMethod",
    "InfluenceProjection",
    "UncertaintyType",
    "StabilityMethod",
    "StabilityAssessment",
    "ResearchTest",
    "DecisionRule",
    "MilestoneBinding",
    "FormalizationProfile",
    "FormalizationCoverage",
    "SimulationResult",
    "EvidenceObject",
    "finite_horizon_response",
    "validate_composition",
    "authorize_predicate",
    "apply_research_transition",
    "package_simulation_as_evidence",
}

REQUIRED_SCHEMA_OBJECTS = {
    "quantity_spec",
    "dynamic_model",
    "local_linearization",
    "finite_horizon_response",
    "data_identification_assessment",
    "mechanistic_derivation_assessment",
    "expert_assumption_assessment",
    "model_composition",
    "coupling_interface",
    "predicate_variable_binding",
    "resource_balance",
    "model_use_authorization",
    "model_property_assessment",
    "multi_fidelity_model_family",
    "transfer_assessment",
    "influence_projection",
    "stability_assessment",
    "physical_state_transition",
    "knowledge_state_transition",
    "research_test",
    "decision_rule",
    "milestone_binding",
    "formalization_profile",
    "simulation_result",
    "v2_evidence_wrapper",
}


def run_audit() -> dict:
    missing_symbols = sorted(name for name in REQUIRED_SYMBOLS if not hasattr(v4, name))

    schema_path = ROOT / "docs/SDBES/V4_R2_SCHEMA_TEMPLATE.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    missing_schema = sorted(REQUIRED_SCHEMA_OBJECTS - set(schema))

    fixture = json.loads(
        (ROOT / "docs/SDBES/tests/V1_V4_R2_EXISTING_CASES.json").read_text(
            encoding="utf-8"
        )
    )
    core = run_checks()
    regression = run_regression()
    spec = (
        ROOT / "docs/SDBES/V4_R2_CAUSAL_DYNAMICS_MODEL_COMPOSITION.md"
    ).read_text(encoding="utf-8")
    invariant_markers = (
        "Simulation result",
        "Component validity",
        "Research acceleration",
        "Low-fidelity success",
        "Transfer",
    )

    checks = {
        "all_required_symbols_present": not missing_symbols,
        "all_required_schema_objects_present": not missing_schema,
        "core_checks_pass": bool(core) and set(core.values()) == {"PASS"},
        "regression_release_gate_pass": regression["release_gate"] == "PASS",
        "regression_case_count_15": regression["case_count"] == 15,
        "no_new_papers_added": fixture["new_papers_added"] is False,
        "hard_invariants_present": all(marker in spec for marker in invariant_markers),
        "v2_wrapper_blocks_direct_updates": (
            schema["v2_evidence_wrapper"]["claim_updates_applied"] is False
            and schema["v2_evidence_wrapper"]["assessment_required"] is True
        ),
    }
    return {
        "checks": checks,
        "missing_symbols": missing_symbols,
        "missing_schema_objects": missing_schema,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


if __name__ == "__main__":
    report = run_audit()
    print(json.dumps(report, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)
