# SDBES V5/V6 R2 — Evidence Workbench and 90-concept pilot

Status: implemented read-only pilot. This release does not authorize automated scientific ranking, pruning, or model execution.

## Purpose

V5 gives a human a truthful way to navigate V1–V4 records. V6 stages the 90 Phase-1 concept candidates without representing them as 90 assessed claims.

The implementation optimizes the speed and clarity with which a reader can determine what is supported, challenged, unknown, or still unverified. It does not optimize the number of promising-looking pathways.

## Release boundaries

- The 90 concept records are `STAGING_ONLY`.
- Phase-1 D/P/S/X values are legacy discovery tags, not confidence values or probabilities.
- The 10 existing paper cases are displayed separately as reviewed claim cases.
- The 13 Observatory program claims are preserved as a separate pinned snapshot. A program `CUT` means cut for the specified program use; it is not universal falsification.
- Only explicit reviewed claim-to-concept relations are drawn. Topic similarity is never rendered as dependency or causation.
- The 19 background-only/adjacent-source identities remain unreconciled because `SEARCH_AND_GAPS.md` contains an error payload.
- Source hashes verify preservation, not source validity or scientific correctness.
- No V4 result is displayed unless a model has a model-use authorization receipt. This release contains no authorized runtime model.

## First interface

One connected workspace contains:

1. a searchable, faceted 90-record atlas;
2. a persistent evidence inspector;
3. a small typed neighborhood graph containing reviewed relations only;
4. a research queue of concrete proposed investigations;
5. a navigation-state export.

The inspector always separates:

- exact assertion;
- bounded scope;
- support;
- challenge;
- unresolved questions;
- what would change the assessment;
- source locator;
- model-authorization state.

Review workflow, work disposition, record role, scientific assessment references, and context compatibility are separate fields. They are not compressed into one visual status.

## Selection and anti-p-hacking controls

Research activities use one of these modes:

```text
EXPLORATORY
CONFIRMATORY
REPLICATION
ROBUSTNESS
SOFTWARE_QA
```

The current Phase-1 queue is exploratory. It is not ranked by a universal score. Missing cost, value, uncertainty, or comparability remains missing and may yield `INSUFFICIENT_COMPARABLE_INFORMATION`.

Before a later activity can be called confirmatory, its claim version, primary outcome, comparator, scope, exclusions, analysis procedure, stopping rule, decision rule, and prior data exposure must be frozen before relevant outcomes are inspected. Attempts must retain successful, null, adverse, invalid, abandoned, and failed-to-run outcomes.

User preference may reorder work, but must not alter evidence status. Repeated AI agreement is not independent evidence.

## Simplification rule

View simplification, compute simplification, and research-work simplification are different operations. A no-impact result is valid only for its tested snapshot, scenarios, outputs, interactions, and tolerances. Dormancy requires a reason, owner, snapshot, and reactivation condition. Adverse evidence is never deleted merely because a binary decision is unchanged.

## Data and validation

- `docs/SDBES/data/V6_CONCEPT_INVENTORY.json` — canonical staged inventory.
- `docs/SDBES/data/V5_RUNTIME_VIEW.json` — reviewed cases, reviewed relationships, queue, and authorization state.
- `sdbes/v5_v6.py` — semantic validation.
- `scripts/build_v5_v6_assets.py` — deterministic source-to-staging migration.
- `navigator/` — React/Vite read-only workbench.

The validator checks unique IDs, concept/domain consistency, resolved references, receipt-backed verification, supported workflow/context values, derived counters, crosswalks, T0–T3 Observatory values, reviewed relationship endpoints, and model authorization receipts.

## Run

```bash
python scripts/build_v5_v6_assets.py
python tests/sdbes_v5_v6_integrity_checks.py
cd navigator
npm ci
npm run test
npm run build
```

## Deferred work

- recover or reconstruct the corrupted gap mapping with documented provenance;
- add exact source passages, tables, figures, equations, or code locations;
- add complete research-plan and attempt-ledger authoring;
- enable scientific prioritization only after selection safeguards are tested;
- expose V4 scenarios only after explicit authorization records exist.
