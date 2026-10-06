PAPER: NRL Plasma Formulary (2007 edition) / https://www.govinfo.gov/content/pkg/GOVPUB-D210-PURL-LPS83689/pdf/GOVPUB-D210-PURL-LPS83689.pdf / Naval Research Laboratory, Beam Physics Branch, Plasma Physics Division, Washington, DC (2007 edition) / 2007-01-01 (day inferred)
BIND: S-L1
GATES: G1=pass G2=pass G3=pass G4=pass G5=pass G6=pass
MATH: p. 28: nu_e = 2.91e-6 n_e lnΛ T_e^(-3/2) s^-1; nu_i = 4.80e-8 Z^4 mu^(-1/2) n_i lnΛ T_i^(-3/2) s^-1 (n in cm^-3, T in eV, mu = m_i/m_p). Ion–ion Coulomb logarithm p. 34. Collisions and transport section from p. 31.
SCORE: S-L1 C2 T2 D1 A3 stays
ACTION: HOLD
ROUTE: QUEUE
VERSION: none
DISPUTER: Formulary rates are order-of-magnitude Spitzer-type estimates; a dense or strongly coupled plasma needs a better lnΛ, and polarized-fuel survival (Kulsrud 1982) is a different question from pair coherence.
LEDGER: none. Not a plant term; sets the S-L1 coherence-time comparison.
WHY QUEUED: A1 pass (S-L1 only, HOLD). A2 pass. A3 miss: HOLD. A4 miss: a textbook rate does not move C. A5 miss: government reference, not journal. A6 pass. A7 miss. A8 pass. Oscar-approved bibliography / ledger-input row for the DBE paper (Phase 5 source check, primary PDF read). Bibliography only: no claims.json edit, no versions.json bump in this PR; INCLUDE (PATCH) is left to the weekly freeze review.
AUTO-GATE: miss A3, A4, A5, A7

CORE: The standard plasma-physics formulary. Page 28 gives the electron collision rate nu_e = 2.91e-6 n_e lnΛ T_e^-3/2 s^-1 and the ion collision rate nu_i = 4.80e-8 Z^4 mu^-1/2 n_i lnΛ T_i^-3/2 s^-1 (n in cm^-3, T in eV); the ion–ion Coulomb logarithm is on page 34.
WHY: Sets the collision time that the Layer 1 coherence target (decoherence time above 1e-9 s) has to beat. At n_i = 1e20 cm^-3 and T_i = 1 keV the ion collision time is of order a nanosecond or less, so 'maintained phase coherence' between colliding pairs has no margin.
LIMIT: Textbook formulas with order-unity coefficients; the result depends on the Coulomb logarithm chosen. The edition consulted is 2007 (an earlier candidate said 2013). Government reference, not a journal (A5 fails). Moves no C. No version bump.
PILLAR: fusion-q1000 (no pillar change)
BRIDGE: no
SOURCE TIER: government/lab report. Not C.
LICENCE: not confirmed (Unpaywall skipped, no contact email)
OA: bronze — https://www.govinfo.gov/content/pkg/GOVPUB-D210-PURL-LPS83689/pdf/GOVPUB-D210-PURL-LPS83689.pdf
MACHINE-TRANSLATED: no
NOTE: Manual Oscar-approved follow-up (Phase 5 source check), not part of run-2026-10-06-daily.
