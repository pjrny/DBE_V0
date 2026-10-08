# SDBES V1 — Typed Evidence & Dependency Ledger

**Project:** SDBES — Search for Dimensions Beyond Energy Scarcity  
**Repository:** pjrny/DBE_V0  
**Branch:** SDBES  
**Status:** Historical design baseline preserved for version control  
**Derived from:** DBE framework work through the v0.10 mathematical-audit revision

## 1. Purpose

SDBES is a research ledger and future simulation architecture for organizing, comparing, and connecting scientific claims relevant to the search for conditions, technologies, and discoveries that could move civilization beyond binding energy scarcity.

The core design principle is:

> **Preserve information first. Aggregate second. Simulate last.**

The system must distinguish evidence quality, evidence direction, structural importance, causal influence, uncertainty, and probability rather than collapsing them into one score.

## 2. Canonical hierarchy

```text
SDBES / DBE
└── Domain
    └── Focus Area
        └── Concept
            └── Claim
                └── Evidence Object
```

Examples of domains and focus areas include fusion, quantum computing, materials, AI/scientific discovery, storage, topology, control systems, and other areas that may alter energy constraints directly or indirectly.

### Evidence Object

An Evidence Object may be a:

- paper
- experiment
- dataset
- theorem
- proof
- simulation
- prototype
- benchmark
- deployed system
- engineering failure
- replication
- meta-analysis
- technical report

A paper is therefore not necessarily the lowest scientific unit.

## 3. Typed numbers rule

Every numeric value must have a declared mathematical meaning.

A number such as `0.8` cannot interchangeably mean:

- 80% probability that a claim is true
- high methodological quality
- strong structural dependency
- strong causal effect
- semantic similarity
- graph centrality

The first invariant of V1 is therefore:

```text
same numerical range ≠ same mathematical type
```

Minimum numeric types:

| Type | Meaning |
|---|---|
| rubric_rating | Descriptive assessment against a rubric |
| evidence_polarity | Direction of a result relative to a claim |
| probability | Probability under an explicitly specified model |
| dependency_index | Structural dependency strength |
| causal/effect coefficient | Defined response under a specified model |
| similarity | Semantic or mathematical similarity |
| centrality | Graph-structural prominence |

Undefined cross-type arithmetic is prohibited.

## 4. Descriptive 3×3 evidence matrix

The original visualization is retained as a descriptive evidence profile:

[
E_i=
\begin{bmatrix}
F_V & F_I & F_G\\
E_V & E_I & E_G\\
A_V & A_I & A_G
\end{bmatrix}
]

Rows:

- **F** — Formal / Mathematical
- **E** — Empirical / Experimental
- **A** — Applied / Engineering

Columns:

- **V** — Validated within the relevant methodology
- **I** — Independently checked / replicated / implemented
- **G** — Generalized beyond a narrow regime, dataset, assumption set, or implementation

This matrix is a **profile**, not a truth-probability calculator.

## 5. Applicability and missingness

A missing method must never automatically reduce a paper's quality.

V1 requires explicit states rather than a simple zero:

```text
N/A       genuinely irrelevant
UNKNOWN   not yet assessed
ABSENT    relevant evidence should exist but is absent
PRESENT   relevant evidence exists
FAILED    criterion was tested and not met
```

This prevents, for example, unattempted replication from being confused with irrelevant replication.

## 6. Quality and polarity are separate

Formal, empirical, and applied quality are nonnegative descriptive dimensions.

[
F,E,A \in [0,1]
]

Evidence direction relative to a claim is separate:

[
p_{ic}\in[-1,+1]
]

where negative values refute/challenge the scoped claim and positive values support it.

A rigorous experiment that falsifies a hypothesis can therefore have:

[
E\approx1,qquad p\approx-1
]

This preserves the distinction:

```text
quality ≠ direction
```

## 7. Support and refutation remain separate

For each claim, supporting and refuting evidence must remain distinguishable.

A descriptive aggregate may retain:

[
S_c
]

for support and:

[
R_c
]

for refutation.

A net balance may be displayed, but the original components must never be destroyed.

This is required because:

- no evidence
- large amounts of balanced contradictory evidence

can both produce a net value near zero but mean radically different things.

## 8. Evidence lineage and duplication

Reports, studies, observations, and datasets are not interchangeable.

The schema must be capable of distinguishing:

```text
Source document/version
→ Study / proof / system
→ Result / observation
→ Claim-specific assessment
```

A duplicated publication does not create duplicated evidence.

Lineage may include:

- shared dataset
- same experiment
- overlapping sample
- same model
- same research group
- derivative paper
- independent replication

No fixed positive redundancy discount is sufficient by itself to guarantee duplication invariance.

## 9. Claims require explicit scope

A claim must eventually contain enough structure to determine whether apparently conflicting evidence actually addresses the same proposition.

Minimum conceptual fields:

```text
claim_id
statement
claim type
quantifier / logical form
conditions
variables
units
endpoint
baseline/comparator
scope
time horizon
```

A result at condition A does not automatically contradict a result at condition B.

## 10. Mathematical methods and rigor are separate

A method vector records **what mathematics is used**:

[
\vec M=[m_1,m_2,\ldots,m_n]
]

Possible methods:

- linear algebra
- differential equations
- PDEs
- probability
- Bayesian inference
- statistics
- optimization
- information theory
- graph theory
- group theory
- topology
- tensor analysis
- geometric algebra
- control theory
- numerical methods
- dynamical systems
- formal logic

This does not measure quality.

Separate diagnostics assess:

- derivation validity
- assumption integrity
- domain validity
- sensitivity robustness
- numerical reproducibility
- formal verification status

## 11. Formal reasoning rule

A valid proof under stated assumptions establishes a formal result under those assumptions. It does not automatically establish physical truth.

SDBES separates:

```text
proof validity
assumption validity
empirical correspondence
```

Failure of a proof route also does not automatically prove the conclusion false.

If:

[
A\Rightarrow C
]

and (A) is false, it does not follow that (C) is false.

This requires dependency typing.

## 12. Dependency network

Dependency is separate from evidence support.

A generic dependency edge must not erase logical distinctions. V1 identifies at least:

- premise of derivation
- necessary prerequisite
- sufficient condition
- enabler
- accelerator
- constraint
- substitute
- alternative route

A dependency index is **not a probability**.

Candidate dependencies should be generated from explicit assumptions, citations, mechanisms, technical roadmaps, semantic relationships, and expert analysis rather than exhaustively comparing every pair of nodes.

## 13. Joint prerequisites

Pairwise edges are insufficient when a target requires combinations such as:

[
A\land B\land C\Rightarrow D
]

or alternatives such as:

[
A\lor B\Rightarrow D
]

The ledger must eventually support:

- ALL / AND
- ANY / OR
- k-of-n
- threshold or explicit functional gates

The data semantics are required before sophisticated hypergraph visualization.

## 14. Structural importance and pillars

A claim may be structurally important if many downstream claims depend on it, especially if those claims are themselves important.

Graph tools may include:

- downstream reach
- betweenness
- Katz-style centrality
- eigenvector centrality where appropriate
- substitutability
- cross-domain reach

A graph centrality score must never be interpreted as truth.

Circular dependency clusters must be detected explicitly.

## 15. Influence network

Influence asks:

> If one variable or capability changes, what changes elsewhere?

This differs from dependency.

Influence relationships must distinguish:

- association
- hypothesized influence
- mechanistic link
- causal effect

Only appropriately defined causal relationships may later be used as causal simulator coefficients.

## 16. Matrix convention

For a column state vector, SDBES adopts:

[
W_{ji}=\text{effect from source }i\text{ to destination }j
]

so that a defined linear transition may use:

[
x_{t+1}=Wx_t
]

when, and only when, the entries have compatible mathematical meanings.

## 17. Matrix powers and path discovery

[
W^2,W^3,\ldots
]

may identify multi-hop candidate pathways.

They do not automatically establish:

- causal relationships
- probabilities
- independent evidence
- physically meaningful net effects

Therefore the correct language is:

```text
two-hop candidate pathway
three-hop candidate pathway
...
```

## 18. Eigenanalysis

Eigenvectors and eigenvalues are retained for appropriate uses:

- feedback modes
- linear dynamical modes
- stability analysis
- selected centrality definitions

They are not universal path detectors.

Strong directed acyclic pathways may have zero eigenvalues.

## 19. Knowledge state and world state

One of the core SDBES invariants is:

[
K(t)\neq X(t)
]

where:

- (K(t)) = what SDBES currently knows or believes
- (X(t)) = modeled physical or technological state

A new paper can change (K(t)) without changing physical reality.

## 20. Bitemporal provenance

Each record should preserve:

- event / valid time
- knowledge / ingestion time
- publication date
- experiment date
- revision date
- superseded-by relationships
- correction / retraction status

The ledger should normally be append-only so historical knowledge states can be reconstructed.

## 21. Engines

### Epistemic Engine

Question:

> What evidence exists and what does it justify believing?

### Structural Engine

Question:

> What depends on what and where are the structural bottlenecks?

### Dynamic / Causal Engine

Question:

> Under an explicitly defined model, what changes if something changes?

### Future Discovery Engine

Question:

> What relationships, gaps, bridges, conflicts, and high-value unknowns should researchers investigate next?

## 22. Core invariants

SDBES must preserve:

[
Quality\neq Direction
]

[
Importance\neq Certainty
]

[
EvidenceVolume\neq Consensus
]

[
EvidenceScore\neq Probability
]

[
Association\neq Causation
]

[
DerivationDependency\neq PhysicalNecessity
]

[
KnowledgeState\neq WorldState
]

[
VisualizationAggregation\neq MathematicalEquivalence
]

## 23. Visualization baseline

Planned linked views:

1. **Knowledge Universe** — Domain → Focus Area → Concept → Claim → Result / Evidence
2. **Evidence Space** — Formal / Empirical / Applied profile
3. **Dependency Architecture** — prerequisites, alternatives, pillars, bottlenecks
4. **Influence View** — association, mechanism, causal and hypothetical edges
5. **Time / Simulation View** — historical knowledge state and future scenarios

Glyphs may encode:

- area/volume → defined evidence quantity
- green/red portions → support/refutation
- opacity → assessment certainty or data-quality state
- halo → disagreement
- edge width → defined magnitude
- edge opacity/style → relationship confidence/type

Visual encodings are not permitted to imply mathematical meanings that the ledger has not established.

## 24. Status

V1 is retained as the typed-ledger baseline. V2 advances from schema safety into explicit claim-evaluation rules.
