"""SDBES V4 R2 executable reference semantics.

This module is intentionally a small, dependency-free reference engine.  It
does not attempt to replace a domain simulator.  It enforces the contracts
that let SDBES call, compose, and interpret domain models without converting a
simulation into empirical evidence or silently satisfying a V3 prerequisite.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isclose
from typing import Any, Callable, Iterable, Mapping, Sequence


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]
Dimension = tuple[int, int, int, int, int, int, int]
DIMENSIONLESS: Dimension = (0, 0, 0, 0, 0, 0, 0)


class ModelRole(str, Enum):
    ENDOGENOUS_STATE = "ENDOGENOUS_STATE"
    CONTROL_INPUT = "CONTROL_INPUT"
    EXOGENOUS_INPUT = "EXOGENOUS_INPUT"
    DISTURBANCE = "DISTURBANCE"
    PARAMETER = "PARAMETER"
    LATENT = "LATENT"
    OBSERVED = "OBSERVED"
    OUTCOME = "OUTCOME"
    RESOURCE_INTERFACE = "RESOURCE_INTERFACE"


class QuantityKind(str, Enum):
    STOCK = "STOCK"
    FLOW = "FLOW"
    RATE = "RATE"
    INTENSIVE = "INTENSIVE"
    EXTENSIVE = "EXTENSIVE"
    COUNT = "COUNT"
    PROBABILITY = "PROBABILITY"
    FRACTION = "FRACTION"
    INDEX = "INDEX"
    CATEGORICAL = "CATEGORICAL"
    BOOLEAN = "BOOLEAN"
    FIELD = "FIELD"
    DISTRIBUTION = "DISTRIBUTION"


class TemporalSupport(str, Enum):
    INSTANTANEOUS = "INSTANTANEOUS"
    INTERVAL_MEAN = "INTERVAL_MEAN"
    INTERVAL_TOTAL = "INTERVAL_TOTAL"
    CUMULATIVE = "CUMULATIVE"
    EVENT = "EVENT"


class PredicateKnowledgeStatus(str, Enum):
    NEITHER = "NEITHER"
    TRUE_ONLY = "TRUE_ONLY"
    FALSE_ONLY = "FALSE_ONLY"
    BOTH = "BOTH"


class ScenarioPolicy(str, Enum):
    STRICT = "STRICT"
    EXPLORATORY_WITH_ASSUMPTION = "EXPLORATORY_WITH_ASSUMPTION"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"


class ModelUseStatus(str, Enum):
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    SCENARIO_ONLY = "SCENARIO_ONLY"
    CONDITIONAL_INTERVENTION_USE = "CONDITIONAL_INTERVENTION_USE"
    CAUSAL_COMPARISON_ALLOWED = "CAUSAL_COMPARISON_ALLOWED"
    VALIDATED_PREDICTIVE_USE = "VALIDATED_PREDICTIVE_USE"


class IdentificationStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    PARTIALLY_IDENTIFIED = "PARTIALLY_IDENTIFIED"
    NOT_IDENTIFIED = "NOT_IDENTIFIED"
    ASSUMPTION_DEPENDENT = "ASSUMPTION_DEPENDENT"


class ModelPropertyType(str, Enum):
    STATE_OBSERVABILITY = "STATE_OBSERVABILITY"
    STRUCTURAL_IDENTIFIABILITY = "STRUCTURAL_IDENTIFIABILITY"
    PRACTICAL_IDENTIFIABILITY = "PRACTICAL_IDENTIFIABILITY"
    INTERVENTION_CONTROLLABILITY = "INTERVENTION_CONTROLLABILITY"
    REACHABILITY = "REACHABILITY"


class TransferStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED = "UNSUPPORTED"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    UNKNOWN = "UNKNOWN"


class InfluenceProjectionType(str, Enum):
    DIRECT_LOCAL_STATE_SENSITIVITY = "DIRECT_LOCAL_STATE_SENSITIVITY"
    LOCAL_CONTROL_RESPONSE = "LOCAL_CONTROL_RESPONSE"
    ONE_STEP_EFFECT = "ONE_STEP_EFFECT"
    FINITE_HORIZON_TOTAL_EFFECT = "FINITE_HORIZON_TOTAL_EFFECT"
    IMPULSE_RESPONSE = "IMPULSE_RESPONSE"
    STEP_RESPONSE = "STEP_RESPONSE"
    CUMULATIVE_EFFECT = "CUMULATIVE_EFFECT"
    PATH_SPECIFIC_EFFECT = "PATH_SPECIFIC_EFFECT"
    PARAMETER_SENSITIVITY = "PARAMETER_SENSITIVITY"
    OBSERVATION_RESPONSE = "OBSERVATION_RESPONSE"


class NormalizationMethod(str, Enum):
    UNNORMALIZED_WITH_UNITS = "UNNORMALIZED_WITH_UNITS"
    CHARACTERISTIC_SCALE = "CHARACTERISTIC_SCALE"
    ELASTICITY = "ELASTICITY"
    STANDARD_DEVIATION = "STANDARD_DEVIATION"
    SCENARIO_RANGE = "SCENARIO_RANGE"
    THRESHOLD_RELATIVE = "THRESHOLD_RELATIVE"


class UncertaintyType(str, Enum):
    INITIAL_CONDITION_UNCERTAINTY = "INITIAL_CONDITION_UNCERTAINTY"
    OBSERVATION_UNCERTAINTY = "OBSERVATION_UNCERTAINTY"
    PARAMETER_EPISTEMIC_UNCERTAINTY = "PARAMETER_EPISTEMIC_UNCERTAINTY"
    PROCESS_VARIABILITY = "PROCESS_VARIABILITY"
    MODEL_FORM_UNCERTAINTY = "MODEL_FORM_UNCERTAINTY"
    CAUSAL_IDENTIFICATION_UNCERTAINTY = "CAUSAL_IDENTIFICATION_UNCERTAINTY"
    SCENARIO_OR_EXOGENOUS_UNCERTAINTY = "SCENARIO_OR_EXOGENOUS_UNCERTAINTY"
    NUMERICAL_OR_DISCRETIZATION_ERROR = "NUMERICAL_OR_DISCRETIZATION_ERROR"
    COMPOSITION_OR_COUPLING_UNCERTAINTY = "COMPOSITION_OR_COUPLING_UNCERTAINTY"
    TRANSFER_UNCERTAINTY = "TRANSFER_UNCERTAINTY"


class StabilityMethod(str, Enum):
    FIXED_POINT_EIGENVALUES = "FIXED_POINT_EIGENVALUES"
    PERIODIC_ORBIT_FLOQUET_MULTIPLIERS = "PERIODIC_ORBIT_FLOQUET_MULTIPLIERS"
    FINITE_HORIZON_GAIN = "FINITE_HORIZON_GAIN"
    PSEUDOSPECTRAL_OR_NONNORMAL_ANALYSIS = "PSEUDOSPECTRAL_OR_NONNORMAL_ANALYSIS"
    LYAPUNOV_ANALYSIS = "LYAPUNOV_ANALYSIS"
    HYBRID_SYSTEM_ANALYSIS = "HYBRID_SYSTEM_ANALYSIS"
    DELAY_SYSTEM_ANALYSIS = "DELAY_SYSTEM_ANALYSIS"


class ResourceBalanceType(str, Enum):
    CONSERVATION_BALANCE = "CONSERVATION_BALANCE"
    EXERGY_BALANCE = "EXERGY_BALANCE"
    INVENTORY_BALANCE = "INVENTORY_BALANCE"
    CAPACITY_OR_THROUGHPUT_ACCOUNTING = "CAPACITY_OR_THROUGHPUT_ACCOUNTING"
    ECONOMIC_ACCOUNTING = "ECONOMIC_ACCOUNTING"
    ENVIRONMENTAL_IMPACT_ACCOUNTING = "ENVIRONMENTAL_IMPACT_ACCOUNTING"


class FormalizationCoverage(str, Enum):
    NO_FORMALIZATION = "NO_FORMALIZATION"
    STATEMENT_ENCODED = "STATEMENT_ENCODED"
    SUPPORTING_LEMMA_ONLY = "SUPPORTING_LEMMA_ONLY"
    MAIN_RESULT_PARTIAL = "MAIN_RESULT_PARTIAL"
    MAIN_RESULT_FULL = "MAIN_RESULT_FULL"
    COMPARATOR_VERIFIED = "COMPARATOR_VERIFIED"


class DecisionOutcome(str, Enum):
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    KILL = "KILL"


class RegressionClassification(str, Enum):
    UNCHANGED = "UNCHANGED"
    EXPECTED_REFINEMENT = "EXPECTED_REFINEMENT"
    SCHEMA_ONLY_CHANGE = "SCHEMA_ONLY_CHANGE"
    UNEXPECTED_REGRESSION = "UNEXPECTED_REGRESSION"


@dataclass(frozen=True)
class QuantitySpec:
    variable_id: str
    roles: frozenset[ModelRole]
    kind: QuantityKind
    unit: str
    dimension: Dimension
    temporal_support: TemporalSupport
    timebase_seconds: float | None = None
    spatial_support: str | None = None
    valid_range: tuple[float, float] | None = None
    semantic_concept: str | None = None

    def __post_init__(self) -> None:
        if not self.roles:
            raise ValueError("a variable requires at least one model role")
        if len(self.dimension) != 7:
            raise ValueError("SI dimension vectors must contain seven exponents")
        if self.timebase_seconds is not None and self.timebase_seconds <= 0:
            raise ValueError("timebase_seconds must be positive")
        if self.valid_range and self.valid_range[0] > self.valid_range[1]:
            raise ValueError("valid_range lower bound exceeds upper bound")


@dataclass(frozen=True)
class LocalLinearization:
    model_id: str
    A: Matrix
    B: Matrix
    E: Matrix
    G: Matrix
    H: Matrix
    D: Matrix
    baseline_state: Vector
    baseline_input: Vector
    baseline_disturbance: Vector
    parameter_point: Vector
    time: float
    numerical_method: str
    validity_radius: float | None = None
    uncertainty: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        n = len(self.baseline_state)
        _require_shape(self.A, n, n, "A")
        _require_shape(self.B, n, len(self.baseline_input), "B")
        _require_shape(self.E, n, len(self.baseline_disturbance), "E")
        _require_shape(self.G, n, len(self.parameter_point), "G")
        if self.H and _matrix_cols(self.H) != n:
            raise ValueError("H must map state to observations")
        if self.D and len(self.D) != len(self.H):
            raise ValueError("D and H must produce the same observation dimension")
        if self.D and _matrix_cols(self.D) != len(self.baseline_input):
            raise ValueError("D must map control input to observations")


@dataclass(frozen=True)
class DataIdentificationAssessment:
    claim_id: str
    estimand: str
    intervention: str
    comparator: str
    population: str
    identification_status: IdentificationStatus
    confounders: tuple[str, ...] = ()
    adjustment_set: tuple[str, ...] = ()
    randomization_status: str | None = None
    positivity_assumption: str | None = None
    consistency_assumption: str | None = None
    selection_assumptions: tuple[str, ...] = ()
    estimator: str | None = None
    diagnostics: tuple[str, ...] = ()
    uncertainty: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MechanisticDerivationAssessment:
    governing_equations: tuple[str, ...]
    conservation_laws: tuple[str, ...]
    boundary_conditions: tuple[str, ...]
    approximation_regime: tuple[str, ...]
    constitutive_relations: tuple[str, ...] = ()
    parameter_sources: tuple[str, ...] = ()
    numerical_verification: tuple[str, ...] = ()
    calibration: tuple[str, ...] = ()
    validation_domain: Mapping[str, Any] = field(default_factory=dict)
    known_failures: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExpertAssumptionAssessment:
    assumption: str
    rationale: str
    source: str
    plausible_range: Any
    affected_outputs: tuple[str, ...]
    sensitivity: Any
    falsifier: str


@dataclass(frozen=True)
class FiniteHorizonResponse:
    state_transition: Matrix
    state_delta: Vector
    observation_delta: Vector | None
    horizon: int
    assumptions: tuple[str, ...] = ()


@dataclass(frozen=True)
class CouplingInterface:
    source_model: str
    source_variable: QuantitySpec
    target_model: str
    target_variable: QuantitySpec
    transformation: str | None = None
    unit_conversion: str | None = None
    temporal_conversion: str | None = None
    spatial_aggregation: str | None = None
    interpolation_or_hold: str | None = None
    synchronization_interval_seconds: float | None = None
    uncertainty_transfer: str | None = None
    resource_boundary_owner: str | None = None
    double_counting_check: bool = False
    causal_direction: str | None = None
    interface_validity_domain: Mapping[str, tuple[float, float]] = field(
        default_factory=dict
    )
    interface_confidence: str | None = None
    failure_behavior: str | None = None
    semantic_compatibility_asserted: bool = False


@dataclass(frozen=True)
class ComponentModel:
    model_id: str
    validity_domain: Mapping[str, tuple[float, float]] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelComposition:
    component_models: tuple[ComponentModel, ...]
    coupling_interfaces: tuple[CouplingInterface, ...]
    execution_order: tuple[str, ...]
    synchronization_policy: str
    initialization_policy: str
    algebraic_loop_policy: str
    composition_tests: tuple[str, ...] = ()
    composition_status: str | None = None


@dataclass(frozen=True)
class PredicateAuthorization:
    allowed: bool
    satisfies_gate: bool = False
    assumption_required: bool = False
    conflict_warning: bool = False
    reason: str = ""


@dataclass(frozen=True)
class PredicateVariableBinding:
    predicate_id: str
    variable_ids: tuple[str, ...]
    evaluation_expression: str
    units: tuple[str, ...]
    scope: Mapping[str, Any]
    context_requirements: Mapping[str, Any]
    threshold: Any
    uncertainty_rule: str


@dataclass(frozen=True)
class ModelUseAuthorization:
    model_id: str
    intended_use: str
    status: ModelUseStatus
    permitted_queries: frozenset[str]
    prohibited_queries: frozenset[str]
    required_validation: tuple[str, ...] = ()
    required_uncertainty_assessments: tuple[str, ...] = ()
    required_structural_predicates: tuple[str, ...] = ()
    version: str = "1"
    scope: Mapping[str, Any] = field(default_factory=dict)
    acceptance_authority: str | None = None
    valid_time: str | None = None

    def authorize(self, query: str, satisfied_predicates: Iterable[str] = ()) -> bool:
        if query in self.prohibited_queries or query not in self.permitted_queries:
            return False
        return set(self.required_structural_predicates).issubset(satisfied_predicates)


@dataclass(frozen=True)
class ModelPropertyAssessment:
    model_id: str
    assessment_type: ModelPropertyType
    method: str
    scope: Mapping[str, Any]
    result: Any
    uncertainty: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TransferAssessment:
    source_scope: str
    target_scope: str
    preserved_invariants: tuple[str, ...]
    changed_conditions: tuple[str, ...]
    domain_overlap: str
    transport_assumptions: tuple[str, ...]
    transfer_evidence: tuple[str, ...]
    status: TransferStatus
    uncertainty: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FidelityLevel:
    model_id: str
    rank: int


@dataclass(frozen=True)
class PromotionRule:
    source_model_id: str
    target_model_id: str
    required_criteria: frozenset[str]


@dataclass(frozen=True)
class MultiFidelityModelFamily:
    family_id: str
    levels: tuple[FidelityLevel, ...]
    promotion_rules: tuple[PromotionRule, ...]
    fidelity_dimensions: tuple[str, ...] = ()
    shared_variables: tuple[str, ...] = ()
    discrepancy_models: tuple[str, ...] = ()
    validation_data: tuple[str, ...] = ()
    transfer_rules: tuple[str, ...] = ()

    def can_promote(
        self, source_model_id: str, target_model_id: str, satisfied_criteria: Iterable[str]
    ) -> bool:
        source = _find_level(self.levels, source_model_id)
        target = _find_level(self.levels, target_model_id)
        if target.rank <= source.rank:
            return True
        rule = next(
            (
                item
                for item in self.promotion_rules
                if item.source_model_id == source_model_id
                and item.target_model_id == target_model_id
            ),
            None,
        )
        return bool(rule and rule.required_criteria.issubset(satisfied_criteria))


@dataclass(frozen=True)
class ResourceBalance:
    balance_type: ResourceBalanceType
    boundary: str
    stocks: Mapping[str, float] = field(default_factory=dict)
    inflows: Mapping[str, float] = field(default_factory=dict)
    outflows: Mapping[str, float] = field(default_factory=dict)
    internal_conversion_terms: Mapping[str, float] = field(default_factory=dict)
    sources: Mapping[str, float] = field(default_factory=dict)
    sinks: Mapping[str, float] = field(default_factory=dict)
    destruction_terms: Mapping[str, float] = field(default_factory=dict)
    storage_change: float = 0.0
    uncertainty: float = 0.0
    reference_environment: str | None = None

    def residual(self) -> float:
        return (
            sum(self.inflows.values())
            + sum(self.sources.values())
            - sum(self.outflows.values())
            - sum(self.sinks.values())
            - sum(self.destruction_terms.values())
            - self.storage_change
        )

    def validates(self, tolerance: float = 1e-9) -> bool:
        if self.balance_type == ResourceBalanceType.EXERGY_BALANCE:
            if not self.reference_environment:
                return False
        if self.balance_type not in {
            ResourceBalanceType.CONSERVATION_BALANCE,
            ResourceBalanceType.EXERGY_BALANCE,
            ResourceBalanceType.INVENTORY_BALANCE,
        }:
            return True
        return abs(self.residual()) <= tolerance + abs(self.uncertainty)


@dataclass(frozen=True)
class InfluenceProjection:
    projection_type: InfluenceProjectionType
    baseline_state_or_trajectory: Any
    source: str
    target: str
    intervention_or_perturbation: Any
    outcome: str
    horizon: Any
    units: str
    normalization_method: NormalizationMethod
    uncertainty: Mapping[str, Any]
    calculation_method: str
    validity_domain: Mapping[str, Any]
    normalization_scales: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class StabilityAssessment:
    method: StabilityMethod
    operating_point_or_trajectory: Any
    scope: Mapping[str, Any]
    stability_metric: str
    result: Any
    uncertainty: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResearchTest:
    test_id: str
    target_claims: tuple[str, ...]
    target_predicates: tuple[str, ...]
    competing_hypotheses: tuple[str, ...]
    required_fidelity: str
    pass_condition: Callable[[Mapping[str, Any]], bool]
    partial_condition: Callable[[Mapping[str, Any]], bool]
    fail_condition: Callable[[Mapping[str, Any]], bool]
    kill_condition: Callable[[Mapping[str, Any]], bool]
    method: str | None = None
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    resources: tuple[str, ...] = ()
    duration: str | None = None
    expected_discrimination: str | None = None
    evidence_object_template: Mapping[str, Any] = field(default_factory=dict)

    def evaluate(self, result: Mapping[str, Any]) -> DecisionOutcome:
        if self.kill_condition(result):
            return DecisionOutcome.KILL
        if self.pass_condition(result):
            return DecisionOutcome.PASS
        if self.partial_condition(result):
            return DecisionOutcome.PARTIAL
        if self.fail_condition(result):
            return DecisionOutcome.FAIL
        return DecisionOutcome.INCONCLUSIVE


@dataclass(frozen=True)
class DecisionRule:
    target: str
    actions: Mapping[DecisionOutcome, str]

    def action_for(self, outcome: DecisionOutcome) -> str:
        return self.actions[outcome]


@dataclass(frozen=True)
class MilestoneBinding:
    milestone_id: str
    required_claims: frozenset[str]
    required_predicates: frozenset[str]
    required_tests: frozenset[str]
    blockers: frozenset[str] = frozenset()
    unlocks: frozenset[str] = frozenset()

    def is_complete(
        self,
        claims: Iterable[str],
        predicates: Iterable[str],
        tests: Iterable[str],
        active_blockers: Iterable[str] = (),
    ) -> bool:
        return (
            self.required_claims.issubset(claims)
            and self.required_predicates.issubset(predicates)
            and self.required_tests.issubset(tests)
            and not self.blockers.intersection(active_blockers)
        )


@dataclass(frozen=True)
class SimulationResult:
    result_id: str
    model_versions: tuple[str, ...]
    input_snapshot: Mapping[str, Any]
    structural_predicate_snapshot: Mapping[str, str]
    scenario: Mapping[str, Any]
    baseline: Mapping[str, Any]
    intervention: Mapping[str, Any]
    outputs: Mapping[str, Any]
    uncertainty: Mapping[str, Any]
    validity_domain: Mapping[str, Any]
    resource_balances: tuple[ResourceBalance, ...]
    unresolved_assumptions: tuple[str, ...]
    sensitivity_summary: Mapping[str, Any]
    authorization_id: str
    reproducibility_record: Mapping[str, Any]


@dataclass(frozen=True)
class FormalizationProfile:
    claim_id: str
    claim_version: str
    formal_statement: str
    assumptions: tuple[str, ...]
    proof_artifacts: tuple[str, ...]
    checker: str | None
    checker_version: str | None
    theorem_names: tuple[str, ...]
    coverage_level: FormalizationCoverage
    scope_note: str
    known_gaps: tuple[str, ...]
    dependent_claim_ids: tuple[str, ...]
    verification_run: str | None


@dataclass(frozen=True)
class EvidenceObject:
    evidence_id: str
    evidence_type: str
    source_result_id: str
    claim_updates_applied: bool
    assessment_required: bool
    payload: Mapping[str, Any]


def package_simulation_as_evidence(result: SimulationResult) -> EvidenceObject:
    """Return a V2 input; never mutate claim or predicate state in V4."""

    return EvidenceObject(
        evidence_id=f"evidence:{result.result_id}",
        evidence_type="SIMULATION_RESULT",
        source_result_id=result.result_id,
        claim_updates_applied=False,
        assessment_required=True,
        payload={
            "model_versions": result.model_versions,
            "outputs": result.outputs,
            "uncertainty": result.uncertainty,
            "validity_domain": result.validity_domain,
            "unresolved_assumptions": result.unresolved_assumptions,
            "authorization_id": result.authorization_id,
        },
    )


def validate_quantity_equation(terms: Sequence[QuantitySpec]) -> tuple[str, ...]:
    """Validate that additive terms have compatible dimensions/time semantics."""

    if not terms:
        return ("equation requires at least one term",)
    issues: list[str] = []
    reference = terms[0]
    for term in terms[1:]:
        if term.dimension != reference.dimension:
            issues.append(
                f"dimension mismatch: {reference.variable_id} vs {term.variable_id}"
            )
        if term.temporal_support != reference.temporal_support:
            issues.append(
                f"temporal support mismatch: {reference.variable_id} vs {term.variable_id}"
            )
        if (
            term.timebase_seconds is not None
            and reference.timebase_seconds is not None
            and not isclose(term.timebase_seconds, reference.timebase_seconds)
        ):
            issues.append(
                f"timebase mismatch: {reference.variable_id} vs {term.variable_id}"
            )
    return tuple(issues)


def validate_coupling(interface: CouplingInterface) -> tuple[str, ...]:
    issues: list[str] = []
    source = interface.source_variable
    target = interface.target_variable
    if source.dimension != target.dimension and not interface.transformation:
        issues.append("dimension mismatch without a declared transformation")
    if source.unit != target.unit and not interface.unit_conversion:
        issues.append("unit mismatch without a declared unit conversion")
    if source.temporal_support != target.temporal_support and not interface.temporal_conversion:
        issues.append("temporal-support mismatch without a declared conversion")
    if (
        source.timebase_seconds is not None
        and target.timebase_seconds is not None
        and not isclose(source.timebase_seconds, target.timebase_seconds)
        and not interface.temporal_conversion
    ):
        issues.append("timebase mismatch without a declared conversion")
    if source.spatial_support != target.spatial_support and not interface.spatial_aggregation:
        issues.append("spatial-support mismatch without declared aggregation")
    if not interface.semantic_compatibility_asserted:
        issues.append("semantic compatibility has not been asserted")
    if not interface.failure_behavior:
        issues.append("interface failure behavior is undefined")
    if ModelRole.RESOURCE_INTERFACE in source.roles or ModelRole.RESOURCE_INTERFACE in target.roles:
        if not interface.resource_boundary_owner:
            issues.append("resource boundary owner is undefined")
        if not interface.double_counting_check:
            issues.append("resource double-counting check has not passed")
    return tuple(issues)


def validate_composition(composition: ModelComposition) -> tuple[str, ...]:
    issues: list[str] = []
    ids = [model.model_id for model in composition.component_models]
    if len(set(ids)) != len(ids):
        issues.append("component model IDs must be unique")
    if set(composition.execution_order) != set(ids):
        issues.append("execution order must contain each component exactly once")
    for interface in composition.coupling_interfaces:
        if interface.source_model not in ids or interface.target_model not in ids:
            issues.append("coupling interface references an unknown component")
        issues.extend(
            f"{interface.source_model}->{interface.target_model}: {issue}"
            for issue in validate_coupling(interface)
        )
    intersection = intersect_validity_domains(
        model.validity_domain for model in composition.component_models
    )
    if intersection is None:
        issues.append("component validity domains have an empty intersection")
    return tuple(issues)


def intersect_validity_domains(
    domains: Iterable[Mapping[str, tuple[float, float]]],
) -> dict[str, tuple[float, float]] | None:
    result: dict[str, tuple[float, float]] = {}
    for domain in domains:
        for variable, (low, high) in domain.items():
            if variable in result:
                low = max(low, result[variable][0])
                high = min(high, result[variable][1])
            if low > high:
                return None
            result[variable] = (low, high)
    return result


def authorize_predicate(
    status: PredicateKnowledgeStatus, policy: ScenarioPolicy
) -> PredicateAuthorization:
    if policy == ScenarioPolicy.DIAGNOSTIC_ONLY:
        return PredicateAuthorization(
            True, satisfies_gate=False, reason="diagnostic evaluation cannot satisfy a gate"
        )
    if status == PredicateKnowledgeStatus.TRUE_ONLY:
        return PredicateAuthorization(
            True,
            satisfies_gate=True,
            reason="qualifying support without qualifying refutation",
        )
    if status == PredicateKnowledgeStatus.FALSE_ONLY:
        return PredicateAuthorization(False, reason="predicate is structurally blocked")
    if status == PredicateKnowledgeStatus.NEITHER:
        if policy == ScenarioPolicy.EXPLORATORY_WITH_ASSUMPTION:
            return PredicateAuthorization(
                True,
                satisfies_gate=True,
                assumption_required=True,
                reason="unresolved predicate exposed as assumption",
            )
        return PredicateAuthorization(False, reason="strict evaluation blocks unresolved predicate")
    if policy == ScenarioPolicy.EXPLORATORY_WITH_ASSUMPTION:
        return PredicateAuthorization(
            True,
            satisfies_gate=True,
            assumption_required=True,
            conflict_warning=True,
            reason="conflicted predicate exposed as an assumption and warning",
        )
    return PredicateAuthorization(False, conflict_warning=True, reason="strict evaluation blocks conflict")


def transfer_authorized(assessment: TransferAssessment, strict: bool = True) -> bool:
    if strict:
        return assessment.status == TransferStatus.SUPPORTED
    return assessment.status in {TransferStatus.SUPPORTED, TransferStatus.PARTIAL}


def ordered_state_transition(a_sequence: Sequence[Matrix]) -> Matrix:
    if not a_sequence:
        raise ValueError("at least one state matrix is required")
    n = len(a_sequence[0])
    transition = identity(n)
    for index, matrix in enumerate(a_sequence):
        _require_shape(matrix, n, n, f"A[{index}]")
        transition = matmul(matrix, transition)
    return transition


def finite_horizon_response(
    linearizations: Sequence[LocalLinearization],
    initial_state_delta: Sequence[float],
    control_deltas: Sequence[Sequence[float]],
    disturbance_deltas: Sequence[Sequence[float]] | None = None,
    parameter_deltas: Sequence[Sequence[float]] | None = None,
) -> FiniteHorizonResponse:
    if not linearizations:
        raise ValueError("at least one linearization is required")
    if len(control_deltas) != len(linearizations):
        raise ValueError("one control perturbation is required per time step")
    disturbance_deltas = disturbance_deltas or [
        (0.0,) * len(item.baseline_disturbance) for item in linearizations
    ]
    parameter_deltas = parameter_deltas or [
        (0.0,) * len(item.parameter_point) for item in linearizations
    ]
    if len(disturbance_deltas) != len(linearizations):
        raise ValueError("one disturbance perturbation is required per time step")
    if len(parameter_deltas) != len(linearizations):
        raise ValueError("one parameter perturbation is required per time step")

    state = tuple(float(value) for value in initial_state_delta)
    for item, du, dz, dtheta in zip(
        linearizations, control_deltas, disturbance_deltas, parameter_deltas
    ):
        state = vecadd(
            matvec(item.A, state),
            matvec(item.B, du),
            matvec(item.E, dz),
            matvec(item.G, dtheta),
        )
    final = linearizations[-1]
    observation = (
        vecadd(matvec(final.H, state), matvec(final.D, control_deltas[-1]))
        if final.H
        else None
    )
    return FiniteHorizonResponse(
        state_transition=ordered_state_transition([item.A for item in linearizations]),
        state_delta=state,
        observation_delta=observation,
        horizon=len(linearizations),
        assumptions=("first-order local linearization",),
    )


def classify_regression(
    prior_conclusion: str,
    r2_conclusion: str,
    *,
    scientific_detail_added: bool = False,
    schema_only: bool = False,
) -> RegressionClassification:
    if prior_conclusion != r2_conclusion:
        return RegressionClassification.UNEXPECTED_REGRESSION
    if scientific_detail_added:
        return RegressionClassification.EXPECTED_REFINEMENT
    if schema_only:
        return RegressionClassification.SCHEMA_ONLY_CHANGE
    return RegressionClassification.UNCHANGED


def apply_research_transition(
    knowledge_state: Mapping[str, Any],
    physical_state: Mapping[str, Any],
    knowledge_updates: Mapping[str, Any],
    physical_updates: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Research actions update K; X changes only through an explicit physical channel."""

    if physical_updates:
        raise ValueError("a research transition cannot directly update physical state X(t)")
    next_knowledge = dict(knowledge_state)
    next_knowledge.update(knowledge_updates)
    return next_knowledge, dict(physical_state)


def identity(size: int) -> Matrix:
    return tuple(
        tuple(1.0 if row == column else 0.0 for column in range(size))
        for row in range(size)
    )


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or _matrix_cols(left) != len(right):
        raise ValueError("matrix dimensions do not close")
    return tuple(
        tuple(
            sum(left[row][k] * right[k][column] for k in range(len(right)))
            for column in range(_matrix_cols(right))
        )
        for row in range(len(left))
    )


def matvec(matrix: Matrix, vector: Sequence[float]) -> Vector:
    if not matrix:
        return ()
    if _matrix_cols(matrix) != len(vector):
        raise ValueError("matrix/vector dimensions do not close")
    return tuple(
        sum(value * vector[column] for column, value in enumerate(row))
        for row in matrix
    )


def vecadd(*vectors: Sequence[float]) -> Vector:
    if not vectors:
        return ()
    size = len(vectors[0])
    if any(len(vector) != size for vector in vectors):
        raise ValueError("vector dimensions do not close")
    return tuple(sum(vector[index] for vector in vectors) for index in range(size))


def _matrix_cols(matrix: Matrix) -> int:
    if not matrix:
        return 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("ragged matrices are not supported")
    return columns


def _require_shape(matrix: Matrix, rows: int, columns: int, name: str) -> None:
    if len(matrix) != rows or (rows and _matrix_cols(matrix) != columns):
        raise ValueError(f"{name} must have shape {rows}x{columns}")


def _find_level(levels: Sequence[FidelityLevel], model_id: str) -> FidelityLevel:
    level = next((item for item in levels if item.model_id == model_id), None)
    if level is None:
        raise ValueError(f"unknown fidelity model: {model_id}")
    return level


__all__ = [name for name in globals() if not name.startswith("_")]
