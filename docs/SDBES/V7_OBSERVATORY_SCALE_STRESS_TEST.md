# SDBES V7 — Observatory scale stress test

Status: implemented bulk integrity and consistency run. This is not a 405-paper scientific replication or an automatic claim-promotion pass.

## Purpose

V7 tests whether SDBES can ingest a substantially larger, focused research program without confusing inventory, review, association, and scientific confirmation.

The pinned source is Observatory commit `9665178ca906a20af25ad23f7cea6ff838d43d57` from 2026-10-08. Only its four structured research files were captured. Observatory application code, simulator code, and review-markdown corpus were not merged into `SDBES`.

## Result

| Measure | V7 result |
|---|---:|
| Cataloged papers | 405 |
| Structured review cards | 291 |
| Cataloged papers with a review card | 288 |
| Cataloged papers without a review card | 117 |
| Observatory program claims | 13 |
| Review-declared paper-to-claim associations | 239 |
| Scientific promotions applied | 0 |

The run passed for browsing, inspection, and use of the pre-existing review bindings, with source defects quarantined. It did not authorize automatic claim strengthening, causal-edge creation, ranking, or pruning.

## Findings retained by the gate

1. Two review cards refer to paper IDs absent from the captured catalog: `2609.20985` and `2609.20725`.
2. Five review cards use `hold` as a gate state even though the established gate vocabulary is pass/fail/partial/unknown. The records are retained and flagged as schema drift.
3. 322 of 405 catalog records have no `sourceTier`. This blocks reliable corpus-wide source-quality comparison until those values are populated or explicitly marked unknown.

V7 does not silently repair any of these records. Known defects remain visible in the generated stress report and release gate.

## Claim association boundary

The Observatory's `bind` fields create candidate associations to its 13 program claims. These are useful for organizing the focused braid, quantum-computing, plasma-control, ignition, barrier-control, and fusion research program.

They mean:

> this review was evaluated in relation to this program claim.

They do not mean:

> this paper independently confirms or strengthens the claim.

`INCLUDE`, `HOLD`, `REJECT`, and `NEW PILLAR` remain Observatory workflow decisions. SDBES records them without converting them into universal scientific verdicts. Any real status change still requires a scoped V1/V2 claim assessment and, where relevant, V3/V4 dependency or model evaluation.

## V4 scenario eligibility

V7 found the `sdbes.v4` reference implementation, but no registered executable scientific model package. The reference code tests contracts, causal-composition rules, and regression behavior. It does not contain a calibrated domain simulator with all of the following:

- pinned code and model version;
- defined inputs, units, operating regime, and horizon;
- calibration or validation record;
- complete dependency and interface contract;
- model-use authorization receipt.

For that reason, the workbench describes V4 scenarios as **not yet registered**, rather than scientifically inapplicable. Adding a valid model card and receipt will make a scenario eligible; no framework redesign is required.

The authorization receipt is an internal provenance record, not outside permission or a declaration that the model is true. It records who or what approved the model for a stated use, the exact version reviewed, the allowed scope, and the date.

## OpenAI Math probe

OpenAI Math is recorded as a separate experimental source family, not merged into the Observatory evidence scores. Its official repository reported 722 manuscripts in 372 families on 2026-10-09, with a mixture of Lean-formalized and unformalized results.

For SDBES, a successful Lean check may establish that a formal statement follows from its encoded assumptions in the pinned environment. It does not by itself establish that:

- the statement models a physical DBE bottleneck;
- the assumptions hold in the target regime;
- the formalization exactly matches every manuscript claim;
- the result is independently replicated or experimentally confirmed.

The useful V7 role is to test formal-artifact provenance, theorem dependencies, corrections and withdrawals, and whether a result changes a specific bottleneck. Relevance must be established claim by claim.

Official source: <https://github.com/openai/math> (accessed 2026-10-09).

## Reproduce

```bash
python scripts/build_v7_assets.py
python tests/sdbes_v7_stress_checks.py
```

The capture command is intentionally separate and should be used only when adopting a new pinned Observatory snapshot:

```bash
python scripts/build_v7_assets.py --capture-ref <pinned-observatory-ref>
```
