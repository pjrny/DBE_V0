# SDBES V4 R2 — Causal Dynamics, Model Composition, Simulation Credibility & Research Intervention

**Project:** SDBES — Search for Dimensions Beyond Energy Scarcity

**Repository/branch:** `pjrny/DBE_V0` / `SDBES`

**Revision:** V4 R2

**Status:** Implemented reference semantics and acceptance tests

**Builds on:** V1 Typed Ledger; V2 Claim Evaluation; V3 Structural Semantics

## 0. Purpose and boundary

V4 turns the evidence and structural knowledge established in V1–V3 into
bounded simulations, interventions, model compositions, scenario comparisons,
and explicit research tests. It provides typed interfaces around domain models;
it does not replace those models.

\[
\boxed{\text{Preserve information first. Aggregate second. Simulate last.}}
\]

V4 may produce trajectories, intervention contrasts, sensitivities, resource
balances, model discrepancies, and research-test recommendations. It may not
directly raise claim confidence, convert theory into empirical support, convert
proof into physical validation, satisfy an unresolved V3 predicate, upgrade a
pillar or milestone, or infer causation because a simulated edge exists.

Every V4 result returns to V2 as a new Evidence Object requiring assessment.

## 1. Canonical dynamic models

Discrete time and observation models are:

\[
x_{k+1}=F_k(x_k,u_k,z_k;\theta,m),\qquad
y_k=h_k(x_k,u_k;\phi)+\nu_k.
\]

Continuous time is:

\[
\dot{x}=f(x,u,z,t;\theta,m).
\]

Here (x) is endogenous state, (u) is control/intervention, (z) is an
exogenous input or disturbance, \(\theta\) is a parameter vector, and (m) is
a model/regime choice. V4 records the form but does not force every external
solver into one representation.

## 2. Local and finite-horizon response

A single Jacobian cannot answer all response questions. V4 separates:

\[
A_k=\partial F_k/\partial x,\quad B_k=\partial F_k/\partial u,\quad
E_k=\partial F_k/\partial z,\quad G_k=\partial F_k/\partial\theta
\]

and:

\[
H_k=\partial h_k/\partial x,\qquad D_k=\partial h_k/\partial u.
\]

These are local sensitivities around a declared operating point, not permanent
edge signs or universal causal truths.

For a time-varying system:

\[
\Phi(k+n,k)=A_{k+n-1}A_{k+n-2}\cdots A_k.
\]

Only for a declared time-invariant or locally frozen system may this become
(A^n). The reference engine multiplies matrices in time order and separately
applies (B,E,G,H,D).

## 3. Three causal-support classes

V4 never collapses these classes:

1. `DataIdentificationAssessment` records the estimand, intervention,
   comparator, population, confounders, adjustment set, randomization,
   positivity, consistency, selection assumptions, estimator, diagnostics,
   uncertainty, and an identification status.
2. `MechanisticDerivationAssessment` records equations, conservation laws,
   boundary conditions, approximations, constitutive relations, parameter
   sources, verification, calibration, validation domain, and failures.
3. `ExpertAssumptionAssessment` records a visible scenario assumption, source,
   plausible range, affected outputs, sensitivity, and falsifier.

A mathematically valid mechanism is not automatically empirically validated.

## 4. Variable semantics and dimensional closure

Variable role and quantity kind are independent.

Roles include state, control, exogenous input, disturbance, parameter, latent,
observed, outcome, and resource interface. Quantity kinds include stock, flow,
rate, intensive, extensive, count, probability, fraction, index, categorical,
Boolean, field, and distribution.

Every quantitative variable also records unit, seven-component SI dimension
vector, temporal support, timebase, aggregation rule, spatial support, valid
range, and semantic concept.

Temporal support is `INSTANTANEOUS`, `INTERVAL_MEAN`, `INTERVAL_TOTAL`,
`CUMULATIVE`, or `EVENT`. Additive equations fail validation when dimensions,
temporal support, or timebases do not close.

## 5. Model composition and coupling

`ModelComposition` records component models, interfaces, execution order,
synchronization, initialization, algebraic-loop policy, validity-domain
intersection, composition tests, and status.

Every `CouplingInterface` declares source/target model and variable, semantic
compatibility, transformation, unit and temporal conversion, spatial
aggregation, interpolation/hold, synchronization, uncertainty transfer,
resource-boundary owner, double-counting check, causal direction, validity
domain, confidence, and failure behavior.

Sharing a unit is insufficient. Composition fails if an interface is invalid,
execution order is incomplete, or component validity domains do not overlap.

## 6. V3 structural binding

A V3 predicate constrains a simulation only through an executable
`PredicateVariableBinding` containing variables, expression, units, scope,
context, threshold, and uncertainty rule.

| V3 knowledge status | Strict | Exploratory | Diagnostic |
|---|---|---|---|
| `TRUE_ONLY` | allow | allow | allow |
| `FALSE_ONLY` | block | block | allow without satisfying gate |
| `NEITHER` | block | assumption required | allow |
| `BOTH` | block | assumption + conflict warning | allow |

An unresolved prerequisite never silently becomes true.

## 7. Typed resource accounting

V4 distinguishes conservation, exergy, inventory, capacity/throughput,
economic, and environmental-impact accounting. Mass, charge, and energy use
conservation. Exergy requires a reference environment and destruction terms.
Tritium and critical materials use inventory balances. Compute, beam time, and
manufacturing use capacity accounting. Costs are not conservation laws.

Each cross-model resource has a declared boundary and owner so it cannot be
counted twice.

## 8. Model-use authorization and model properties

`ModelUseAuthorization` records intended use, scope, permitted/prohibited
queries, required validation and uncertainty work, required V3 predicates,
accepting authority, version, and valid time.

Statuses are `DESCRIPTIVE_ONLY`, `SCENARIO_ONLY`,
`CONDITIONAL_INTERVENTION_USE`, `CAUSAL_COMPARISON_ALLOWED`, and
`VALIDATED_PREDICTIVE_USE`. A model may hold different authorizations for
different uses.

Separate property assessments cover observability, structural/practical
identifiability, intervention controllability, and reachability. A numerically
executable model can still be scientifically unusable for an intervention.

## 9. Multi-fidelity families and transfer

`MultiFidelityModelFamily` records levels, fidelity dimensions, promotion
criteria, shared variables, discrepancy models, validation data, and transfer
rules. A result at (L_i) does not inherit validation at (L_{i+1}).

`TransferAssessment` records source/target scope, preserved invariants, changed
conditions, domain overlap, assumptions, evidence, uncertainty, and one of:
`SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `OUT_OF_DOMAIN`, or `UNKNOWN`.

Strict transferred use requires `SUPPORTED`. Exploratory use may admit
`PARTIAL` with visible limitations.

## 10. Influence projections and normalization

A visual edge must correspond to a defined query: local state sensitivity,
control response, one-step or finite-horizon effect, impulse/step response,
cumulative or path-specific effect, parameter sensitivity, or observation
response.

Every projection records baseline, source, target, perturbation, outcome,
horizon, units, normalization, uncertainty, calculation, and validity domain.
No edge has a permanent sign: feedback and horizon may change it.

Normalization may be unnormalized units, characteristic scale, elasticity,
standard deviation, scenario range, or threshold-relative. The method and
scales remain visible.

## 11. Uncertainty and stability

V4 distinguishes initial-condition, observation, parameter-epistemic,
process, model-form, causal-identification, scenario/exogenous,
numerical/discretization, composition/coupling, and transfer uncertainty.
Representation may use distributions, intervals, sets, ensembles, or
alternative model families.

Stability methods include fixed-point eigenvalues, Floquet multipliers,
finite-horizon gain, non-normal/pseudospectral analysis, Lyapunov, hybrid, and
delay-system analysis. \(\rho(A)<1\) and \(\Re(\lambda_i)<0\) are local
fixed-point conditions, not universal stability claims.

## 12. Physical state and knowledge state

V4 preserves:

\[
X_{t+1}=F_X(X_t,U_t,Z_t;\theta)
\]

for physical/technical evolution and:

\[
K_{t+1}=F_K(K_t,A_t,Y_t;\psi)
\]

for research/knowledge evolution. A research tool can strongly change (K(t))
without changing (X(t)). A research action cannot mutate physical state
without an explicit validated intervention channel.

## 13. Research tests, decisions, and milestones

Every recommendation becomes a `ResearchTest` with target claims/predicates,
competing hypotheses, method, fidelity, inputs, outputs, resources, duration,
discrimination, pass/partial/fail/kill conditions, and Evidence Object
template.

A `DecisionRule` binds every result class to an action. A `MilestoneBinding`
specifies required claims, predicates, tests, completion expression, blockers,
and unlocks. The valid transition is:

    simulation/experiment → Evidence Object → V2 assessment
    → justified claim update → V3 predicate reassessment
    → milestone expression → route change

## 14. Formalization profile

Formal artifacts record the scoped statement, assumptions, proof artifacts,
checker/version, theorem names, coverage, gaps, dependencies, and verification
run. Formal verification may improve Formal evidence. It does not automatically
improve empirical, applied, causal-identification, or transfer evidence.

## 15. Simulation output contract

Every result records model versions, input and predicate snapshots, scenario,
baseline, intervention, outputs, uncertainty, validity domain, resource
balances, unresolved assumptions, sensitivities, authorization, and a
reproducibility record.

Its V2 wrapper must state:

    evidence_type: SIMULATION_RESULT
    claim_updates_applied: false
    assessment_required: true

## 16. Hard invariants

\[
\text{Simulation result}\neq\text{empirical validation}
\]
\[
\text{Formal proof}\neq\text{physical truth}
\]
\[
\text{Model fit}\neq\text{causal identification}
\]
\[
\text{Component validity}\neq\text{composition validity}
\]
\[
\text{Local sensitivity}\neq\text{long-horizon total effect}
\]
\[
\text{Research acceleration}\neq\text{physical-system improvement}
\]
\[
\text{Low-fidelity success}\neq\text{high-fidelity success}
\]
\[
\text{Transfer}\neq\text{inheritance}
\]

## 17. Acceptance criteria and implementation

R2 is blocked unless executable tests establish correct (A/B/E/G/H/D)
routing, ordered propagation, role/kind separation, unit/time closure,
composition validation, V3 predicate policies, fidelity promotion, transfer,
use authorization, typed balances, return to V2, (K/X) separation,
pass/partial/fail/kill behavior, and milestone gating.

Reference artifacts:

    sdbes/v4.py
    docs/SDBES/V4_R2_SCHEMA_TEMPLATE.json
    tests/sdbes_v4_r2_core_logic_checks.py
    tests/test_sdbes_v4_r2.py

V4 is the first layer allowed to ask, “What happens under an intervention?”
V5 will sit across V1–V4 as the human visualization and research-priority layer.
