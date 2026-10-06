PAPER: Diagnostic Methodologies of Laser-Initiated 11B(p,α)2α Fusion Reactions / 10.3389/fphy.2020.561492 / Frontiers in Physics 8, 561492 (2020) / 2020-11-12
BIND: S-L3
GATES: G1=pass G2=pass G3=pass G4=pass G5=pass G6=pass
MATH: p + 11B → 3α + 8.7 MeV. Channel 1: p + 11B → alpha_0 + 8Be (Q = 8.59 MeV), 8Be → 2α (Q = 91.8 keV). Channel 2: p + 11B → alpha_1 + 8Be* (Q = 5.65 MeV, width 1.5 MeV), 8Be* → 2alpha_12 (Q = 3.028 MeV). alpha_0 ≈ 5.7 MeV, alpha_1 ≈ 3.76 MeV; alpha_12 from 0 to > 5 MeV.
SCORE: S-L3 C4 T2 D2 A3 stays
ACTION: HOLD
ROUTE: QUEUE
VERSION: none
DISPUTER: Channel energies are kinematic estimates; measured laser-plasma alpha spectra are broadened and diagnostic-limited (CR-39, Thomson parabola), so the 5.7 / 3.76 MeV lines are indicative, not measured peaks.
LEDGER: none. Fixes the alpha-energy input (8.7 MeV over 3 alphas; alpha_0 ≈ 5.7 MeV, alpha_1 ≈ 3.76 MeV); no plant term moved.
WHY QUEUED: A1 pass (S-L3 only, KEEP). A2 pass. A3 miss: HOLD (bibliography only by instruction; no PATCH in this PR). A4 pass: C unchanged and a published number corrects the manuscript. A5 pass: journal. A6 pass. A7 miss. A8 pass. Oscar-approved bibliography / ledger-input row for the DBE paper (Phase 5 source check, primary PDF read). Bibliography only: no claims.json edit, no versions.json bump in this PR; INCLUDE (PATCH) is left to the weekly freeze review.
AUTO-GATE: miss A3, A7

CORE: Review of diagnostics for laser-initiated p-11B fusion. p + 11B → 3α + 8.7 MeV proceeds mainly via 8Be: through the 8Be ground state (alpha_0 + 8Be, channel Q = 8.59 MeV; 8Be → 2α with Q = 91.8 keV) or through 8Be* (alpha_1 channel Q = 5.65 MeV, width 1.5 MeV; 8Be* → 2α with Q = 3.028 MeV). In laser plasmas alpha_0 and alpha_1 are estimated at about 5.7 and 3.76 MeV; the secondary alphas spread from 0 to above 5 MeV.
WHY: Corrects the Layer 3 alpha-energy premise: 8.7 MeV is shared by three alphas, so no single alpha carries '2.9 to 8.7 MeV'. The alpha spectrum is the input for any phase-space repopulation or direct-conversion term.
LIMIT: Diagnostics review with channel energies from kinematics, not a new nuclear-data measurement. Laser-driven, not a thermal burn. 91.8 keV is the 8Be ground-state decay Q, not the primary fusion Q. Moves no C. No version bump.
PILLAR: fusion-q1000 (no pillar change)
BRIDGE: no
SOURCE TIER: journal. Not C.
LICENCE: https://creativecommons.org/licenses/by/4.0/
OA: gold — https://doi.org/10.3389/fphy.2020.561492
MACHINE-TRANSLATED: no
NOTE: Manual Oscar-approved follow-up (Phase 5 source check), not part of run-2026-10-06-daily.
