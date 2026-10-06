PAPER: ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets / 10.1016/j.fusengdes.2015.07.008 / Fusion Engineering and Design 100, 378–405 (2015) / 2015-11-01 (day inferred)
BIND: S-Q
GATES: G1=pass G2=pass G3=pass G4=pass G5=fail G6=pass
MATH: Table 1: P_f = 525 MW, P_tot = 708 MW, eta_elec = 0.40, P_e = 283 MW, P_net = 190 MW, Q_e = 3.0, Q_p ≈ 13.6, bootstrap fraction ~63%. Coupled aux: LHCD 25 MW, ICRF 13.6 MW. Table 2: LH wall-plug 69.6 MW → 25.0 MW at the launcher; ICRF wall-plug ~19 MW. Aggressive Pilot: eta ~50%, P_net = 261 MW, Q_e = 3.8.
SCORE: S-Q C1 T2 D0 A0 stays (CUT as output; ledger stress test)
ACTION: HOLD
ROUTE: QUEUE
VERSION: none
DISPUTER: ARC's Q_e = 3 is a design estimate for the power core only; the authors say the full-plant Q_e is lower. Designs are not plants, and SPARC has not yet run.
LEDGER: P_recirc = P_e − P_net = 283 − 190 = 93 MW; f_recirc ≈ 1/3; Q_e = 3.0 (FPC Brayton estimate). Conservative direction only.
WHY QUEUED: A1 miss: S-Q is CUT. A2 miss (G5). A3 miss: HOLD. A4 pass: a published power balance tightens the ledger conservatively. A5 pass: journal. A6 pass. A7 miss: one more HOLD. A8 pass. Oscar-approved bibliography / ledger-input row for the DBE paper (Phase 5 source check, primary PDF read). Bibliography only: no claims.json edit, no versions.json bump in this PR; INCLUDE (PATCH) is left to the weekly freeze review.
AUTO-GATE: miss A1, A2, A3, A7

CORE: MIT's ARC conceptual design is a compact, high-field HTS tokamak with demountable magnets. Its design point is 525 MW of fusion power, 708 MW of total thermal power, a plant thermal efficiency of 0.40, 283 MW of total electric and 190 MW of net electric output, so Q_e = 3.0. The lower-hybrid chain draws 69.6 MW from the wall to launch 25.0 MW.
WHY: Second, independent anchor for the MCF recirculating-power term of the Q ledger: P_recirc = 283 − 190 = 93 MW, f_recirc ≈ 1/3. Even the 'aggressive Pilot' case (Brayton ~50%, 261 MW net, Q_e = 3.8) is about 260 times above the f_recirc = 1e-3 that Q_eng = 1000 needs.
LIMIT: Conceptual design, not a built plant. The authors say Q_e is a Brayton estimate for the fusion power core alone and the whole-plant Q_e is lower. Tokamak, not stellarator. Binds S-Q, which is CUT as an output, so it can never be an ADD; ledger input only. No version bump.
PILLAR: fusion-q1000 (no pillar change)
BRIDGE: no
SOURCE TIER: journal. Not C.
LICENCE: not confirmed (Unpaywall skipped, no contact email)
OA: green — https://arxiv.org/abs/1409.3540
MACHINE-TRANSLATED: no
NOTE: Manual Oscar-approved follow-up (Phase 5 source check), not part of run-2026-10-06-daily.
