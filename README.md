# SDBES — Search for Dimensions Beyond Energy Scarcity

This branch is the continuously versioned framework branch for **SDBES: the Search for Dimensions Beyond Energy Scarcity**.

It grows out of the DBE project but has a different job from the repository's simulation and paper-research branches: **SDBES defines the evidence ledger, claim taxonomy, dependency mathematics, visualization grammar, and eventual simulation rules used to organize and connect the research.**

## Why this branch exists

Other branches in this repository are being used to explore or collect research in areas such as:

- ignition-barrier / fusion research
- nuclear fusion
- topology and advanced mathematics
- quantum computing
- research-grade physics
- ongoing observatory/research pulls

The `SDBES` branch is intended to become the **common framework those research streams can eventually feed into**.

It should not treat a paper count as knowledge, a graph score as truth, or a speculative relationship as a causal law.

## Thread summary

The framework began with a visualization idea:

- classify papers and concepts by scientific field
- represent mathematical, empirical, and applied confidence in a visual matrix/vector
- allow evidence supporting and refuting a claim to interact
- identify "pillar" claims that many other claims depend upon
- connect apparently separate research areas such as AI, quantum computing, materials, and fusion
- use matrix powers to expose possible bridge pathways
- eventually simulate how breakthroughs, failures, or bottlenecks propagate across the network
- visualize the entire system in linked 2D/3D views using glyph size, color, opacity, edge width, animation, and time

The framework was then stress-tested for mathematical failure modes.

That review preserved the overall architecture but changed several critical assumptions:

1. **Evidence quality and evidence direction must be separate.**
2. **A score in [0,1] is not automatically a probability.**
3. **Formal, empirical, and engineering evidence establish different things.**
4. **A paper is not necessarily one independent unit of evidence.**
5. **Claims require explicit scope before evidence can truly support or refute them.**
6. **Dependency, causation, similarity, and graph importance require different mathematical types.**
7. **A failed derivation premise does not automatically falsify a conclusion.**
8. **AND/OR and alternative pathways must be represented explicitly.**
9. **Matrix powers expose walks/candidate pathways, not automatic causal effects.**
10. **Eigenvectors are useful for selected dynamical/structural questions but are not universal pathway detectors.**
11. **What the project knows and what physical reality is doing are separate states.**
12. **Time and revision history must be preserved from the beginning.**

## Version history on this branch

### V1 — Typed Evidence & Dependency Ledger

File:

- `docs/SDBES/V1_TYPED_EVIDENCE_DEPENDENCY_LEDGER.md`

Defines the safe mathematical architecture, typed values, evidence profile, dependencies, influence layers, time, graph rules, and project invariants.

### V2 — Claim Evaluation Rules

File:

- `docs/SDBES/V2_CLAIM_EVALUATION_RULES.md`

Defines how individual claims are specified and how formal, empirical, numerical, engineering, causal, and forecast claims are evaluated without forcing them through one universal confidence formula.

### V3 — Dependency Mathematics & Structural Semantics

Files:

- `docs/SDBES/V3_DEPENDENCY_MATHEMATICS_STRUCTURAL_SEMANTICS.md`
- `docs/SDBES/V3_STRUCTURAL_SCHEMA_TEMPLATE.json`
- `tests/sdbes_v3_core_logic_checks.py`

V3 was formalized after the V1/V2 10-paper stress test and Pro mathematical review. It introduces Structural Predicates, Structural Assessments, typed translation links, epistemic versus structural dependency layers, gate-aware ALL/ANY/k-of-n semantics, four-valued knowledge state, three-valued scenario state, alternative routes, minimal path/cut analysis, SCC/bootstrap handling, and snapshot-versioned structural diagnostics.

The required core-logic verification passed with `ALL_CHECKS_PASSED`.

V4 is next and must preserve the V3 invariant:

```text
Structural Requirement ≠ Causal Effect
```

## Development sequence

Current planned sequence:

```text
V1  Typed ledger and mathematical safety rules
V2  Claim evaluation rules
V3  Dependency mathematics and structural semantics — committed
V4  Influence, causality & dynamic-state semantics — next
V5  Glyphs and linked visualization system
V6  Real-paper pilot
V7  Failure-mode and consistency tests at scale
V8  Probabilistic inference layer
V9  Early simulation layer
V1.0 Validated research platform milestone
```

Version labels here describe SDBES framework progression. They do not imply that the underlying scientific claims have been validated.

## Pilot strategy

The framework should be tested in stages rather than waiting for a perfect schema.

### Design examples

Use a small diverse set of real papers/results to challenge the schema while it is still changing.

Target: approximately **3–5 source papers** yielding **10–20 useful scoped claims**, chosen for diversity rather than quantity.

### Operational pilot

After the schema and dependency/influence rules stabilize, expand toward approximately **100 reviewed, scoped claims** across several research areas.

The unit counted should be the **reviewed claim**, while papers, studies, results, concepts, and ideas remain separate counts.

## Fundamental SDBES rule

> **Preserve the source and meaning of every value before aggregating it.**

The long-term objective is not merely a literature database. It is a research-navigation and scenario-analysis system capable of showing:

- what is known
- what is uncertain
- what contradicts what
- what depends upon what
- where the bottlenecks are
- which unresolved claims have large downstream consequences
- which cross-field pathways deserve investigation
- and, only when a defensible causal model exists, what may happen under defined interventions

## Relationship to the existing DBE simulator

The repository's existing simulator on `main` explores a specific fusion/DBE implementation and explicitly uses simplified models.

SDBES is a broader evidence and research architecture. It should eventually be capable of evaluating and contextualizing models like the existing simulator rather than inheriting their assumptions as established facts.

For the original repository simulator documentation, see the `main` branch.
