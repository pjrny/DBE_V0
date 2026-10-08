# SDBES V1/V2 — 10-Paper Stress Test

**Project:** SDBES — Search for Dimensions Beyond Energy Scarcity  
**Test:** V1 Typed Evidence & Dependency Ledger + V2 Claim Evaluation Rules  
**Corpus:** `dimensions-beyond-energy/docs/research/phase1/`  
**Date:** 2026-10-08  
**Status:** Completed design stress test; not a systematic review and not a full-paper replication audit

## 1. Purpose

This test asks whether V1/V2 can represent real research spanning:

- engineering-scale component demonstrations,
- laboratory experiments,
- computational discovery,
- numerical simulation,
- corrected and challenged results,
- quantum hardware demonstrations,
- analytic/numerical theory,
- no-go theorems,
- and highly theoretical model protocols,

without turning a bounded result into an unsupported DBE-scale conclusion.

The test uses the Phase-1 atlas and source library as the intake corpus, then spot-checks primary publisher/official records for the selected papers and known corrections.

No experiment, simulation, raw-data reanalysis, or theorem formalization was independently reproduced by SDBES during this test.

## 2. Test design

For every paper, SDBES creates two conceptual assessments:

### A. Direct paper claim

The narrowest defensible claim supported by the screened source.

### B. DBE application claim

The broader candidate question or technological implication to which the atlas links the paper.

This distinction is deliberately adversarial.

A framework failure would occur if a component experiment, model result, or theorem were automatically promoted into evidence that the full DBE application is feasible.

## 3. Selected papers

| ID | Paper | Evidence mode | Primary DBE focus |
|---|---|---|---|
| N01 | [The SPARC Toroidal Field Model Coil Program](https://doi.org/10.1109/TASC.2023.3332613) | Experimental / engineering | Compact high-field tokamak power |
| C02 | [Self-Organizing Knotted Magnetic Structures in Plasma](https://doi.org/10.1103/PhysRevLett.115.095001) | Numerical simulation + analytic model | Magnetic topology and knotted-field confinement |
| C09 | [Superabsorption in an organic microcavity: Toward a quantum battery](https://doi.org/10.1126/sciadv.abk3160) | Experimental + theoretical model | Quantum batteries |
| I01 | [Avoiding fusion plasma tearing instability with deep reinforcement learning](https://doi.org/10.1038/s41586-024-07024-9) | Experimental control | AI-assisted plasma prediction and feedback |
| I02 | [Scaling deep learning for materials discovery](https://doi.org/10.1038/s41586-023-06735-9) | Computational | AI-guided materials discovery |
| I03 | [An autonomous laboratory for the accelerated synthesis of inorganic materials](https://doi.org/10.1038/s41586-023-06734-w) | Experimental autonomous workflow | Autonomous laboratories |
| I04 | [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) | Quantum hardware experiment | Quantum error correction |
| I07 | [Quantum Self-Correction in the 3D Cubic Code Model](https://doi.org/10.1103/PhysRevLett.111.200501) | Analytic + numerical theory | Self-correcting quantum memory |
| E03 | [Absence of Quantum Time Crystals](https://doi.org/10.1103/PhysRevLett.114.251603) | Formal no-go theorem | Time-crystalline order |
| E04 | [Quantum Energy Teleportation in Spin Chain Systems](https://doi.org/10.1143/JPSJ.78.034001) | Theoretical model/protocol | Quantum energy teleportation |

## 4. Results by paper

### 4.1 N01 — SPARC Toroidal Field Model Coil

**Direct scoped claim**

A representative-scale REBCO toroidal-field model coil was designed, built and experimentally operated at approximately 20 T peak field on the conductor under the reported test conditions.

**V2 adapter**

Empirical + engineering.

**DBE application claim**

Can a compact high-field tokamak export dependable net electricity?

**Assessment**

The paper is direct evidence for a major magnet component and high-field engineering pathway. It is **not** direct evidence for whole-plant net electricity, plasma-axis field performance, blanket/exhaust viability, tritium sufficiency, availability, or economics.

**Framework result:** PASS WITH SCHEMA EXTENSION.

V1/V2 correctly prevent the application leap if claim scope is respected.

**Stress exposed:** SDBES lacks an explicit typed relation such as `COMPONENT_EVIDENCE_FOR` between the direct paper claim and the higher-level DBE application.

---

### 4.2 C02 — Self-Organizing Knotted Magnetic Structures in Plasma

**Direct scoped claim**

Under the modeled full-MHD conditions, initially helical configurations can relax into quasistable linked/knotted configurations with nested toroidal surfaces, with analytic approximations to the simulated structures.

**V2 adapter**

Numerical/simulation + formal/analytic.

**DBE application claim**

Can topology-informed magnetic design improve fusion confinement without unacceptable transport or control costs?

**Assessment**

The simulation is relevant mechanism evidence. It does not establish fusion-grade confinement, favorable transport, device realizability, or a net-energy benefit.

**Framework result:** PASS WITH SCHEMA EXTENSION.

V2's simulation adapter correctly separates numerical behavior from physical validation.

**Stress exposed:** the schema needs an explicit simulation-to-world correspondence field and a typed `MECHANISM_SEED_FOR` or `MODEL_EVIDENCE_FOR` application relation.

---

### 4.3 C09 — Superabsorption / quantum battery

**Direct scoped claim**

The reported organic-microcavity experiment demonstrates collective/superextensive charging behavior and energy storage dynamics in the tested system, consistent with the study's theoretical modeling.

**V2 adapter**

Empirical + numerical/formal model.

**DBE application claim**

Can collective quantum effects improve useful storage service after charging, retention, discharge and wall-plug losses are counted?

**Assessment**

The paper demonstrates a charging/storage mechanism. It does not establish a useful repeated battery cycle, efficient extraction of electrical work, long retention, or competitive system-level storage.

**Framework result:** PASS WITH SCHEMA EXTENSION.

**Stress exposed:** a prototype/component result needs an explicit demonstration context and translation distance to an integrated capability.

---

### 4.4 I01 — Deep reinforcement learning for tearing-instability avoidance

**Direct scoped claim**

A learned predictive/control workflow was experimentally used on DIII-D to steer plasma operation while avoiding tearing instability within the tested regime.

**V2 adapter**

Empirical + causal/intervention + bounded engineering control.

**DBE application claim**

Can learned controllers improve plasma performance and robustness against defined baselines?

**Assessment**

This is the cleanest direct match in the ten-paper set: the source directly supports a bounded AI-assisted plasma-control claim. Generalization to other devices, operating regimes, complete reactor control, or net-electricity improvement remains unresolved.

**Framework result:** PASS.

V2 cleanly separates the demonstrated intervention from AGI, universal reactor control and downstream power-plant claims.

**Stress exposed:** generalization needs a first-class assessment status rather than being hidden in notes.

---

### 4.5 I02 — Scaling deep learning for materials discovery

**Direct scoped claim**

The study demonstrates large-scale computational prediction of candidate stable crystal structures using learned models and first-principles calculations, with a subset connected to experimental realization.

**V2 adapter**

Computational + empirical cross-check.

**DBE application claim**

Can AI-guided candidate discovery increase the rate of independently verified, useful materials relevant to energy technologies?

**Assessment**

The computational discovery result is strong evidence for candidate-generation capability. It does not by itself establish synthesis feasibility, novelty in every case, service-condition stability, manufacturability, useful energy properties, or superiority per total experimental resource budget.

**Framework result:** PASS WITH SCHEMA EXTENSION.

**Stress exposed:** the DBE application is a chain:

```text
candidate prediction
→ synthesis
→ identification
→ independent verification
→ useful property
→ manufacturability
→ deployment
```

V2 can scope each claim but currently lacks an explicit claim-decomposition/composite-claim structure.

---

### 4.6 I03 — Autonomous laboratory for inorganic materials

**Direct scoped claim**

The corrected article reports that the autonomous A-Lab workflow realized 36 compounds from 57 targets during the reported campaign. The 2026 correction narrowed novelty language and reanalyzed diffraction assignments; a 2024 PRX Energy critique identified serious issues in the original novelty and phase-identification claims.

**V2 adapter**

Empirical + engineering workflow + revision/conflict handling.

**DBE application claim**

Can closed-loop autonomous laboratories produce reproducible discoveries more efficiently than strong baselines?

**Assessment**

This paper is the strongest V2 version-control stress test. The autonomous workflow itself remains evidence of bounded laboratory automation, while broader claims about novelty and autonomous identification required correction and remain sensitive to independent validation.

**Framework result:** PASS, BUT SCHEMA AMENDMENT REQUIRED.

V2's append-oriented correction model is conceptually correct.

**Stress exposed:**

1. correction and critique can affect only particular claims, not the entire paper;
2. an assessment needs a formal `SUPERSEDES`, `CORRECTS`, or `CHALLENGES` relationship to another assessment;
3. source-reported status must be distinguishable from SDBES-verified status in machine-readable form.

---

### 4.7 I04 — Quantum error correction below threshold

**Direct scoped claim**

The reported superconducting surface-code memories operate below threshold in the tested regime, with logical-error suppression as code distance increases and real-time decoding demonstrated. A 2026 publisher correction applies to a Figure 3 label.

**V2 adapter**

Empirical quantum-hardware + engineering demonstration.

**DBE application claim**

Can improved error correction and decoding reduce the logical error and total overhead enough for useful fault-tolerant quantum computation and downstream scientific simulation?

**Assessment**

The experiment directly supports below-threshold logical-memory progress. It does not establish a large fault-tolerant computer, practical quantum chemistry, or favorable total energy/refrigeration overhead.

**Framework result:** PASS WITH SCHEMA EXTENSION.

**Stress exposed:** the atlas-level claim bundles several sequential capabilities. V2 needs composite-claim decomposition and demonstration-context fields.

---

### 4.8 I07 — Quantum self-correction in the 3D cubic code model

**Direct scoped claim**

For the specified 3D cubic-code model and assumptions, the paper provides analytic and numerical evidence for a finite-size/temperature-dependent increase in memory lifetime, including a proved lower bound in the stated regime.

**V2 adapter**

Formal + numerical.

**DBE application claim**

Can fracton/self-correcting memories provide practically useful finite-temperature quantum storage at realistic hardware cost?

**Assessment**

The formal/model result is directly relevant to the theoretical mechanism. It does not establish an implementable material/device, indefinite storage, realistic many-body interactions, or competitive hardware cost.

**Framework result:** PASS.

V2 handles the separation of theorem/model validity, assumptions and physical correspondence well.

**Stress exposed:** theory papers need a more precise subtype distinguishing `THEOREM`, `BOUND`, `MODEL_RESULT`, and `NUMERICAL_EVIDENCE`.

---

### 4.9 E03 — Absence of Quantum Time Crystals

**Direct scoped claim**

Under the paper's definition and stated assumptions, a no-go theorem rules out the specified equilibrium time-crystal behavior in ground states or canonical ensembles for sufficiently short-range Hamiltonians.

**V2 adapter**

Formal theorem.

**DBE application claim**

Can driven/Floquet time-crystalline phases provide useful synchronization or reliability?

**Assessment**

The paper constrains an equilibrium formulation. It does **not** refute driven Floquet time crystals or every open/non-equilibrium construction.

**Framework result:** STRONG PASS.

This directly validates V2's scope-mismatch and universal-claim rules. A negative theorem can be strong formal evidence without becoming a universal refutation outside its assumptions.

**Stress exposed:** no material schema failure.

---

### 4.10 E04 — Quantum energy teleportation in spin chains

**Direct scoped claim**

Within the specified spin-chain model, local operations, classical communication and ground-state correlations permit energy injected/handled at one region to enable extractable energy at a distant region while respecting causality and local energy conservation.

**V2 adapter**

Theoretical model/protocol.

**DBE application claim**

Can QET provide a useful energy-control or information function after preparation, measurement, communication, reset and extraction costs are included?

**Assessment**

The theory paper supports existence of a model protocol. It does not establish free energy, superluminal energy transfer, a favorable complete energy balance, or practical hardware utility.

**Framework result:** PASS WITH SCHEMA EXTENSION.

**Stress exposed:** V2 needs an explicit distinction between a theoretical existence/model claim and a practical capability claim. This directly supports the proposed V3 addition of a first-class Capability/Condition object.

---

## 5. Acceptance-test coverage

The 10-paper corpus exercises most V2 acceptance cases.

| V2 acceptance case | Tested? | Example |
|---|---:|---|
| Duplicate / non-independent reporting | Partial | I03 original + correction; I04 original + correction |
| Strong negative evidence | Partial | I03 external challenge; E03 formal no-go |
| Scope mismatch | Yes | E03 equilibrium no-go vs driven Floquet application |
| Simulation without physical validation | Yes | C02 |
| Speculative idea with no evidence | No | This corpus intentionally used papers |
| Corrected publication | Yes | I03, I04 |
| Components without integrated system | Yes | N01, C09, I04 |
| Universal mathematical counterexample/no-go logic | Yes | E03 theorem case |

**Coverage conclusion:** the paper test does not replace the remaining synthetic acceptance tests. In particular, SDBES still needs a clean case of an evidence-free idea and a strong empirical refutation.

## 6. V1/V2 failure-mode findings

### P0 — none observed

No case required:

- adding incomparable numeric types,
- converting a rubric score into probability,
- treating a simulation as physical proof,
- treating an application-level claim as established merely because a component paper exists,
- or treating a scoped no-go theorem as universal beyond its assumptions.

The central V1/V2 safety invariants survived.

### P1-1 — Missing typed Result/Claim → DBE Application relation

This appeared in at least 8/10 papers.

A source can be:

- direct evidence for a claim,
- component evidence,
- mechanism seed,
- model evidence,
- background,
- constraint,
- scope limit,
- counterexample,
- or merely adjacent.

The current schema relies too heavily on prose `scope_match`.

**Required amendment**

Add a typed relation such as:

```text
DIRECT_EVIDENCE_FOR
COMPONENT_EVIDENCE_FOR
MECHANISM_SEED_FOR
MODEL_EVIDENCE_FOR
CONSTRAINT_ON
SCOPE_LIMIT_ON
COUNTEREXAMPLE_TO
BACKGROUND_FOR
ADJACENT_TO
```

This relation must itself carry scope and provenance.

### P1-2 — Composite application claims need decomposition

This appeared clearly in N01, I02, I04 and E04.

A high-level DBE proposition often bundles several required stages.

Example:

```text
quantum error correction
→ fault-tolerant machine
→ useful simulation
→ faster scientific discovery
→ relevant energy breakthrough
```

V2 can evaluate each statement but does not yet represent that decomposition structurally.

**Required amendment**

Create explicit subclaims and defer their dependency structure to V3.

### P1-3 — 3×3 F/E/A cells are under-specified as single values

The paper test shows that one cell needs several independent properties:

```text
applicability
evidence availability
criterion outcome
verification provenance
scope
```

For example, independent replication may be applicable but unassessed; that is different from absent, failed, or irrelevant.

**Required amendment**

A matrix cell should be a structured object rather than a bare scalar/status.

Suggested form:

```json
{
  "applicability": "APPLICABLE",
  "availability": "PRESENT",
  "outcome": "MEETS|DOES_NOT_MEET|INCONCLUSIVE|UNKNOWN",
  "verification": "SOURCE_REPORTED|SDBES_SCREENED|INDEPENDENTLY_REPRODUCED",
  "scope": "..."
}
```

A visualization may derive a compact symbol from this object, but the ledger must retain all fields.

### P1-4 — Assessment-to-assessment provenance is required

I03 shows that source-level versioning is not enough.

A correction may change only one claim while leaving another result intact. An external critique may challenge only novelty or identification while agreeing that the robotic workflow physically operated.

**Required amendment**

Claim Assessments need relationships:

```text
SUPERSEDES
CORRECTS
CHALLENGES
NARROWS
REANALYZES
REPLICATES
FAILS_TO_REPLICATE
```

### P1-5 — Reported versus independently checked state needs an explicit field

This appeared in all ten papers because the Phase-1 source library generally contains abstract/official-summary screening rather than independent reproduction.

**Required amendment**

Every important state needs an epistemic provenance such as:

```text
SOURCE_REPORTED
SOURCE_TEXT_SCREENED
SDBES_DERIVATION_CHECKED
SDBES_DATA_REANALYZED
INDEPENDENT_REPLICATION_CONFIRMED
FORMALLY_MACHINE_CHECKED
```

SDBES must not display `SIMULATION_VERIFIED`, `FORMALLY_PROVED`, or `REPLICATED` without saying **by whom and by what procedure**.

### P1-6 — Demonstration context / integration level should be first-class

N01, C09, I01, I03 and I04 all demonstrate real systems at very different levels.

A universal TRL score would be too coarse for the epistemic ledger, but SDBES needs structured context such as:

```text
model
simulation
bench experiment
component prototype
integrated subsystem
full system
operational deployment
```

plus the actual environment and scale.

This is descriptive, not a probability of commercial success.

### P2 — Theory subtype

The theory cases differ substantially:

- I07 contains analytic bounds + numerical evidence.
- E03 is a no-go theorem under explicit assumptions.
- E04 is an existence/model protocol.
- C02 mixes simulation with analytic approximation.

Add:

```text
THEOREM
NO_GO_THEOREM
BOUND
MODEL_EXISTENCE_RESULT
ANALYTIC_APPROXIMATION
NUMERICAL_EVIDENCE
CONJECTURE
```

as non-exclusive formal-result descriptors.

## 7. F/E/A scoring decision

**No numeric F/E/A scores were assigned in this test.**

That is an intentional success condition, not missing work.

The Phase-1 records were mostly screened at abstract/official-summary depth, and V1 explicitly prohibits converting incomplete qualitative screening into false quantitative confidence.

For the 10-paper pilot, SDBES can determine:

- which F/E/A dimensions are applicable,
- what evidence is present,
- what is unassessed,
- and what the paper directly demonstrates,

without claiming calibrated numeric confidence.

Numeric rubric values should wait for a rubric with demonstrated inter-rater behavior and sufficiently deep source review.

## 8. What the test says about the proposed V3

The test strengthens the proposed V3 architecture.

The clearest repeated problem is that:

```text
a paper's direct claim
≠
the capability needed by the DBE application
```

Examples:

- a 20 T model coil ≠ a net-electric fusion plant;
- superabsorption ≠ useful cyclic grid storage;
- below-threshold logical memory ≠ fault-tolerant quantum chemistry;
- a QET protocol ≠ useful energy transmission;
- MHD knot simulation ≠ fusion-grade topological confinement.

Therefore the proposed V3 **Capability / Condition** object is not optional decoration. It is the cleanest way to separate:

```text
what evidence says
from
what a technological pathway requires
```

The paper test also supports separate:

[
D^K=	ext{epistemic dependency}
]

and:

[
D^X=	ext{structural/capability dependency}
]

because theoretical assumptions and physical prerequisites repeatedly differ.

## 9. V3 changes recommended before Pro review

Carry the following into the V3 review candidate:

1. **Capability/Condition object stays.**
2. **Two dependency layers (D^K) and (D^X) stay.**
3. Add a typed **Evidence/Claim → Application/Capability relevance edge**.
4. Add **composite-claim decomposition** before structural gates are computed.
5. Add **assessment provenance/version edges** so corrected/challenged claims do not contaminate unaffected claims.
6. Make **three-valued structural logic** explicit: TRUE / FALSE / UNKNOWN.
7. Keep minimal path sets, minimal cut sets and dominators as structural diagnostics rather than truth scores.
8. Add demonstration context so structural reasoning knows whether evidence concerns a model, component, integrated system or deployment.

## 10. Verdict

### V1

**PASS WITH AMENDMENTS.**

The typed-number rules, provenance principles, separation of support/refutation, and knowledge/world distinction survived the 10-paper corpus.

### V2

**PASS WITH AMENDMENTS.**

The claim adapters and scoped assessment model correctly prevented the most important overclaims. The test exposed missing machine-readable relations and provenance, not a collapse of the epistemic architecture.

### Gate to V3

**READY FOR V3 PRO REVIEW AFTER INCORPORATING THE SIX P1 SCHEMA AMENDMENTS ABOVE.**

The 10-paper test supports moving forward; it does not support skipping claim decomposition or Capability/Condition modeling.

---

## Source corpus

Phase-1 research files:

- [DBE Research Atlas](https://github.com/pjrny/DBE_V0/blob/dimensions-beyond-energy/docs/research/phase1/DBE_RESEARCH_ATLAS.md)
- [Source Library](https://github.com/pjrny/DBE_V0/blob/dimensions-beyond-energy/docs/research/phase1/SOURCE_LIBRARY.md)

Framework:

- [SDBES V1](https://github.com/pjrny/DBE_V0/blob/SDBES/docs/SDBES/V1_TYPED_EVIDENCE_DEPENDENCY_LEDGER.md)
- [SDBES V2](https://github.com/pjrny/DBE_V0/blob/SDBES/docs/SDBES/V2_CLAIM_EVALUATION_RULES.md)

Known correction/challenge records used in the stress test:

- [A-Lab Author Correction (2026)](https://doi.org/10.1038/s41586-025-09992-y)
- [Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis](https://doi.org/10.1103/PRXEnergy.3.011002)
- [Quantum error correction Author Correction (2026)](https://doi.org/10.1038/s41586-026-10559-8)
