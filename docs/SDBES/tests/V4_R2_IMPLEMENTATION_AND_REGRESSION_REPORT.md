# SDBES V4 R2 — Implementation and Regression Report

**Run date:** 2026-10-09

**Target:** `pjrny/DBE_V0`, branch `SDBES`

**Baseline commit:** `a8278039cff8e4c13c225b982ecc63249e37b70a`

**New research papers introduced:** No

**Release gate:** PASS

## 1. What was implemented

R2 is represented at three levels:

1. Normative specification:
   `docs/SDBES/V4_R2_CAUSAL_DYNAMICS_MODEL_COMPOSITION.md`
2. Machine-readable template:
   `docs/SDBES/V4_R2_SCHEMA_TEMPLATE.json`
3. Dependency-free reference semantics:
   `sdbes/v4.py`

The executable layer covers the response family (A/B/E/G/H/D), ordered
finite-horizon propagation, variable-role/quantity-kind separation,
dimension/timebase closure, composition interfaces, V3 predicate
authorization, typed resource balances, use authorization, multi-fidelity
promotion, transfer, V2 Evidence Object wrapping, (K(t)/X(t)) separation,
research-test decisions, kill conditions, and milestone completion.

## 2. Frozen regression corpus

The run used only previously reviewed material:

- the existing ten-paper V1/V2 assessment set from the `SDBES` branch;
- the already used M2 internal burn-control result;
- Bus B offline compute;
- S-L2 barrier evasion;
- the (Q_{eng}\approx1000) ledger claim;
- the component-coupling/interface-contract case.

The exact frozen input and source commits are recorded in
`V1_V4_R2_EXISTING_CASES.json`.

## 3. Regression results

| Case | Prior conclusion | V4 R2 conclusion | Classification |
|---|---|---|---|
| N01 SPARC model coil | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| C02 knotted plasma | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| C09 quantum battery | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| I01 DIII-D RL control | PASS | PASS | EXPECTED_REFINEMENT |
| I02 materials discovery | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| I03 autonomous lab correction | PASS_SCHEMA_AMENDMENT_REQUIRED | PASS_SCHEMA_AMENDMENT_REQUIRED | UNCHANGED |
| I04 below-threshold QEC | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| I07 cubic-code model | PASS | PASS | EXPECTED_REFINEMENT |
| E03 time-crystal no-go | STRONG_PASS | STRONG_PASS | UNCHANGED |
| E04 quantum energy teleportation | PASS_WITH_SCHEMA_EXTENSION | PASS_WITH_SCHEMA_EXTENSION | EXPECTED_REFINEMENT |
| M2 internal burn control | DOES_NOT_CLOSE_M2 | DOES_NOT_CLOSE_M2 | EXPECTED_REFINEMENT |
| Bus B offline compute | NO_DIRECT_CAUSAL_PATH_TO_Q | NO_DIRECT_CAUSAL_PATH_TO_Q | EXPECTED_REFINEMENT |
| S-L2 barrier evasion | HOLD | HOLD | EXPECTED_REFINEMENT |
| Engineering gain 1000 | CUT_AS_OUTPUT_KEEP_AS_LEDGER_TEST | same | EXPECTED_REFINEMENT |
| Component coupling | NO_INTERFACE_NO_PILLAR | NO_INTERFACE_NO_PILLAR | EXPECTED_REFINEMENT |

Totals:

```text
EXPECTED_REFINEMENT     13
UNCHANGED                2
SCHEMA_ONLY_CHANGE       0
UNEXPECTED_REGRESSION    0
```

R2 changed no scientific verdict. It added explicit model-use, fidelity,
transfer, resource, and milestone boundaries around prior conclusions.

## 4. Important case interpretations

### M2 near-ignition burn control

The previous conclusion remains that the result does not close M2. R2 now
encodes it as a `SCENARIO_ONLY` 0-D precursor. A headline success rate no
greater than 5%, pure-PPO failure, hybrid partial performance, one learned
training seed, and the absence of profiles, MHD, and disruption physics cannot
promote to 1-D transport, profile/MHD, or machine validation.

### Bus B offline compute

The previous “no direct causal path to Q” conclusion remains. Offline compute
can change research state (K(t)). Physical state (X(t)) changes only after
an explicit chain through candidate design, experiment, validated engineering
change, and system intervention.

### S-L2 barrier evasion

The claim remains HOLD. R2 represents WKB/Volkov, finite-volume or
Crank–Nicolson, TDSE, finite-pulse, kinetic depletion, and experiment as a
fidelity ladder rather than averaging disagreements. The retained kill
condition is net enhancement below (2\times) thermal at reachable
field/intensity after hole-burning and instability losses.

### Engineering gain

(Q_{eng}\approx1000) remains cut as an output and retained only as a ledger
stress test. A strict result is blocked unless all required power and
conversion terms are dimensionally and temporally compatible and the plant
boundary closes.

### Component coupling

“No interface contract, no pillar” remains unchanged. R2 makes the interface
executable: semantic meaning, units, timebase, spatial aggregation, validity
domain, uncertainty propagation, resource ownership, double-counting, causal
direction, and failure behavior are all required.

## 5. Test results

### SDBES-scoped release checks

| Check | Result |
|---|---:|
| V3 core logic reference checks | PASS |
| V4 R2 executable acceptance checks | 13/13 PASS |
| Frozen V1→V4 regression cases | 15/15 PASS |
| Unexpected regressions | 0 |
| V4 R2 second-pass requirement audit | 8/8 PASS |
| SDBES pytest adapters | 3/3 PASS |
| V4 JSON artifacts parse | PASS |

### Legacy simulator suite

The complete inherited test suite reports 11 passed and 9 failed after R2.
The same nine failures reproduce at the untouched V3 baseline, where the
suite reports 9 passed and 9 failed. They are existing API/test mismatches in
the legacy DBE simulator:

- one `initialize_profiles` call-signature mismatch;
- three `HolographicEncoder(block_size=...)` mismatches through controller tests;
- one `FractonMemory.write` signature mismatch;
- one `TimeCrystalClock.sync_delay` signature mismatch;
- one direct holographic-encoder constructor mismatch;
- two `PlasmaState` constructor mismatches in risk tests.

R2 changes none of the `dbe/` simulator modules or those legacy tests. The
dedicated SDBES CI workflow therefore enforces the V3/V4 framework and
regression gates without masking or rewriting the separate simulator debt.

## 6. Requirement audit

| R2 requirement | Implementation | Verification |
|---|---|---|
| (A/B/E/G/H/D) response family | `LocalLinearization` | PASS |
| Ordered time-varying propagation | `finite_horizon_response` | PASS |
| Identification/mechanism/assumption separation | schema + dataclasses | PASS |
| Role vs quantity kind | `QuantitySpec` | PASS |
| Unit/dimension/timebase closure | equation/interface validators | PASS |
| `ModelComposition` and `CouplingInterface` | schema + validators | PASS |
| Executable V3 binding | `PredicateVariableBinding` + policy function | PASS |
| Typed resource balances | `ResourceBalance` | PASS |
| Use-specific authorization | `ModelUseAuthorization` | PASS |
| Observability/identifiability/controllability/reachability | model-property schema/dataclass | PRESENT |
| Multi-fidelity promotion | `MultiFidelityModelFamily` | PASS |
| Transfer assessment | `TransferAssessment` | PASS |
| Query-specific influence projection | schema + dataclass | PRESENT |
| Expanded uncertainty/stability semantics | normative schema + dataclasses | PRESENT |
| Separate (K(t)) and (X(t)) | `apply_research_transition` | PASS |
| Research test and kill condition | `ResearchTest` | PASS |
| Decision rules | `DecisionRule` | PASS |
| Milestone binding | `MilestoneBinding` | PASS |
| Formalization profile | schema + dataclass | PRESENT |
| Simulation returns through V2 | `package_simulation_as_evidence` | PASS |

## 7. Observed failure modes and release decision

No R2 acceptance or regression failure was observed. The implementation did
expose the intended failure modes during negative tests:

- mismatched dimensions, temporal support, and timebases are rejected;
- semantic-free and failure-free interfaces are rejected;
- empty validity-domain intersections are rejected;
- unresolved/conflicted V3 predicates are blocked in strict mode;
- low-fidelity results cannot skip promotion criteria;
- partial transfer is rejected for strict use;
- unclosed conservation balances fail;
- research actions cannot mutate physical state;
- milestones remain open until every explicit requirement is satisfied.

Because the unexpected-regression count is zero and all SDBES release gates
pass, V4 R2 is approved for the `SDBES` branch.
