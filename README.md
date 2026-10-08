# Dimensions Beyond Energy (DBE)

## The Search for a Civilization Beyond Energy Scarcity

> **Core question:** What physically permissible discovery, technology, combination of technologies, or transformation of civilization could make energy cease to be a binding constraint on intelligent life?

## Purpose of this branch

The `dimensions-beyond-energy` branch is the broad **concept-discovery and source-gathering layer** of DBE.

Its job is to search widely across established engineering, frontier science, speculative physics, computation, civilization-scale demand reduction, and unknown mechanisms without prematurely collapsing unlike ideas into a single score.

This branch now contains the first large **DBE Concept Atlas** and its supporting research library.

### Phase 1 research set

- **90 candidate concepts**
- **81 annotated source records**
- **19 software repositories**
- **11 research/data portals**
- **19 candidates explicitly marked as background-only or adjacent-source coverage**

Files:

- [DBE Concept Atlas — Phase 1](docs/research/phase1/DBE_RESEARCH_ATLAS.md)
- [Annotated Source Library](docs/research/phase1/SOURCE_LIBRARY.md)
- [Search Coverage & Gaps](docs/research/phase1/SEARCH_AND_GAPS.md)

The web-readable abstract interface remains in [`index.html`](./index.html).

---

## Abstract

DBE is a broad, continuously updated research program for mapping the scientific and technological search space around one civilization-scale objective: making energy and resource scarcity cease to be meaningful constraints on intelligent life.

It is not limited to a single reactor design, energy source, or engineering discipline. Instead, DBE deliberately spans near-term engineering, frontier physics, computation, materials science, intelligence amplification, and transformations in the physical requirements of civilization itself.

The project does not assume that literally unlimited energy is attainable under known thermodynamics. Its target is broader and more practical: **effectively inexhaustible accessible energy, radically improved conversion and use of energy, discovery of presently inaccessible reservoirs or interactions, or sufficiently reduced energy demand that scarcity becomes non-binding.**

A successful pathway may therefore:

- increase the amount of accessible useful energy,
- improve conversion, storage, transport, or control,
- uncover a previously inaccessible reservoir or interaction,
- reduce the energy required for computation or civilization,
- or combine several of these effects.

Candidate concepts include fusion and advanced fission, geothermal and solar systems, superconductivity and magnetic-field engineering, quantum and emergent materials, quasiparticles, quantum thermodynamics, antimatter, nuclear isomers, weakly interacting or hidden particles, vacuum and zero-point phenomena, black-hole and gravitational physics, reversible and neuromorphic computation, brain emulation and consciousness science, AI and AGI-assisted discovery, quantum computing, autonomous laboratories, and currently unknown particles, fields, phases of matter, interactions, or physical principles.

**Inclusion is not endorsement.**

---

# Classification: DBE discovery tags vs. SDBES scientific assessment

The original DBE abstract used broad evidence classes such as:

- **Demonstrated pathway**
- **Physics-compatible frontier**
- **Speculative / unknown physics**
- **Conflicts with established constraints**

Those labels remain useful as **discovery-stage tags**, especially when surveying dozens of concepts quickly.

However, after reviewing the SDBES framework, they are **not sufficient as the canonical scientific classification system**.

The SDBES branch establishes a stricter rule:

> **Preserve information first. Aggregate second. Simulate last.**

DBE discovery tags therefore answer:

> *What kind of candidate are we looking at?*

SDBES claim assessment answers:

> *What exactly is being claimed, what evidence bears on that claim, under what scope, and what does that evidence actually justify?*

These are different tasks.

---

## Canonical hierarchy

The SDBES framework organizes knowledge as:

```text
SDBES / DBE
└── Domain
    └── Focus Area
        └── Concept
            └── Claim
                └── Evidence Object
```

A **Concept** is not itself automatically true or false.

A concept may contain many claims with different evidentiary states.

Example:

```text
Concept: proton-boron fusion
├── Claim: p–B11 fusion reactions can occur in magnetically confined plasma
├── Claim: sufficient gain can be achieved for a practical reactor
├── Claim: direct charged-particle conversion can produce competitive electricity
└── Claim: a complete p–B11 system can operate economically at scale
```

Those claims may receive very different assessments.

---

# Core SDBES invariants adopted here

The `dimensions-beyond-energy` branch should follow these SDBES principles when concepts graduate from discovery into formal assessment:

```text
Quality ≠ Direction
Importance ≠ Certainty
Evidence Volume ≠ Consensus
Evidence Score ≠ Probability
Association ≠ Causation
Derivation Dependency ≠ Physical Necessity
Knowledge State ≠ World State
Visualization Aggregation ≠ Mathematical Equivalence
```

This prevents DBE from turning broad exploratory labels into false scientific precision.

---

## Evidence quality and evidence direction must remain separate

A rigorous experiment that refutes a claim can be **high-quality evidence with negative polarity**.

Likewise, a weak study supporting a claim does not become strong evidence merely because it points in the desired direction.

SDBES therefore separates:

- evidence quality,
- evidence polarity,
- replication,
- generalization,
- scope compatibility,
- independence,
- and formal validity.

---

## Formal, empirical, numerical, engineering, causal, and forecast claims are different

A single universal confidence formula is not appropriate.

SDBES uses different evaluation adapters for:

- **Formal / mathematical claims**
- **Empirical / observational claims**
- **Numerical / simulation claims**
- **Engineering / feasibility claims**
- **Causal / intervention claims**
- **Forecast / predictive claims**

A reproduced simulation does not automatically validate physical reality.

A mathematically valid proof under assumptions does not establish that the assumptions describe nature.

A successful component does not automatically establish integrated-system feasibility.

---

## Claim states instead of one universal confidence percentage

SDBES allows multiple scoped states such as:

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

These are **not a single ordinal ladder**.

Multiple labels may apply simultaneously.

---

# How Phase 1 atlas tags should be interpreted

The Phase 1 atlas currently uses:

| Code | Discovery-stage meaning |
|---|---|
| **D** | Demonstrated bounded mechanism or technology |
| **P** | Physics-compatible frontier |
| **S** | Speculative capability or unknown physics |
| **X** | Conflicts with established constraints in the specified formulation |

These are provisional **concept-intake tags** only.

They are not:

- probabilities,
- truth scores,
- engineering-readiness levels,
- measures of importance,
- measures of popularity,
- measures of causal effect,
- or substitutes for a Claim Assessment.

Formal DBE/SDBES evaluation happens only after a concept is decomposed into scoped claims.

---

# Evidence profile

The SDBES framework retains a descriptive 3×3 evidence profile:

```text
             Validated   Independent   Generalized
Formal           F_V          F_I           F_G
Empirical        E_V          E_I           E_G
Applied          A_V          A_I           A_G
```

This profile describes **what kind of evidence exists and how far it has progressed**.

It is not a truth-probability calculator.

Missing evidence must also preserve explicit state:

```text
N/A
UNKNOWN
ABSENT
PRESENT
FAILED
```

For example, lack of an independent replication should not be confused with a failed replication.

---

# Confidence and probability policy

DBE should avoid fabricating a universal “confidence score.”

A probability is permitted only when its origin is explicit, for example:

- Bayesian model
- statistical estimator
- reliability model
- calibrated forecast
- expert elicitation
- Monte Carlo model

When a probability exists, it should be interpretable as something like:

```text
P(H | D, M)
```

where:

- `H` = scoped proposition
- `D` = evidence
- `M` = model and assumptions

A rubric rating must never be silently converted into probability.

---

# Importance, tractability, and popularity remain separate

DBE still needs descriptive fields that help navigate the landscape, including:

- potential civilization-scale impact,
- strategic importance,
- research tractability,
- falsifiability,
- scientific attention,
- scalability,
- resource burden,
- environmental profile,
- AI/AGI leverage,
- quantum-computing leverage.

But these must remain mathematically distinct from evidence strength.

A concept can be:

- **important but uncertain,**
- **popular but weakly evidenced,**
- **strongly evidenced but low-impact,**
- **speculative but highly tractable,**
- or **physically plausible but engineering-intractable.**

That distinction is central to DBE.

---

# From concept discovery to research-grade work

DBE does not require a concept to become an engineering-ready technology before it deserves serious research.

Instead, there are two separate graduation gates.

## 1. Research-paper readiness

A concept can graduate into a research-grade paper when it has:

1. a clearly scoped research question,
2. explicit claim statements,
3. a defensible source corpus,
4. supporting and opposing evidence,
5. assumptions and boundary conditions,
6. competing hypotheses,
7. measurable outcomes or formal propositions,
8. falsification or decision criteria,
9. reproducible methods,
10. uncertainty and sensitivity treatment,
11. provenance and revision history,
12. conclusions that do not exceed the evidence.

A rigorous negative result, constraint analysis, or formal refutation can qualify.

## 2. Engineering readiness

Engineering development requires additional evidence:

- demonstrated critical mechanisms,
- integrated-system performance,
- complete energy/resource accounting,
- relevant-environment testing,
- reliability,
- safety,
- failure-mode analysis,
- scalability,
- lifecycle constraints,
- and comparison against alternatives.

**Paper readiness ≠ engineering readiness.**

---

# Relationship to SDBES

The two branches now have complementary roles.

## `dimensions-beyond-energy`

**Discovery landscape**

- find candidate concepts,
- broaden the search space,
- collect sources,
- identify gaps,
- preserve speculative ideas,
- record unusual cross-domain connections,
- generate candidate claims.

## `SDBES`

**Evidence and dependency framework**

- scope claims,
- construct Claim Assessments,
- preserve provenance,
- distinguish support from refutation,
- model evidence independence,
- define dependency semantics,
- later support graph analysis, visualization, inference, and simulation.

The Phase 1 atlas should therefore be treated as **input to SDBES**, not as a replacement for it.

---

# Current research branches

The Phase 1 atlas organizes candidates into six broad branches:

1. **Nuclear energy and fusion architectures**
2. **Planetary heat, solar, and renewable gradients**
3. **Magnetism, materials, conversion, and storage**
4. **Intelligence and discovery multipliers**
5. **Unconventional reservoirs and fundamental physics**
6. **Demand reduction, computation, and digital civilization**

These branches are organizational, not mutually exclusive physical categories.

A single concept may participate in several pathways.

---

# Long-term objective

DBE is intended to become a continuously updated search landscape capable of asking:

- What is known?
- What remains speculative?
- What has been contradicted?
- What is merely untested?
- Which results are independent?
- What depends on what?
- Which assumptions are carrying large portions of the landscape?
- Where are there alternative pathways?
- Which unknowns have unusually large downstream consequences?
- Which concepts are underexplored relative to their possible impact?
- Which cross-field combinations deserve dedicated research?
- Which claims are mature enough for research-grade papers?
- Which technologies are mature enough for engineering programs?

The purpose is not to make every idea look equally plausible.

The purpose is to make the entire search space **inspectable, falsifiable, updateable, and difficult to fool ourselves about**.

---

## Status

**Current stage:** broad concept discovery + source intake.

**Canonical assessment framework:** SDBES V1 Typed Evidence & Dependency Ledger + SDBES V2 Claim Evaluation Rules.

**Next DBE task:** convert selected atlas concepts into scoped claims and Claim Assessments suitable for the SDBES real-paper pilot.
