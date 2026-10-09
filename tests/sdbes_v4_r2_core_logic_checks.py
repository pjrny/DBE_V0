"""Executable acceptance checks for SDBES V4 R2.

Run directly with:

    python tests/sdbes_v4_r2_core_logic_checks.py

The checks are dependency-free so the framework's core semantics can be
verified even before pytest is installed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sdbes.v4 import (
    ComponentModel,
    CouplingInterface,
    DecisionOutcome,
    DecisionRule,
    FidelityLevel,
    LocalLinearization,
    MilestoneBinding,
    ModelComposition,
    ModelRole,
    ModelUseAuthorization,
    ModelUseStatus,
    MultiFidelityModelFamily,
    PredicateKnowledgeStatus,
    PromotionRule,
    QuantityKind,
    QuantitySpec,
    ResearchTest,
    ResourceBalance,
    ResourceBalanceType,
    ScenarioPolicy,
    SimulationResult,
    TemporalSupport,
    TransferAssessment,
    TransferStatus,
    apply_research_transition,
    authorize_predicate,
    finite_horizon_response,
    package_simulation_as_evidence,
    transfer_authorized,
    validate_composition,
    validate_coupling,
    validate_quantity_equation,
)


POWER = (1, 2, -3, 0, 0, 0, 0)
ENERGY = (1, 2, -2, 0, 0, 0, 0)
TEMPERATURE = (0, 0, 0, 1, 0, 0, 0)


def quantity(
    variable_id,
    *,
    roles=(ModelRole.ENDOGENOUS_STATE,),
    kind=QuantityKind.RATE,
    unit="W",
    dimension=POWER,
    temporal_support=TemporalSupport.INSTANTANEOUS,
    timebase_seconds=1.0,
    spatial_support="whole-system",
    semantic_concept=None,
):
    return QuantitySpec(
        variable_id=variable_id,
        roles=frozenset(roles),
        kind=kind,
        unit=unit,
        dimension=dimension,
        temporal_support=temporal_support,
        timebase_seconds=timebase_seconds,
        spatial_support=spatial_support,
        semantic_concept=semantic_concept or variable_id,
    )


def valid_interface(source=None, target=None):
    return CouplingInterface(
        source_model="transport",
        source_variable=source or quantity("heat_flux"),
        target_model="wall",
        target_variable=target or quantity("incident_heat_flux"),
        uncertainty_transfer="interval propagation",
        causal_direction="transport->wall",
        semantic_compatibility_asserted=True,
        double_counting_check=True,
        resource_boundary_owner="wall",
        failure_behavior="block composition",
    )


def run_checks():
    results = {}

    # A/B/E/G/H/D are distinct and ordered propagation is time varying.
    step0 = LocalLinearization(
        model_id="m",
        A=((2.0,),),
        B=((3.0,),),
        E=((5.0,),),
        G=((7.0,),),
        H=((11.0,),),
        D=((13.0,),),
        baseline_state=(0.0,),
        baseline_input=(0.0,),
        baseline_disturbance=(0.0,),
        parameter_point=(0.0,),
        time=0.0,
        numerical_method="analytic",
    )
    step1 = LocalLinearization(
        model_id="m",
        A=((4.0,),),
        B=((0.0,),),
        E=((0.0,),),
        G=((0.0,),),
        H=((1.0,),),
        D=((0.0,),),
        baseline_state=(0.0,),
        baseline_input=(0.0,),
        baseline_disturbance=(0.0,),
        parameter_point=(0.0,),
        time=1.0,
        numerical_method="analytic",
    )
    response = finite_horizon_response(
        (step0, step1),
        initial_state_delta=(1.0,),
        control_deltas=((1.0,), (0.0,)),
        disturbance_deltas=((1.0,), (0.0,)),
        parameter_deltas=((1.0,), (0.0,)),
    )
    # First step: 2 + 3 + 5 + 7 = 17. Second step: 4 * 17 = 68.
    assert response.state_delta == (68.0,)
    assert response.state_transition == ((8.0,),)
    results["ordered_finite_horizon"] = "PASS"

    # Variable role and quantity kind are orthogonal.
    stored_energy = quantity(
        "stored_energy",
        roles=(ModelRole.ENDOGENOUS_STATE, ModelRole.OUTCOME),
        kind=QuantityKind.STOCK,
        unit="J",
        dimension=ENERGY,
    )
    assert ModelRole.OUTCOME in stored_energy.roles
    assert stored_energy.kind == QuantityKind.STOCK
    results["role_kind_independent"] = "PASS"

    # Units, dimensions, temporal support, and timebases must close.
    power = quantity("power")
    energy = quantity("energy", unit="J", dimension=ENERGY)
    interval_power = quantity(
        "interval_power", temporal_support=TemporalSupport.INTERVAL_MEAN
    )
    slow_power = quantity("slow_power", timebase_seconds=60.0)
    assert "dimension mismatch" in " ".join(validate_quantity_equation((power, energy)))
    assert "temporal support mismatch" in " ".join(
        validate_quantity_equation((power, interval_power))
    )
    assert "timebase mismatch" in " ".join(
        validate_quantity_equation((power, slow_power))
    )
    results["unit_timebase_closure"] = "PASS"

    # Composition rejects an unconverted interface and an empty domain overlap.
    temp_k = quantity(
        "temperature_limit",
        unit="K",
        dimension=TEMPERATURE,
        semantic_concept="material temperature limit",
    )
    temp_c = quantity(
        "operating_temperature",
        unit="degC",
        dimension=TEMPERATURE,
        timebase_seconds=60.0,
        semantic_concept="component operating temperature",
    )
    bad_interface = valid_interface(temp_k, temp_c)
    coupling_issues = validate_coupling(bad_interface)
    assert any("unit mismatch" in issue for issue in coupling_issues)
    assert any("timebase mismatch" in issue for issue in coupling_issues)
    bad_composition = ModelComposition(
        component_models=(
            ComponentModel("transport", {"T": (0.0, 10.0)}),
            ComponentModel("wall", {"T": (20.0, 30.0)}),
        ),
        coupling_interfaces=(bad_interface,),
        execution_order=("transport", "wall"),
        synchronization_policy="fixed step",
        initialization_policy="declared snapshot",
        algebraic_loop_policy="reject",
    )
    assert any("empty intersection" in issue for issue in validate_composition(bad_composition))
    good_composition = ModelComposition(
        component_models=(
            ComponentModel("transport", {"T": (0.0, 100.0)}),
            ComponentModel("wall", {"T": (20.0, 80.0)}),
        ),
        coupling_interfaces=(valid_interface(),),
        execution_order=("transport", "wall"),
        synchronization_policy="fixed step",
        initialization_policy="declared snapshot",
        algebraic_loop_policy="reject",
    )
    assert validate_composition(good_composition) == ()
    results["model_composition"] = "PASS"

    # V3 predicate binding policies preserve unknown and conflict.
    assert authorize_predicate(
        PredicateKnowledgeStatus.TRUE_ONLY, ScenarioPolicy.STRICT
    ).satisfies_gate
    assert not authorize_predicate(
        PredicateKnowledgeStatus.FALSE_ONLY, ScenarioPolicy.STRICT
    ).allowed
    unresolved = authorize_predicate(
        PredicateKnowledgeStatus.NEITHER, ScenarioPolicy.EXPLORATORY_WITH_ASSUMPTION
    )
    assert unresolved.allowed and unresolved.assumption_required
    conflict = authorize_predicate(
        PredicateKnowledgeStatus.BOTH, ScenarioPolicy.EXPLORATORY_WITH_ASSUMPTION
    )
    assert (
        conflict.allowed
        and conflict.satisfies_gate
        and conflict.assumption_required
        and conflict.conflict_warning
    )
    diagnostic = authorize_predicate(
        PredicateKnowledgeStatus.TRUE_ONLY, ScenarioPolicy.DIAGNOSTIC_ONLY
    )
    assert diagnostic.allowed and not diagnostic.satisfies_gate
    results["v3_predicate_binding"] = "PASS"

    # A lower-fidelity result cannot silently become a higher-fidelity result.
    family = MultiFidelityModelFamily(
        family_id="burn-control",
        levels=(FidelityLevel("0d", 0), FidelityLevel("1d", 1), FidelityLevel("machine", 2)),
        promotion_rules=(
            PromotionRule("0d", "1d", frozenset({"profile_validation"})),
            PromotionRule("1d", "machine", frozenset({"device_validation"})),
        ),
    )
    assert not family.can_promote("0d", "1d", ())
    assert family.can_promote("0d", "1d", ("profile_validation",))
    assert not family.can_promote("0d", "machine", ("profile_validation",))
    results["multi_fidelity_promotion"] = "PASS"

    # Transfer is explicit and strict use requires SUPPORTED.
    partial_transfer = TransferAssessment(
        source_scope="TCV",
        target_scope="DIII-D",
        preserved_invariants=("normalized beta",),
        changed_conditions=("geometry",),
        domain_overlap="partial",
        transport_assumptions=("similar control authority",),
        transfer_evidence=(),
        status=TransferStatus.PARTIAL,
    )
    assert not transfer_authorized(partial_transfer, strict=True)
    assert transfer_authorized(partial_transfer, strict=False)
    results["transfer_assessment"] = "PASS"

    # Validation is use-specific.
    authorization = ModelUseAuthorization(
        model_id="burn-0d",
        intended_use="controller comparison in simplified model",
        status=ModelUseStatus.SCENARIO_ONLY,
        permitted_queries=frozenset({"compare_controllers"}),
        prohibited_queries=frozenset({"predict_machine_success"}),
    )
    assert authorization.authorize("compare_controllers")
    assert not authorization.authorize("predict_machine_success")
    results["model_use_authorization"] = "PASS"

    # Conservation/inventory close; economics is accounting, not conservation.
    balance = ResourceBalance(
        balance_type=ResourceBalanceType.CONSERVATION_BALANCE,
        boundary="plant",
        inflows={"electricity": 10.0},
        outflows={"delivered": 7.0},
        sinks={"loss": 3.0},
    )
    assert balance.validates()
    assert not ResourceBalance(
        balance_type=ResourceBalanceType.CONSERVATION_BALANCE,
        boundary="plant",
        inflows={"electricity": 10.0},
        outflows={"delivered": 7.0},
    ).validates()
    assert ResourceBalance(
        balance_type=ResourceBalanceType.ECONOMIC_ACCOUNTING,
        boundary="project",
        inflows={"revenue": 10.0},
        outflows={"cost": 7.0},
    ).validates()
    results["typed_resource_balance"] = "PASS"

    # Simulation results return to V2 as unapplied evidence.
    simulation = SimulationResult(
        result_id="sim-1",
        model_versions=("burn-0d@1",),
        input_snapshot={},
        structural_predicate_snapshot={"burn_stable": "NEITHER"},
        scenario={},
        baseline={},
        intervention={},
        outputs={"success_rate": 0.05},
        uncertainty={},
        validity_domain={"model": "0-D"},
        resource_balances=(),
        unresolved_assumptions=("no profiles",),
        sensitivity_summary={"success_rate": "seed-sensitive"},
        authorization_id="auth-1",
        reproducibility_record={"seed": 1},
    )
    evidence = package_simulation_as_evidence(simulation)
    assert evidence.assessment_required
    assert not evidence.claim_updates_applied
    results["simulation_returns_to_v2"] = "PASS"

    # Research can change K(t), not X(t), without an explicit physical channel.
    knowledge, physical = apply_research_transition(
        {"uncertainty": 1.0}, {"fusion_gain": 1.0}, {"uncertainty": 0.5}
    )
    assert knowledge["uncertainty"] == 0.5
    assert physical["fusion_gain"] == 1.0
    try:
        apply_research_transition({}, {}, {}, {"fusion_gain": 2.0})
    except ValueError:
        pass
    else:
        raise AssertionError("research transition changed X(t) directly")
    results["knowledge_physical_separation"] = "PASS"

    # Research tests bind pass/partial/fail/kill to explicit decision rules.
    test = ResearchTest(
        test_id="s-l2",
        target_claims=("S-L2",),
        target_predicates=("net_enhancement_reachable",),
        competing_hypotheses=("enhancement", "no useful enhancement"),
        required_fidelity="finite-pulse + kinetic depletion",
        pass_condition=lambda r: r["net_ratio"] >= 2.0 and r["reachable"],
        partial_condition=lambda r: r["net_ratio"] >= 2.0 and not r["reachable"],
        fail_condition=lambda r: r["net_ratio"] < 2.0 and not r["reachable"],
        kill_condition=lambda r: r["net_ratio"] < 2.0 and r["reachable"],
    )
    assert test.evaluate({"net_ratio": 1.5, "reachable": True}) == DecisionOutcome.KILL
    rule = DecisionRule(
        target="S-L2",
        actions={
            DecisionOutcome.PASS: "advance",
            DecisionOutcome.PARTIAL: "hold",
            DecisionOutcome.FAIL: "revise",
            DecisionOutcome.INCONCLUSIVE: "repeat",
            DecisionOutcome.KILL: "remove from plant route",
        },
    )
    assert rule.action_for(DecisionOutcome.KILL) == "remove from plant route"
    results["decision_and_kill_test"] = "PASS"

    # Milestones cannot move from an unrelated simulation result.
    milestone = MilestoneBinding(
        milestone_id="M2",
        required_claims=frozenset({"E-RL-bounded"}),
        required_predicates=frozenset({"beats_lab_baseline"}),
        required_tests=frozenset({"machine_disruption_metric"}),
        blockers=frozenset({"unsafe_command_path"}),
    )
    assert not milestone.is_complete({"E-RL-bounded"}, set(), set())
    assert milestone.is_complete(
        {"E-RL-bounded"}, {"beats_lab_baseline"}, {"machine_disruption_metric"}
    )
    assert not milestone.is_complete(
        {"E-RL-bounded"},
        {"beats_lab_baseline"},
        {"machine_disruption_metric"},
        {"unsafe_command_path"},
    )
    results["milestone_binding"] = "PASS"

    return results


if __name__ == "__main__":
    for name, result in run_checks().items():
        print(f"{name}: {result}")
    print("ALL_V4_R2_CHECKS_PASSED")
