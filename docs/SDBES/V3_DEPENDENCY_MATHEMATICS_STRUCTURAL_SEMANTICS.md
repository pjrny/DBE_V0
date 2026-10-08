# SDBES V3 — Dependency Mathematics & Structural Semantics

**Project:** SDBES — Search for Dimensions Beyond Energy Scarcity  
**Intended repository:** `pjrny/DBE_V0`  
**Intended branch:** `SDBES`  
**Recommended path:** `docs/SDBES/V3_DEPENDENCY_MATHEMATICS_STRUCTURAL_SEMANTICS.md`  
**Status:** Approved and committed following Pro review  
**Repository write performed after this review:** Yes — committed to `SDBES`  
**Builds on:** V1 Typed Evidence & Dependency Ledger; V2 Claim Evaluation Rules; V1/V2 10-Paper Stress Test

---

## 0. Review outcome

The conceptual V3 architecture is approved **with material refinements incorporated into this specification**.

The central direction survives:

- Claims remain epistemic objects.
- Capabilities and physical/technical conditions require a separate structural representation.
- Epistemic dependency and structural dependency remain separate layers.
- AND, OR, k-of-n and alternative-route semantics become first-class.
- Minimal path sets, minimal cut sets, dominators and strongly connected components remain structural diagnostics rather than truth scores.
- V3 remains noncausal and nondynamic; causal magnitude and time evolution belong to V4.

The review made nine principal corrections:

1. Replace the broad `Capability / Condition` object with a general **Structural Predicate** and explicit subtypes.
2. Add a **Structural Assessment** bridge so a paper claim never automatically sets a capability state.
3. Treat epistemic dependency as an **argument/inference graph**, not merely a matrix of pairwise arrows.
4. Separate **route-local requirements** from **global necessity**.
5. Use **four-valued knowledge status** to preserve conflicting evidence, while using three-valued logic for scenario evaluation.
6. Restrict minimal path/cut analysis to a declared monotone structural model and label all results as **model-relative**.
7. Use Boolean matrix algebra only for typed pairwise reachability; use gate-aware methods for AND/OR/k-of-n viability.
8. Give cycles explicit fixed-point and bootstrap semantics rather than simply collapsing them.
9. Make every derived pillar, bottleneck, path and cut result reproducible from a versioned graph snapshot.

---

# Part I — Purpose, scope and invariants

## 1. Purpose

V1 defines the typed research ledger.

V2 defines how scientific claims are specified and evaluated.

V3 defines:

> **What epistemically relies on what, what a modeled technological pathway structurally requires, and which conclusions may legitimately be derived from those dependency structures.**

V3 supports:

- claim decomposition,
- formal premise tracking,
- component-to-application translation,
- physical and engineering prerequisites,
- alternative pathways,
- joint prerequisites,
- model-relative necessity and sufficiency,
- circular dependency detection,
- bootstrap dependency analysis,
- structural bottleneck analysis,
- pillar diagnostics,
- and hierarchical visualization provenance.

V3 does **not** yet calculate causal effect sizes or future trajectories.

## 2. Non-goals

V3 must not calculate or imply:

- the probability that a claim is true unless V2 supplies a justified probability model;
- causal effect magnitude;
- progress rate or acceleration;
- time-dependent state propagation;
- energy, resource or economic flow;
- commercial success probability;
- Monte Carlo forecasts;
- differential-equation dynamics;
- graph diffusion;
- feedback-loop stability;
- or a universal scalar “importance” score.

Those belong to V4 or later versions.

## 3. V3 invariants

V3 inherits all V1/V2 invariants and adds the following:

\[
\text{Claim} \neq \text{Structural Predicate}
\]

\[
\text{Route-local Requirement} \neq \text{Global Necessity}
\]

\[
\text{Unresolved} \neq \text{Refuted}
\]

\[
\text{Conflict} \neq \text{Unknown}
\]

\[
\text{All Represented Routes Blocked} \neq \text{Physically Impossible}
\]

\[
\text{Pairwise Reachability} \neq \text{Gate Satisfaction}
\]

\[
\text{Structural Centrality} \neq \text{Scientific Truth}
\]

\[
\text{Derived Diagnostic} \neq \text{Intrinsic Node Property}
\]

---

# Part II — Mandatory V1/V2 amendments adopted by V3

The 10-paper stress test found no P0 failure, but it found six P1 schema gaps. V3 adopts the following amendments as normative prerequisites.

## 4. Structured F/E/A evidence-profile cells

A cell in the V1/V2 Formal–Empirical–Applied profile must not be stored as a single scalar or status.

Each cell is a structured record:

```json
{
  "applicability": "APPLICABLE | NOT_APPLICABLE | UNRESOLVED",
  "availability": "PRESENT | ABSENT | UNKNOWN",
  "outcome": "MEETS | DOES_NOT_MEET | INCONCLUSIVE | UNKNOWN",
  "verification_activities": [],
  "scope": {},
  "notes": null
}
```

These dimensions are independent:

- evidence can be present but inconclusive;
- replication can be applicable but unassessed;
- a test can be performed and fail;
- a method can be genuinely irrelevant.

A visualization may derive a compact glyph from these fields, but the ledger retains the complete record.

## 5. Verification provenance

Verification must be modeled as one or more activities, not as one ordinal badge.

Permitted activity types include:

```text
SOURCE_REPORTED
SOURCE_TEXT_SCREENED
SOURCE_METHODS_SCREENED
SDBES_DERIVATION_CHECKED
SDBES_CODE_EXECUTED
SDBES_NUMERICAL_RESULT_REPRODUCED
SDBES_DATA_REANALYZED
INDEPENDENT_REPLICATION_SCREENED
INDEPENDENT_REPLICATION_CONFIRMED
FORMALLY_MACHINE_CHECKED
```

Every activity records:

```text
activity_id
activity_type
performed_by
method
input_artifacts
output_artifacts
started_at
ended_at
outcome
limitations
ruleset_version
```

SDBES must never display “verified,” “replicated,” or “proved” without identifying the verification activity and actor.

## 6. Assessment-to-assessment provenance

Claim Assessments may have typed relations:

```text
SUPERSEDES
CORRECTS
CHALLENGES
NARROWS
BROADENS
REANALYZES
REPLICATES
FAILS_TO_REPLICATE
RETRACTS_SUPPORT_FOR
RESTORES_SUPPORT_FOR
```

A correction or critique applies only to linked claims and assessments. It does not automatically invalidate every result in a source document.

These relations should align, where practical, with W3C PROV concepts such as revision, derivation and invalidation while retaining SDBES-specific scientific semantics.

## 7. Demonstration context

A single Technology Readiness Level is too coarse for the epistemic ledger. Demonstration context is multi-axis:

```text
artifact_type:
  FORMAL_MODEL
  ANALYTIC_MODEL
  NUMERICAL_SIMULATION
  BENCH_EXPERIMENT
  COMPONENT_PROTOTYPE
  INTEGRATED_SUBSYSTEM
  FULL_SYSTEM
  OPERATIONAL_DEPLOYMENT

scale
operating_environment
duration_or_cycles
integration_scope
performance_metrics
resource_inputs
replication_context
failure_envelope
```

These fields are descriptive. They are not a probability of deployment or commercial success.

## 8. Formal-result subtypes

Formal and theoretical results may carry multiple descriptors:

```text
THEOREM
NO_GO_THEOREM
BOUND
MODEL_EXISTENCE_RESULT
CONSTRUCTIVE_PROTOCOL
ANALYTIC_APPROXIMATION
NUMERICAL_EVIDENCE
CONJECTURE
COUNTEREXAMPLE
```

## 9. Generalization status

Generalization is first-class rather than buried in prose:

```text
NOT_ASSESSED
SAME_SYSTEM_NEW_RUN
SAME_DEVICE_NEW_REGIME
CROSS_DEVICE
CROSS_LAB
CROSS_DOMAIN
FAILED_GENERALIZATION
CONTESTED
```

---

# Part III — V3 metamodel

## 10. Layered architecture

V3 uses two linked but distinct worlds.

### 10.1 Epistemic layer

What SDBES claims, observes, infers and verifies:

```text
Source
→ Study / Proof / System
→ Result / Observation
→ Claim Assessment
→ Claim
→ Inference / Argument
```

### 10.2 Structural layer

What a modeled scientific or technological pathway requires:

```text
Structural Predicate
→ Requirement Gate
→ Route / Architecture
→ Outcome Target
```

### 10.3 Translation layer

What permits epistemic evidence to inform, but not automatically determine, a structural state:

```text
Claim / Claim Assessment
→ Translation Link
→ Structural Assessment
→ Structural Predicate
```

## 11. Structural Predicate

The conceptual V3 `Capability / Condition` object is generalized to:

```text
StructuralPredicate
```

A Structural Predicate is a normalized, scoped proposition about the modeled world or system.

Subtypes:

```text
CAPABILITY
CONDITION
RESOURCE_AVAILABILITY
CONSTRAINT_SATISFIED
OUTCOME
```

Examples:

- `CAPABILITY`: magnet system sustains field ≥ 20 T under environment E.
- `CONDITION`: plasma remains within stability envelope S for duration T.
- `RESOURCE_AVAILABILITY`: tritium inventory ≥ required quantity Q.
- `CONSTRAINT_SATISFIED`: wall heat flux remains below limit L.
- `OUTCOME`: plant exports net electricity above threshold P with availability A.

Required fields:

```text
predicate_id
name
subtype
description
predicate_expression
variables[]
units[]
comparison_operator
threshold_or_target
scope
operating_conditions
valid_time
knowledge_time
version
canonical_identity
```

A Structural Predicate definition does not itself contain a current truth value.

## 12. Structural state records

State is stored separately from predicate definition.

### 12.1 Structural Assessment

A Structural Assessment records what SDBES is justified in saying about a Structural Predicate.

```text
structural_assessment_id
predicate_id
knowledge_status
claim_assessment_inputs[]
translation_links[]
scope
scenario_id
valid_time
knowledge_time
assessor
ruleset_version
rationale
limitations
```

### 12.2 Scenario State

A Scenario State records a hypothetical or observed model assignment.

```text
scenario_state_id
predicate_id
scenario_id
state_value
numeric_value_if_any
units
source
valid_time
version
```

This preserves:

\[
K(t) \neq X(t)
\]

A paper can update knowledge without changing the physical system.

## 13. Claim vs Structural Predicate

A Claim is a proposition asserted by a source or SDBES assessment.

A Structural Predicate is a normalized element of a pathway model.

Example:

```text
Claim:
“The tested model coil reached approximately 20 T peak field on conductor.”

Structural Predicate:
“A magnet architecture can satisfy field, duration, stress and integration
requirements for compact high-field tokamak route R.”
```

The first does not automatically set the second to true.

A Structural Assessment must explicitly perform that translation.

## 14. Requirement Gate

A Requirement Gate is a first-class factor node connecting prerequisite predicates to an output predicate.

```text
RequirementGate
```

Required fields:

```text
gate_id
operator
input_predicate_ids[]
output_predicate_id
route_id
k_if_applicable
threshold_expression_if_applicable
custom_evaluator_if_applicable
scope
operating_conditions
decomposition_status
supporting_claim_ids[]
assertion_status
valid_time
knowledge_time
version
```

Supported operators:

```text
ALL
ANY
K_OF_N
THRESHOLD
CUSTOM
```

## 15. Route

A Route is a named, scoped architecture or pathway through which a target may be satisfied.

```text
route_id
name
target_predicate_id
gate_ids[]
architecture_scope
scenario_scope
closure_status
sequence_constraints[]
alternative_group_id
supporting_claim_ids[]
status
version
```

A Route can contain several gates and intermediate predicates.

## 16. Alternative Group

Alternative routes to the same target are grouped explicitly:

```text
alternative_group_id
target_predicate_id
route_ids[]
coverage_status
scope
version
```

Pairwise “substitute” arrows are insufficient because substitution may be partial, asymmetric and condition-dependent.

If pairwise replacement is recorded, it must include:

```text
source_route
target_route
replacement_direction
coverage: FULL | PARTIAL | UNKNOWN
performance_envelope
scope
tradeoffs
```

## 17. Constraint object

`INCOMPATIBLE_WITH` is not a prerequisite edge. It is represented separately:

```text
constraint_id
constraint_type
member_ids[]
expression
scope
operating_conditions
supporting_claim_ids[]
status
version
```

Constraint types may include:

```text
MUTUAL_EXCLUSION
RESOURCE_LIMIT
BOUNDARY_LIMIT
REGULATORY_LIMIT
CONSERVATION_CONSTRAINT
DESIGN_INCOMPATIBILITY
```

Constraints are not mixed into the monotone route engine unless transformed into an explicit positive predicate such as `TEMPERATURE_WITHIN_LIMIT`.

## 18. Inference / Argument object

Epistemic dependencies require an argument object because several premises may jointly support a conclusion.

```text
inference_id
premise_claim_ids[]
conclusion_claim_id
rule_type
logical_form
scope
assumptions[]
validity_status
verification_activities[]
version
```

Rule types may include:

```text
DEDUCTIVE
INDUCTIVE
STATISTICAL
MODEL_DERIVED
ANALOGICAL
EXPERT_INFERENCE
```

V2 remains responsible for assessing whether the inference is valid or adequately supported.

---

# Part IV — Typed relation system

## 19. Relation families

Mixed edge types must not be multiplied together or traversed without an explicit projection.

### 19.1 Evidential relations

| Relation | Signature | Engine use |
|---|---|---|
| `DIRECT_EVIDENCE_FOR` | ClaimAssessment → Claim | Epistemic |
| `COUNTEREXAMPLE_TO` | ClaimAssessment → universal Claim | Epistemic; exact scope required |
| `CONTRADICTORY_EVIDENCE_FOR` | ClaimAssessment → Claim | Epistemic |

### 19.2 Translation/relevance relations

| Relation | Meaning |
|---|---|
| `COMPONENT_EVIDENCE_FOR` | Evidence concerns one component of a broader structural predicate |
| `MECHANISM_SEED_FOR` | Evidence supports existence/plausibility of a mechanism, not integrated capability |
| `MODEL_EVIDENCE_FOR` | A model result informs a structural predicate under stated assumptions |
| `CONSTRAINT_ON` | Evidence supports a bound or restriction on a structural predicate or route |
| `SCOPE_LIMIT_ON` | Evidence limits where a broader claim/predicate applies |
| `BACKGROUND_FOR` | Context only; excluded from state propagation |
| `ADJACENT_TO` | Thematically related; excluded from inference and state propagation |

A Translation Link records:

```text
translation_link_id
source_id
source_type
target_predicate_id
relation_type
scope_match
translation_gaps
supporting_assessment_ids[]
verification_activities[]
version
```

No Translation Link directly changes structural state. A Structural Assessment consumes it.

### 19.3 Assessment provenance relations

As specified in Section 6.

### 19.4 Epistemic inference relations

Premises and conclusions are represented through Inference objects rather than unrestricted pairwise arrows.

### 19.5 Structural route relations

Canonical structural graph edges are:

```text
PREDICATE_INPUT_TO_GATE
GATE_PRODUCES_PREDICATE
GATE_MEMBER_OF_ROUTE
ROUTE_MEMBER_OF_ALTERNATIVE_GROUP
ROUTE_TARGETS_PREDICATE
```

Direct `NECESSARY_FOR` and `SUFFICIENT_FOR` edges are not primary storage primitives. Necessity and sufficiency are derived or explicitly asserted with scope and proof.

## 20. Translation gaps

Translation distance must not initially be collapsed into one number.

Record categorical gaps:

```text
scale_gap
environment_gap
duration_gap
integration_gap
performance_gap
resource_gap
manufacturing_gap
economics_gap
validation_gap
```

Each may be:

```text
NONE
MINOR
MATERIAL
MAJOR
UNKNOWN
NOT_APPLICABLE
```

Example:

A 20 T coil experiment may have little field-strength gap but major integration, duration, neutron-environment, maintainability and whole-plant gaps.

---

# Part V — Composite claims and structural decomposition

## 21. Composite claim decomposition

A broad DBE proposition may be decomposed into subclaims, but not every decomposition is a logical equivalence.

Every decomposition receives one status:

```text
EXACT_LOGICAL
NECESSARY_ONLY
SUFFICIENT_ONLY
PARTIAL
HEURISTIC
SEQUENTIAL_APPLICATION_CHAIN
UNKNOWN
```

Only `EXACT_LOGICAL`, formally accepted `NECESSARY_ONLY`, and formally accepted `SUFFICIENT_ONLY` decompositions may enter logical propagation as specified.

`PARTIAL`, `HEURISTIC`, and `SEQUENTIAL_APPLICATION_CHAIN` decompositions remain useful for research navigation but must not determine truth or route viability.

Example:

```text
quantum error correction
→ fault-tolerant computer
→ useful chemistry simulation
→ faster materials discovery
→ energy-relevant material
```

This is initially a sequential application chain, not a proven logical implication chain.

## 22. Atomicity rule

A claim or Structural Predicate is sufficiently atomic for V3 when:

- it has one identifiable outcome;
- its scope and threshold are explicit;
- it does not silently bundle several independently failing stages;
- and its truth/satisfaction can be assessed without first inventing an unstated decomposition.

Atomicity is practical and model-relative, not metaphysical.

---

# Part VI — Knowledge-state and scenario-state logic

## 23. Why three values are insufficient for knowledge

V1 requires support and refutation to remain separate.

Therefore “unknown” and “conflicted” must not be collapsed.

V3 represents epistemic status as an evidence pair:

\[
K(p)=(t_p,f_p),\qquad t_p,f_p\in\{0,1\}
\]

where:

- `t_p = 1` means there is qualifying support for the predicate;
- `f_p = 1` means there is qualifying support against the predicate.

The four statuses are:

| Pair | Status |
|---|---|
| `(0,0)` | `NEITHER` — unresolved/unassessed |
| `(1,0)` | `TRUE_ONLY` — supported, not qualifyingly refuted |
| `(0,1)` | `FALSE_ONLY` — refuted/blocked, not qualifyingly supported |
| `(1,1)` | `BOTH` — materially conflicted |

These are information states, not calibrated probabilities.

## 24. Four-valued gate propagation

For evidence pairs, use Belnap–Dunn-style conjunction and disjunction.

### ALL / conjunction

For inputs \(x_i=(t_i,f_i)\):

\[
t_{ALL}=\bigwedge_i t_i
\]

\[
f_{ALL}=\bigvee_i f_i
\]

### ANY / disjunction

\[
t_{ANY}=\bigvee_i t_i
\]

\[
f_{ANY}=\bigwedge_i f_i
\]

### Negation

\[
\neg(t,f)=(f,t)
\]

Negation is not normally needed in the monotone route core; it is defined for completeness.

### K-of-N

For \(n\) inputs and threshold \(k\):

\[
t_{k/n}=1\quad\text{iff}\quad \sum_i t_i\ge k
\]

\[
f_{k/n}=1\quad\text{iff}\quad \sum_i f_i\ge n-k+1
\]

This permits a result to be `BOTH` when qualifying evidence supports both satisfaction and nonsatisfaction.

## 25. Scenario-state logic

A scenario assignment uses:

```text
TRUE
FALSE
UNKNOWN
```

It may represent an observed system state, a hypothetical intervention state, or an explicit modeling assumption.

For logical gates, use strong three-valued semantics:

### ALL

- if any input is `FALSE`, output `FALSE`;
- if all inputs are `TRUE`, output `TRUE`;
- otherwise output `UNKNOWN`.

### ANY

- if any input is `TRUE`, output `TRUE`;
- if all inputs are `FALSE`, output `FALSE`;
- otherwise output `UNKNOWN`.

### K-of-N

Let \(T\) be the count of true inputs and \(U\) the count of unknown inputs.

\[
T\ge k\Rightarrow TRUE
\]

\[
T+U<k\Rightarrow FALSE
\]

otherwise:

\[
UNKNOWN
\]

## 26. Context compatibility rule

Gate propagation is permitted only after inputs are bound to a compatible evaluation context.

The context includes:

```text
scenario
architecture
operating regime
spatial scope
temporal interval
parameter range
valid-time overlap
```

Evidence that supports A in context S1 and B in mutually incompatible context S2 does not support \(A\land B\) in either context.

Before evaluating a gate, the implementation must produce one of:

```text
COMPATIBLE
PARTIALLY_OVERLAPPING
INCOMPATIBLE
UNRESOLVED
```

- `COMPATIBLE` permits evaluation.
- `PARTIALLY_OVERLAPPING` requires an explicitly narrowed common scope before evaluation.
- `INCOMPATIBLE` blocks the combination and records a scope error rather than a truth value.
- `UNRESOLVED` leaves the gate unresolved.

This prevents separately true results from different regimes from being combined into a nonexistent integrated capability.

## 27. Numeric predicates and thresholds

A numeric Structural Predicate may be evaluated only when its variables, units and comparison rule are defined.

Example:

```text
field_strength >= 20 tesla
```

If the value is an interval:

- entire interval satisfies threshold → `TRUE`;
- entire interval violates threshold → `FALSE`;
- interval overlaps threshold → `UNKNOWN`.

Conflicting measurements remain a knowledge-state problem and may produce `BOTH` in Structural Assessment.

No probability is inferred from these statuses.

---

# Part VII — Necessity, sufficiency and alternatives

## 28. Route-local requirement

If predicate A is an input to an ALL gate within Route R, then A is required **within Route R**.

This does not establish that A is globally necessary for the target.

## 29. Necessity within a model

For target \(T\), model \(M\), scope \(S\), and represented minimal path sets \(\mathcal P(T,M,S)\):

A is necessary within the represented model if, and only if, path-set enumeration is complete for that model and:

\[
\forall P\in\mathcal P(T,M,S),\quad A\in P
\]

A partial path-set enumeration may identify a candidate necessary predicate but cannot establish necessity.

The correct label is:

```text
NECESSARY_WITHIN_MODEL
```

not “physically necessary” unless completeness is independently established.

## 30. Sufficiency within a model

A set \(P\) is sufficient within model \(M\) and scope \(S\) if setting all members of \(P\) to satisfied, together with declared background conditions, satisfies the target under the route semantics.

The background conditions must be explicit.

## 31. Closure status and open-world protection

Every target model records:

```text
OPEN_WORLD
CLOSED_WITHIN_DEFINED_ARCHITECTURE
CLAIMED_COMPLETE_UNVERIFIED
```

Under `OPEN_WORLD`:

- exhausting all represented routes does not establish impossibility;
- a cut set blocks all **represented** routes only;
- a global necessity result is model-relative;
- unknown alternative mechanisms remain possible.

Under `CLOSED_WITHIN_DEFINED_ARCHITECTURE`, conclusions apply only to that explicitly bounded architecture.

## 32. Alternatives and substitution

Alternative routes are modeled explicitly.

A failure in one route does not invalidate the target if another viable route remains.

Substitution must record:

- direction;
- full or partial coverage;
- operating envelope;
- performance differences;
- resource and constraint tradeoffs;
- and scenario scope.

---

# Part VIII — Graph and Boolean mathematics

## 33. V3 is not one matrix

V3 is a typed multilayer factor graph.

Useful matrix projections may be generated, but matrices are views over selected relation types.

Conceptually:

\[
G_K=\text{Epistemic argument graph}
\]

\[
G_X=\text{Structural requirement factor graph}
\]

\[
G_T=\text{Translation/relevance graph}
\]

No operation may multiply or add edges across these layers without an explicit composition rule.

## 34. Sparse adjacency projections
For a selected pairwise relation type \(r\), define:

\[
D^{(r)}_{ji}=1
\]

when source \(i\) has relation \(r\) to destination \(j\), using the SDBES source-column/destination-row convention.

These matrices are sparse and typed.

## 35. Boolean-semiring reachability

For simple pairwise reachability, use Boolean multiplication:

- addition becomes OR;
- multiplication becomes AND.

Then a Boolean power indicates existence of a typed walk of a specified length.

This is valid for questions such as:

> Is there a two-hop path of typed relation r from A to B?

It is not sufficient for:

- AND-gate satisfaction;
- k-of-n satisfaction;
- route viability;
- minimal path/cut analysis in a factor graph;
- causal effect;
- probability;
- or evidence aggregation.

## 36. Gate-aware evaluation

Requirement Gates must be evaluated as a Boolean/multivalued circuit or factor graph.

Permitted implementation strategies include:

- direct recursive gate evaluation for acyclic models;
- Binary Decision Diagrams;
- SAT/SMT encodings;
- monotone Boolean circuit analysis;
- bounded symbolic model checking where temporal structure is later added.

The chosen algorithm and version must be recorded.

## 37. Monotone core

Minimal path/cut semantics are clearest for a monotone positive-predicate core:

> Satisfying additional prerequisite predicates cannot make an otherwise satisfied target fail.

Where practical, encode boundaries as positive predicates:

```text
TEMPERATURE_WITHIN_LIMIT
```

rather than unrestricted NOT edges.

Nonmonotone compatibility constraints are checked separately.

---

# Part IX — Path sets, cut sets and dominators

## 38. Minimal path set

For a monotone structural model, a minimal path set for target \(T\) is a smallest set of atomic Structural Predicates whose satisfaction is sufficient to satisfy \(T\) in the declared model and scope.

No proper subset is sufficient.

## 39. Minimal cut set

A minimal cut set for target \(T\) is a smallest set of atomic Structural Predicates whose nonsatisfaction blocks every represented satisfying route to \(T\) in the declared model and scope.

No proper subset has that blocking property.

## 40. Model-relative labeling

Every path/cut output includes:

```text
target_id
model_snapshot_id
scope
scenario_id
closure_status
gate_semantics_version
enumeration_complete
max_set_size
max_results
time_limit
algorithm
algorithm_version
```

Under open-world modeling, display:

```text
REPRESENTED_ROUTE_PATH_SET
REPRESENTED_ROUTE_CUT_SET
```

not an unqualified universal conclusion.

## 41. Enumeration complexity

The number of minimal path or cut sets may grow exponentially.

V3 therefore permits:

- lazy enumeration;
- top-k or bounded-size enumeration;
- time limits;
- result limits;
- BDD/SAT-based methods;
- and partial-result reporting.

A partial enumeration must never be presented as complete.

## 42. Dominators

Dominator analysis is valid only after specifying:

- a rooted directed projection;
- a selected target or flow direction;
- a gate-normalized representation;
- and a super-root when multiple structural roots exist.

A node A dominates node T when every path from the selected root to T passes through A in that projection.

Dominator output is representation-relative and does not replace gate-aware minimal path/cut analysis.

## 43. Pillar profile

V3 does not define a universal scalar Pillar Score.

A Pillar Profile contains inspectable structural diagnostics:

```text
downstream_predicate_reach
downstream_target_reach
cross_domain_reach
minimal_cut_set_memberships
minimal_path_set_memberships
dominator_targets
alternative_route_count
replacement_coverage
route_local_requirement_count
model_snapshots[]
```

Epistemic support is shown alongside this profile, never multiplied into it by default.

## 44. Bottleneck profile

A Bottleneck Profile contains:

```text
scenario_blocking_state
blocked_route_count
blocked_target_count
minimal_cut_set_memberships
alternative_route_coverage
constraint_memberships
demonstration_context
knowledge_status
translation_gaps
```

Possible descriptive labels:

```text
ACTIVE_BLOCKER
POTENTIAL_BLOCKER
UNRESOLVED_BOTTLENECK
REDUNDANT_OR_BYPASSED
NOT_BLOCKING_IN_SCENARIO
```

Bottleneck, research priority and engineering priority remain distinct concepts.

---

# Part X — Cycles, bootstraps and fixed points

## 45. Strongly connected components

V3 detects strongly connected components in selected directed projections.

Cycle type must be classified.

### 44.1 Epistemic circularity

Claims support one another without independent grounding.

Label:

```text
POTENTIAL_CIRCULAR_JUSTIFICATION
```

### 44.2 Structural bootstrap dependency

Capabilities require one another or require infrastructure that itself depends on them.

Label:

```text
BOOTSTRAP_DEPENDENCY
```

### 44.3 Dynamic feedback

A changes B and B changes A over time.

This belongs to V4 and must not be analyzed as a V3 prerequisite cycle.

## 46. Condensation graph

For graph-level visualization and reach analysis, each strongly connected component may be condensed into a supernode.

The condensation graph is acyclic.

Internal structure must remain accessible by drill-down.

## 47. Fixed-point semantics for structural cycles

For a monotone cyclic **scenario-state** structural model:

\[
x=F(x)
\]

compute least and greatest fixed points under the declared seed assignments.

- If least and greatest fixed points agree, the structural state is uniquely determined.
- If they differ, the cycle is underdetermined without additional seed/initialization assumptions.

Label:

```text
UNDERDETERMINED_BOOTSTRAP
```

An external seed, staged construction capability or initial condition may resolve the cycle.

V3 does not infer the probability or cost of obtaining that seed.

---

# Part XI — Time, snapshots and reproducibility

## 48. Bitemporal records

All V3 objects preserve:

- valid/event time;
- knowledge/recorded time;
- version;
- supersession/invalidation relations.

## 49. Derived diagnostic run

Path sets, cut sets, SCCs, dominators, pillar profiles and bottleneck profiles are derived artifacts.

Every diagnostic run records:

```text
derivation_run_id
graph_snapshot_id
snapshot_hash
ruleset_version
algorithm
algorithm_version
parameters
scope
scenario_id
closure_status
started_at
completed_at
completion_status
outputs[]
limitations
```

When an underlying graph, relation, scope or gate changes, the prior diagnostics remain historically valid for their snapshot but become stale for the current snapshot.

## 50. Hierarchical aggregation

Domain-, focus-area- and concept-level edges are visualization summaries unless a valid quotient/aggregation model is defined.

A high-level edge must retain:

```text
source_lower_level_relations[]
relation_type_counts
scope_summary
conflict_summary
aggregation_method
snapshot_id
```

A single claim-level relation must not be displayed as though an entire field universally depends on another field.

---

# Part XII — Mapping the 10-paper stress test into V3

## 51. SPARC high-field model coil

```text
Direct Claim
→ COMPONENT_EVIDENCE_FOR
→ Structural Assessment
→ High-field magnet component predicate
```

It does not directly satisfy:

```text
net-electric compact tokamak outcome
```

The translation gaps include integration, duration, neutron environment, fuel cycle, exhaust, availability and economics.

## 52. Knotted magnetic structures simulation

```text
Simulation Claim
→ MODEL_EVIDENCE_FOR / MECHANISM_SEED_FOR
→ topology-informed confinement predicate
```

Physical validation and device-level transport remain unresolved.

## 53. Quantum-battery superabsorption

The experiment can support a collective-charging predicate while leaving extraction, retention, cycle life and wall-plug efficiency predicates unresolved.

The application requires a multi-gate storage route.

## 54. AI plasma control

This is close to direct evidence for a bounded control capability in the tested regime.

Cross-device and reactor-level generalization remain separate predicates.

## 55. AI materials discovery

The application chain becomes explicit predicates and gates:

```text
candidate prediction
→ synthesizability
→ correct identification
→ independent verification
→ useful service property
→ manufacturability
→ deployment relevance
```

The chain is not assumed exact until each relation is specified.

## 56. Autonomous laboratory correction and critique

Correction and challenge relations attach only to affected Claim Assessments.

A correction to novelty or phase identification does not erase evidence that the automated laboratory physically operated.

## 57. Quantum error correction

Below-threshold logical-memory performance supports one predicate in a route toward useful fault-tolerant computation.

It does not directly satisfy the downstream quantum-chemistry or energy-discovery outcome.

## 58. 3D cubic-code self-correction

The theorem/bound and numerical model evidence inform a model-level memory predicate.

Implementability and hardware-cost predicates remain unresolved.

## 59. Equilibrium time-crystal no-go theorem

The theorem creates a scoped constraint on equilibrium routes.

It does not block driven/Floquet routes outside its assumptions.

## 60. Quantum energy teleportation

A model-existence protocol informs a theoretical mechanism predicate.

Practical energy-control capability requires additional predicates for preparation, measurement, communication, reset, extraction and complete energy accounting.

---

# Part XIII — Normative schema summaries

## 61. Structural Predicate

```text
predicate_id
canonical_identity
name
subtype
predicate_expression
variables[]
units[]
comparison_operator
threshold_or_target
scope
operating_conditions
valid_time
knowledge_time
version
```

## 62. Structural Assessment

```text
structural_assessment_id
predicate_id
knowledge_status
supporting_claim_assessment_ids[]
refuting_claim_assessment_ids[]
translation_link_ids[]
demonstration_context
scope
scenario_id
valid_time
knowledge_time
assessor
verification_activities[]
ruleset_version
rationale
limitations
version
```

## 63. Translation Link

```text
translation_link_id
source_id
source_type
target_predicate_id
relation_type
scope_match
translation_gaps
verification_activities[]
version
```

## 64. Inference

```text
inference_id
premise_claim_ids[]
conclusion_claim_id
rule_type
logical_form
scope
assumptions[]
validity_status
verification_activities[]
version
```

## 65. Requirement Gate

```text
gate_id
operator
input_predicate_ids[]
output_predicate_id
route_id
k_if_applicable
threshold_expression_if_applicable
custom_evaluator_if_applicable
scope
operating_conditions
decomposition_status
supporting_claim_ids[]
assertion_status
valid_time
knowledge_time
version
```

## 66. Route

```text
route_id
name
target_predicate_id
gate_ids[]
architecture_scope
scenario_scope
closure_status
sequence_constraints[]
alternative_group_id
supporting_claim_ids[]
status
version
```

## 67. Derived Diagnostic Run

As defined in Section 49.

---

# Part XIV — Required acceptance tests

A V3 implementation is not conformant until it passes these tests.

## A. Layer separation

### Test 1 — Claim does not automatically set capability

A component experiment supports a direct claim.

Expected: the related integrated capability remains unresolved until a Structural Assessment is created.

### Test 2 — Knowledge state does not alter world state

A new paper changes a Structural Assessment.

Expected: an observed/scenario state record does not change unless separately updated.

## B. Evidence and translation

### Test 3 — Component evidence

A high-field coil result is linked to a fusion-plant outcome.

Expected: `COMPONENT_EVIDENCE_FOR`, not `DIRECT_EVIDENCE_FOR`.

### Test 4 — Correction scope

A correction changes one assessment in a multi-result paper.

Expected: only dependent Structural Assessments are reopened.

### Test 5 — Source reported vs independently checked

A paper reports replication but SDBES has not screened the replication.

Expected: both facts remain distinguishable.

### Test 6 — Translation gaps

A result matches performance but not environment or duration.

Expected: structural predicate is not automatically satisfied.

## C. Composite claims

### Test 7 — Exact vs heuristic decomposition

The same high-level proposition receives one exact logical decomposition and one heuristic research chain.

Expected: only the exact decomposition enters gate propagation.

### Test 8 — Application chain

QEC → fault-tolerant computer → chemistry → materials → energy.

Expected: each stage remains separately assessable; no transitive truth is assumed.

## D. Gate logic

### Test 9 — AND vs OR

Identical inputs are assigned to ALL and ANY gates.

Expected: different results under partial satisfaction.

### Test 10 — Unknown is not false

One necessary input is unresolved.

Expected: target is `UNKNOWN`, not `FALSE`, unless another input already forces false.

### Test 11 — Conflict is not unknown

A prerequisite has qualifying support and refutation.

Expected: knowledge status is `BOTH`, not `NEITHER`.

### Test 12 — K-of-N

For 2-of-3: one true, one false, one unknown.

Expected: `UNKNOWN`.

Two true.

Expected: `TRUE`.

Two false.

Expected: `FALSE`.

### Test 13 — Context incompatibility

Predicate A is supported only in operating regime S1. Predicate B is supported only in mutually exclusive regime S2. An ALL gate requires A and B in one operating context.

Expected: no `TRUE` propagation; the gate records incompatible scope or remains unresolved.

## E. Necessity and alternatives

### Test 14 — Route-local is not global

Target can be satisfied by route `{A,B}` or route `{C}`.

Expected: A is required within the first route but not globally necessary.

### Test 15 — Alternative route survives

Route A is blocked; Route B is viable.

Expected: target remains viable within the model.

### Test 16 — Open-world cut set

All represented routes are blocked in an `OPEN_WORLD` model.

Expected: “all represented routes blocked,” not “target impossible.”

## F. Graph mathematics

### Test 17 — Pairwise reachability does not satisfy AND gate

Boolean adjacency shows paths from A and B to target gate.

Expected: target is not satisfied unless gate semantics are evaluated.

### Test 18 — Duplicate edge invariance

The same structural assertion is imported five times through duplicate reports.

Expected: route viability and reachability do not change.

### Test 19 — Nonmonotone constraint exclusion

An incompatibility relation is inserted.

Expected: it is evaluated by the constraint layer, not the monotone cut-set engine.

## G. Cycles

### Test 20 — Bootstrap without seed

A requires B and B requires A, with no seed.

Expected: least and greatest fixed points differ; state is `UNDERDETERMINED_BOOTSTRAP`.

### Test 21 — Bootstrap with seed

The same cycle receives a valid external seed.

Expected: unique fixed point may become available.

### Test 22 — Epistemic circularity

Claim A relies solely on B and B solely on A.

Expected: `POTENTIAL_CIRCULAR_JUSTIFICATION`.

## H. Diagnostics and provenance

### Test 23 — Dominator root dependence

Change the selected root.

Expected: dominator result may change and records the root/projection.

### Test 24 — Diagnostic staleness

A route is added after cut sets are computed.

Expected: prior diagnostics remain historically preserved but are stale for the new snapshot.

### Test 25 — Aggregation provenance

A single claim-level dependency generates a high-level field-to-field visualization edge.

Expected: drill-down reveals the originating relation; no universal field-level claim is asserted.

### Test 26 — Partial enumeration

Minimal cut-set enumeration hits a configured limit.

Expected: results are marked incomplete and are not used as exhaustive necessity proof.

---

# Part XV — Formal review verdict

## 68. Readiness

**Ready for repository commit within reviewed scope.**

The formalized V3 resolves the material failure modes exposed by the V1/V2 10-paper stress test and by the mathematical audit of the conceptual V3.

## 69. Remaining limitations

V3 remains a structural model, not a validated scientific ontology or causal simulator.

Its outputs are valid only relative to:

- the represented claims;
- the selected scopes;
- the declared route model;
- the closure assumption;
- the graph snapshot;
- and the algorithms used.

## 70. Exit criteria before V4

V3 is complete enough to begin V4 when:

1. Structural Predicate, Structural Assessment, Translation Link, Gate and Route records can be created.
2. V1/V2 assessment provenance amendments are implemented.
3. Exact vs heuristic decompositions are distinguishable.
4. Four-valued knowledge and three-valued scenario tests pass.
5. Route-local vs model-global necessity is correctly distinguished.
6. At least the ten-paper corpus can be mapped without direct paper-to-capability overclaim.
7. Derived diagnostics are snapshot-versioned.
8. Open-world warnings are visible.

---

# Part XVI — V4 handoff contract

V4 should be titled:

> **Influence, Causality & Dynamic-State Semantics**

V4 may consume V3 outputs but must introduce its own typed objects for:

```text
state variables
units
baselines
causal mechanisms
interventions
comparators
effect functions
sign and magnitude
time lags
feedback
uncertainty distributions
scenario parameters
resource flows
```

V4 must preserve:

\[
\text{Structural Requirement} \neq \text{Causal Effect}
\]

A V3 gate says what a represented route requires.

A V4 causal model says what changes under an intervention and by how much.

V4 must not use V3 centrality, cut-set membership or epistemic support as causal coefficients.

---

# References informing the formalization

- W. E. Vesely et al., *Fault Tree Handbook*, NUREG-0492, U.S. Nuclear Regulatory Commission, 1981.
- R. W. Butler and A. L. Martensen, *The Fault Tree Compiler: Program and Mathematics*, NASA-TP-2915, 1989.
- R. E. Tarjan, “Depth-First Search and Linear Graph Algorithms,” *SIAM Journal on Computing* 1(2), 1972.
- T. Lengauer and R. E. Tarjan, “A Fast Algorithm for Finding Dominators in a Flowgraph,” *ACM TOPLAS* 1(1), 1979.
- O. Arieli and A. Avron, “Reasoning with Logical Bilattices,” *Journal of Logic, Language and Information* 5(1), 1996.
- W3C, *PROV-O: The PROV Ontology* and related PROV recommendations, 2013.
