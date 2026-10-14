# SDBES V8 — Knowledge Universe, completed interface release

**Implementation status:** V8 framework and frontend interface complete for available **source-backed records** and clearly separated **educational demonstrations**. This release is not a validated physical simulator, not an automatically assessed 90-concept corpus, not a probability-of-truth engine, and not the V9 Research Campaign Engine.

## Scope

The primary SDBES mission is the cross-domain visualization of Dimensions Beyond Energy Scarcity—not optimization of one Observatory research stream. The six source domains remain A–F and 90 unchanged concept IDs. V7's separate 13-claim Observatory is contextual evidence intake, not a seventh domain or the source of general taxonomy.

## Finished V8 functionality

1. **Interactive 2D and optional 3D taxonomy.** Full 90-concept domain map and object-kind-based spatial projection; domain, concept and reviewed-case levels are distinguished by categorical position. Zooming/focusing, keyboard alternatives, persistent record inspector and filters stay available. Neither distance nor elevation means probability, physical extra dimensions or scientific impact.
2. **F/E/A×V/I/G evidence profile.** A typed registry accepts only claim-scoped, provenance- and verification-activity-backed assessment cells. The existing 10 reviewed V1/V2 cases contribute method labels and detailed source/application trace records, but **not** automatically validated V/I/G values. Unregistered cells display UNKNOWN. Independent replication requires a specifically registered replication activity.
3. **Knowledge-state and V3 dependency mathematics.** A separately labeled mathematical sandbox exercises the four-valued knowledge states `NEITHER/TRUE_ONLY/FALSE_ONLY/BOTH` and the three-valued scenario states `UNKNOWN/TRUE/FALSE`. ALL, ANY, k-of-n, minimal path sets and minimal cut sets operate on a model-relative, monotone four-predicate **hypothetical** network. The registered structural graph panel is empty until valid source-scoped predicate/gate data is imported.
4. **V4 mathematical dynamics visualization.** A clearly synthetic, dimensionless linear recurrence `x(k+1)=ax(k)+u−d` provides intervention, zero-control comparator, impulse response, local Jacobian eigenvalue and fixed-point interpretation. It is for mathematical explanation only: no calibrated source, units, physical regime or real prediction. The real V4 scenario execution remains disabled without a registered use-bounded domain model.
5. **Time and lineage.** The historical snapshot timeline and provenance inspector show actual import/reference artifacts and known source incidents. They do not invent claim-level changes absent versioned claim assessment history.
6. **Exploratory cross-field lens.** Shared catalog tags are classified as unreviewed topic overlap, explicitly not causal or structural linkage. Side-by-side concept comparisons keep evidence, phase-1 labels, roles and research gaps separate.

## Complete scientific boundaries

`docs/SDBES/data/V8_VIEW_RECORDS.json` establishes a machine-readable registry for future reviewed profile records, verification activities, structural predicate graphs and model-card entries. The baseline intentionally has **zero** of these items because complete receipt-backed records are not available in the current frozen intake. Validator tests protect source/claim binding, receipt integrity, unknown-vs-absent distinctions, replication claims, gate referential integrity, and model provenance.

Mathematical simulations are not probabilistic inference; the V8 system **allows appropriately specified probabilities but does not produce universal confidence percentages**. Real calibrated simulations, broad fully reviewed source coverage, stochastic forecasts, publication decisions, and autonomous campaigns require additional scientific inputs or V9/V10 workflows. These are scientific-data readiness requirements, not unimplemented V8 user-interface controls.

## Verification

```sh
cd navigator
npm ci
npm run test
npm run build
```

Plus the SDBES Python regressions from previous versions. New targeted tests cover registry semantics, the gate logic, minimal paths/cuts, the linear synthetic trajectory and categorical projection. The existing V5–V7 integrity tests and source-snapshot checks must remain green.

## Publishing

The SDBES branch contains the navigator source and V8 release specification. GitHub Pages is independently published from `feature/research-grade-physics`; static deployment of the compiled Vite bundle at `/DBE_V0/navigator/` requires building with the repository base path. A source HTML entry by itself is not a usable hosted app. Any deployed build must preserve the Observatory at `/DBE_V0/research/lab.html`.

**Design invariant:** Preserve information first. Aggregate second. Simulate last.
