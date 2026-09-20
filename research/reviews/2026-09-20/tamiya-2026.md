# rev-2026-09-20-tamiya

PAPER: tamiya-2026 / 2026-09-20

BIND: E-QEC

GATES: {'G1': 'pass', 'G2': 'pass', 'G3': 'pass', 'G4': 'pass', 'G5': 'pass', 'G6': 'pass', 'note': 'Closed threshold proof vs stochastic baseline; platform-honest (codes, not a tokamak).'}

MATH: Coherent Z-rotation noise on qLDPC / surface code; ML Pauli recovery. Breaks if noise is generic non-Pauli coherent.

SCORE: harvest I/C/P {'importance': 86, 'confidence': 84, 'popularity': 72} (not C/T/D/A)

ACTION: INCLUDE

ROUTE: AUTO-MERGED

VERSION: DBE-0.1.1

DISPUTER: Proof is Z-type coherent rotations, not a non-Abelian decoder.

LEDGER: n/a

Core: Real devices make coherent over-rotations, not just random bit flips. This paper proves a positive threshold still exists for that noise on surface-code-like codes.

Why: DBE braids will be miscalibrated. A coherent-error theorem is more honest than a stochastic slogan.

Limitation: Does not cover generic non-Pauli coherent noise or non-Abelian anyon decoding.
