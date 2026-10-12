PAPER: Resgru: Syndrome decoder for heavy-hexagon quantum error correction code / kumar-resgru-2026 / Physica Scripta / 2026-07-15
BIND: E-QEC
GATES: G1=pass G2=pass G3=pass G4=fail G5=pass G6=pass
MATH: INSPIRE recid 3185476. DOI 10.1088/1402-4896/ae87e2. Phys. Scr. 101 (2026) 285102. Authors Kumar, Haghparast, Kettunen. Stated simulation: p = 0.1 percent, d in {3, 5, 7}, 28 percent reduction at d=5, 14 percent at d=7, checked to 300 rounds. Licence not in the INSPIRE record.
SCORE: E-QEC C4 T3 D3 A3 stays
ACTION: HOLD
ROUTE: QUEUE
VERSION: none
DISPUTER: Beating MWPM by 28 percent at distance 5 in a depolarizing simulation is not the device result that holds E-QEC at C4. A Physica Scripta venue passes the preprint test and still does not raise C, because G4 and A4 fail. Do not raise C.
LEDGER: none.
WHY QUEUED: A1 pass (E-QEC only). A2 miss (G4). A3 miss: HOLD, not INCLUDE. A4 miss: C stays C4; a simulated decoder gain is not a published device bound. A5 pass: Physica Scripta 101, 285102 (2026). A6 pass. A7 pass. A8 pass. Journal tier: harvest confidence 71 is round(71 x 1.00), still under 80.
AUTO-GATE: miss A2, A3, A4

CORE: Resgru is a recurrent neural decoder that maps time-ordered heavy-hexagon detection events to a binary logical class for each shot. On a circuit-level depolarizing model at physical error rate 0.1 percent, for distances 3, 5, and 7, the authors report higher logical fidelity than minimum-weight perfect matching on the same detector error model, including a 28 percent lower per-round logical error at distance 5 and 14 percent at distance 7. The network was trained on short sequences and checked out to 300 correction rounds.
WHY: A heavy-hexagon syndrome decoder is queued under E-QEC. The 28 percent and 14 percent reductions are comparisons with matching inside a noise model, not a new device memory. The journal venue does not by itself raise C. C4 stays.
LIMIT: INSPIRE earliest date 2026-07-15, outside the seven-day window; this weekly pull found it because the INSPIRE date filter did not stick. Phys. Scr. 101, 285102 (2026). Licence and OA status were not resolved: Unpaywall was skipped, no contact email. No PDF cached.
PILLAR: none
BRIDGE: no
SOURCE TIER: journal (1.0). Harvest confidence 71 is round(71 x 1.00). Not C.
LICENCE: unresolved (Unpaywall skipped, DBE_CONTACT_EMAIL unset)
OA: unknown
MACHINE-TRANSLATED: no
