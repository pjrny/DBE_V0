# Dimensional Braid Engine — approved freeze DBE-0.2.0
Date: 2026-09-21  
Kind: MAJOR (retired pillars)  
Previous: DBE-0.1.3

## What this paper is
The approved DBE is a modular stack, not a five-headed engine.

- **Bus A — plant attach.** Learned plasma control on a machine that already exists (DIII-D now; SPARC/ITER-class later). Metric: beat a lab baseline on one disruption-relevant number. KEEP · E-RL · C4 T3 D3 A3.
- **Bus B — compute.** S₃ braid + fusion as the topological primitive, wrapped in a surface-code / qLDPC error layer. KEEP · E-S3 C3 · E-QEC C4.
- **Bus C — microphysics.** A campaign, not a coupled engine. It does not write a plant Q in this freeze.

Cyclic fusion is in this paper as the *reason S₃ + fusion is universal*. It is not a fourth bus.

## Load-bearing (in the paper)
| ID | Claim | C T D A | Status |
|---|---|---|---|
| E-S3 | S₃ braid + fusion is the topological primitive | C3 T3 D3 A3 | KEEP |
| E-QEC | Surface-code / qLDPC is the error layer | C4 T3 D3 A3 | KEEP |
| E-RL | RL/AI control attaches to an existing plant bus | C4 T3 D3 A3 | KEEP |

Evidence that rides: Kitaev 1997, Nayak 2008, Lo et al. Nature 2026 (Quantinuum H2 S₃), Willow / qLDPC threshold papers, TCV/DIII-D RL control.

## Watch (diagram only, not load-bearing)
| ID | Claim | Status | Rule |
|---|---|---|---|
| E-MZM | Majorana zero modes as load-bearing qubits | WATCH C1 | M5: independent X and Z plus gap scaling, or drop from the diagram. |

## Cut from this paper
These stay in the library. They do not ride the engine.

- **E-TC** Floquet time crystal as system clock — CUT as metronome. Use a classical clock + QEC cycle.
- **E-FR** Fracton code as hardware memory — CUT from the hardware stack.
- **E-HOL** Holographic encoding as a reactor/processor part — CUT. Reading list only.
- **E-5** Five subsystems coupled as one device — CUT. Coupling starts at C1.
- Consciousness benchmark — already cut in 0.1.0.
- **Q = 1000 as an output** — not a DBE result. Ledger stress test only.

## Suggested pillars decided this freeze
Protocol: at most one NEW PILLAR per week. None added as a new bus.

- **cyclic-fusion** — promoted suggested → established, *under E-S3*. High confidence. Not a new ID.
- **cyclic-fusion-family** (Haagerup–Izumi at every odd order) — expired as pillar. Bibliography under E-S3. No interface contract.
- **nonabelian-qldpc** — expired as pillar. Abelian qLDPC already rides E-QEC.
- **topo-dynamics** — expired as pillar. Jennings is a Bus B constraint, not a subsystem.
- **floquet-majorana-codes**, **spacetime-fractons**, **fracton-holography** — rejected. They couple WATCH/CUT boxes. Coupling starts at C1.

## What the paper may not say
- Harvest gauges (importance / confidence / popularity 0–100) are not C.
- Simulations cannot raise C above 2. Wrong-platform hardware cannot raise C above 3.
- A CUT reversal needs two independent C≥4 sources.

## Milestones unchanged
M0 done (this rubric). M1–M8 open. M5 is the Majorana distinguisher. M8 is the actual deliverable: a control container a SPARC-class team can run without DBE metaphysics.
