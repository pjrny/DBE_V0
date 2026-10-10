PAPER: Global classical solutions of the three-dimensional relativistic Vlasov-Maxwell system / openai-math-362 / OpenAI Math preprint / 2026-09-23
BIND: S-L3
GATES: G1=pass G2=pass G3=pass G4=fail G5=pass G6=pass
MATH: Commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (2026-10-08). Licence Apache-2.0 from the LICENSE blob at that commit. Theorem name global_classical_solution for Admissible data. PDF sha recorded by the contents API: 0605323dab9e34937ba0a42ffa675bb965903491, 601957 bytes. Not hashed again here and not stored. No DOI.
SCORE: S-L3 C4 T2 D2 A3 stays
ACTION: HOLD
ROUTE: QUEUE
VERSION: none
DISPUTER: An unchecked machine-written existence theorem is not a Layer-3 solver. Lean was not executed. The PDF was not stored and not read. S-L3 stays C4. This cannot raise C.
LEDGER: none.
WHY QUEUED: A1 pass (S-L3 only). A2 miss (G4). A3 miss. A4 miss: C unchanged and no journal bound is tightened. A5 miss: not a journal and not replicated hardware. A6 pass. A7 pass: claim HOLD count unchanged. A8 pass: no ledger term moved. Machine-generated; verify before any later STRENGTHEN.
AUTO-GATE: miss A2, A3, A4, A5

CORE: OpenAI math family 362, manuscript dated 23 September 2026, is a public GitHub preprint titled as global classical solutions of the three-dimensional relativistic Vlasov–Maxwell system. At commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb the tree contains lean/OAI/Analysis/VlasovMaxwell/. Model.lean defines the one-species relativistic system on Euclidean 3-space. Main.lean states a theorem, global_classical_solution, that admissible smooth data have a classical solution which is smooth on every finite time horizon and unique at nonnegative times, proved by calling global_classical_of_uniform_physical_increment. The repository text says the manuscripts were produced by an internal model and that not every result is formalized. This run did not compile Lean and did not read the PDF.
WHY: S-L3 keeps Vlasov methods. This is an existence claim for the relativistic Vlasov–Maxwell equation, so it is queued as background. It is not a fusion reactivity ratio, not M4 (FV versus CN), and not a reason to move C4.
LIMIT: Machine-generated. Not peer-reviewed. PDF stored nowhere (link only). Lean build not run. One species, not a tokamak edge solver. oaStatus left TBD.
PILLAR: none
BRIDGE: no
SOURCE TIER: repo/model (0.4). Harvest confidence 30 is round(40 x 0.76). Not C.
LICENCE: Apache-2.0
OA: TBD by Oscar; public GitHub file under Apache-2.0; not an Unpaywall label
MACHINE-TRANSLATED: no
