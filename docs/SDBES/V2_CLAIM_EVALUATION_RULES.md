# SDBES V2 — Claim Evaluation Rules

**Project:** SDBES — Search for Dimensions Beyond Energy Scarcity  
**Branch:** SDBES  
**Status:** Approved framework version  
**Supersedes:** V1 only for claim-evaluation behavior; V1 remains the typed-ledger foundation

## 1. Purpose

V2 defines how SDBES evaluates scientific and technical claims without forcing every claim through one universal confidence formula.

The central rule is:

> **Every assessment must target an identifiable proposition, under identifiable conditions, using an evaluation method appropriate to that proposition.**

V2 keeps the V1 distinction between:

- descriptive evidence profiles
- formal validity
- empirical support
- engineering demonstration
- causal effects
- forecasts
- probabilities

These are related but not interchangeable.

## 2. Claims before scores

A broad research question may enter SDBES immediately, but it must not be treated as a scored scientific claim until it is operationally defined.

Example research question:

> Could AI materially accelerate progress toward energy abundance?

This may be stored as a research question or hypothesis-generation target.

An evaluable claim is narrower, for example:

> Under operating condition set S, controller A reduces auxiliary electricity consumption by at least 15% compared with controller B over interval T.

A claim record should include:

```text
claim_id
statement
claim_type
logical_form
scope
conditions
variables
units
outcome
baseline_or_comparator
threshold_or_decision_criterion
time_horizon
source_or_origin
version
status
```

## 3. Claim characteristics are multi-axis

A claim should not be forced into a single mutually exclusive label.

For example, a claim can simultaneously be:

- empirical
- comparative
- universal within a specified operating regime

SDBES therefore separates:

### Subject / epistemic family

- formal / mathematical
- empirical / observational
- numerical / simulation
- engineering / feasibility
- causal / intervention
- forecast / predictive

### Logical form

- universal
- existential
- conditional
- equality
- inequality
- threshold
- comparative
- implication

### Scope

- population or system
- operating regime
- spatial domain
- temporal interval
- parameter range
- assumptions

## 4. Epistemic Engine adapters

The Epistemic Engine uses different evaluation adapters.

### 4.1 Formal claims

Question:

> Does the conclusion follow from the specified premises and assumptions?

Possible outcomes include:

- proved under stated assumptions
- formally verified
- proof incomplete
- proof invalid
- counterexample found
- assumptions inconsistent
- claim not yet formalized

A verified counterexample defeats a universal claim.

A failed proof does **not** automatically prove the conclusion false.

### 4.2 Empirical claims

Question:

> What do observations establish about the specified quantity, effect, or relationship?

Evaluate:

- study design
- population / sample
- measurement quality
- uncertainty
- comparator
- effect magnitude
- replication
- external validity
- scope compatibility

A statistically inconclusive result is not automatically evidence of no effect.

A result showing some benefit does not automatically establish that a specified engineering or policy threshold has been reached.

### 4.3 Numerical / simulation claims

Question:

> Is the computation implemented correctly, and does the model correspond to the physical system for the claimed use?

Separate:

- code correctness
- numerical verification
- convergence
- reproducibility
- parameter provenance
- sensitivity
- model validation
- physical correspondence

A reproduced simulation is not automatically a validated physical theory.

### 4.4 Engineering claims

Question:

> Does the defined system meet the defined requirement under the tested operating conditions?

Evaluate:

- requirement definition
- integration state
- test environment
- reliability
- tolerances
- failure modes
- scalability
- reproducibility
- deployment relevance

Individual component success does not automatically establish integrated-system feasibility.

### 4.5 Causal claims

Question:

> What changes because of a specified intervention?

Require, where applicable:

- intervention
- comparator
- outcome
- population / system
- conditions
- identification assumptions
- causal graph or mechanism
- confounders
- mediation
- uncertainty

Association alone does not become a simulator-ready causal coefficient.

### 4.6 Forecast claims

Question:

> What event or measurable outcome is predicted, by when, under what conditions?

Require:

- target event
- horizon
- resolution criterion
- probability source
- forecast date
- model or elicitation method
- later resolution outcome
- calibration history where available

## 5. Claim Assessment object

The central V2 record is the Claim Assessment.

A Claim Assessment connects a result or evidence item to a scoped claim and records what SDBES has actually checked.

Suggested fields:

```text
assessment_id
claim_id
claim_version
result_id
source_version
assessment_method
scope_match
evidence_direction
evidence_quality_profile
independence_lineage
assumptions_checked
checks_performed
unresolved_questions
conclusion_state
probability_if_any
probability_model_if_any
assessor
assessment_time
ruleset_version
notes
```

The critical distinction is:

```text
what the source reports
≠
what SDBES independently verified
```

Example:

```text
Author-reported replication: yes
SDBES replication independently checked: no
```

## 6. V1 3×3 F/E/A matrix retained as descriptive profile

SDBES retains:

[
E_i=
\begin{bmatrix}
F_V & F_I & F_G\\
E_V & E_I & E_G\\
A_V & A_I & A_G
\end{bmatrix}
]

Rows:

- Formal
- Empirical
- Applied

Columns:

- Validated within relevant methodology
- Independent
- Generalized

The matrix is a visualization and descriptive summary.

It does **not** directly calculate:

- truth probability
- causal effect
- research priority
- dependency strength

## 7. Evidence-state semantics

Each evidence criterion must distinguish at least:

```text
N/A       genuinely irrelevant
UNKNOWN   not assessed
ABSENT    relevant but no evidence currently available
PRESENT   relevant evidence exists
FAILED    criterion tested and not met
```

Presence and success are separate.

An experiment may be present and may fail to support the claim.

## 8. Support and refutation

Support and refutation remain separate descriptive quantities.

A claim may have:

- supporting evidence
- refuting evidence
- unresolved evidence
- scope-mismatched evidence
- inadmissible / retracted evidence

Net balances may be displayed only if the component meanings remain accessible.

A support/refute score is not automatically a probability of truth.

## 9. Claim states

Instead of forcing one universal confidence percentage, SDBES may apply multiple state labels.

Candidate states include:

```text
UNASSESSED
SPECULATIVE
FORMALLY_CONSISTENT
FORMALLY_PROVED_UNDER_ASSUMPTIONS
FORMALLY_REFUTED
EMPIRICALLY_SUGGESTIVE
EMPIRICALLY_SUPPORTED
INDEPENDENTLY_REPLICATED
ENGINEERING_DEMONSTRATED
CONTESTED
CONTRADICTED
FALSIFIED_IN_SCOPE
CONDITIONALLY_VALID
SIMULATION_VERIFIED
PHYSICALLY_UNVALIDATED
FORECAST_PENDING
FORECAST_RESOLVED
```

These are not a universal ordinal ladder.

Multiple labels may coexist.

## 10. Probability policy

Probability is allowed only when its source and interpretation are explicit.

A probabilistic assessment should identify:

[
P(H\mid D,M)
]

where:

- (H) = proposition
- (D) = evidence
- (M) = model and assumptions

Acceptable probability origins may include:

- Bayesian model
- statistical estimator
- reliability model
- calibrated forecast
- explicit expert elicitation
- Monte Carlo output from a defined model

A rubric score must not be silently converted into probability.

## 11. Formal verification

Formal proof tools such as Lean may increase confidence in derivation validity for formalized statements.

SDBES must still retain:

```text
statement actually formalized
axioms / assumptions used
proof artifact
proof checker/version
verification status
physical interpretation
```

Machine-checked proof validity does not itself establish empirical correspondence.

## 12. Evidence independence

V2 inherits the V1 provenance structure:

```text
Source document/version
→ Study / proof / system
→ Result / observation
→ Claim Assessment
→ Claim
```

The following may indicate non-independence:

- same experiment
- shared dataset
- overlapping population
- same simulation output
- shared model assumptions
- derivative publication
- copied benchmark
- same hardware run

Multiple reports of one observation add provenance, not independent evidential mass.

## 13. Ideas and hypotheses

SDBES must accept ideas before evidence exists.

An idea may be recorded as:

```text
Idea / research question
Origin
Possible domains
Possible concepts
Potential dependencies
Potential influence paths
Open questions
Evidence status: unassessed
Probability: unavailable
```

This preserves exploratory research while preventing speculative ideas from being treated as evidence.

## 14. Claim conflict logic

Two pieces of evidence should not automatically be marked contradictory.

Before assigning conflict, compare:

- proposition
- quantifier
- system/population
- operating regime
- endpoint
- threshold
- comparator
- units
- time horizon
- assumptions

Different conditions may explain apparently opposite results.

## 15. Revisions and corrections

SDBES is append-oriented.

A corrected or retracted source should remain historically visible.

Suggested states:

- active
- superseded
- corrected
- retracted
- disputed

Affected Claim Assessments should be re-evaluated rather than silently overwritten.

## 16. V2 acceptance tests

A conforming implementation should correctly represent at least the following cases:

### Test A — duplicate reporting
Two papers report the same underlying experiment.

Expected:
- two source records
- one underlying observation lineage
- no automatic doubling of independent evidence

### Test B — strong negative evidence
A high-quality experiment refutes a scoped claim.

Expected:
- high quality score
- negative evidence polarity
- no penalty to experimental quality merely because the result is negative

### Test C — scope mismatch
Two studies appear contradictory but operate under materially different regimes.

Expected:
- scope comparison
- no automatic cancellation

### Test D — verified simulation, unvalidated physics
A numerical result is reproduced but not compared successfully against physical observations.

Expected:
- simulation verification may pass
- empirical / physical validation remains unresolved

### Test E — speculative idea
A novel cross-field idea has no direct evidence.

Expected:
- idea accepted into ledger
- evidence marked unassessed
- no fabricated probability

### Test F — corrected publication
A result is later corrected.

Expected:
- prior version preserved
- new version linked
- affected assessments re-opened

### Test G — components without integrated system
Subsystems individually satisfy requirements but the combined system has not been tested.

Expected:
- component claims may be supported
- integrated feasibility remains unresolved

### Test H — universal mathematical counterexample
A universal claim has many examples supporting it and one verified counterexample.

Expected:
- universal claim refuted in its stated scope
- support counts do not outweigh the counterexample

## 17. Design examples before operational pilot

V2 explicitly encourages a small set of real design examples before the full schema is frozen.

Suggested design set:

- 3–5 diverse source papers/results
- approximately 10–20 useful scoped claims
- diversity preferred over quantity

Useful diversity includes:

- formal/theoretical paper
- experiment
- simulation
- prototype or engineering result
- disputed, corrected, failed, or contradictory case

These examples are for **schema development**, not a statistically representative scientific review.

## 18. Operational pilot

After dependency and influence semantics stabilize, conduct an operational pilot.

A practical target is approximately:

[
100\text{ reviewed scoped claims}
]

distributed across several focus areas.

This is a workflow target, not a mathematical sample-size theorem.

Track separately:

- source documents
- studies/proofs
- results
- claims
- claim assessments
- concepts
- ideas

Do not add these counts together as if they represented interchangeable evidence.

## 19. Exit criteria for V2

V2 is ready to feed V3 when the design examples can be represented without:

- inventing missing evidence
- silently changing claim scope
- treating quality scores as probabilities
- treating duplicate reports as independent observations
- treating simulation reproduction as physical validation
- treating one failed derivation as proof that a conclusion is physically impossible
- forcing unlike claim types through one aggregation rule

## 20. Next version

V3 is reserved for:

> **Dependency Mathematics & Structural Semantics**

V3 must be reviewed before being committed.
