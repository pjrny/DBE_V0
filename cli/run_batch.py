"""
DBE batch runner (Phase 7).

This script generates a set of synthetic DBE scenarios by sweeping over
randomly sampled plasma stabilities, coil currents, pellet availability
and memory error counts.  For each scenario it computes a risk score
using the :class:`~dbe.risk.RiskAnalyzer` and writes the results to a
CSV file.  The goal is to produce a dataset of inputs → outputs to
explore controller performance and risk behaviour.

Usage
-----

Run this script from the root of the repository.  By default it
generates 100 runs and writes the results to `outputs/batch_runs.csv`.
You can override the number of runs with the `--runs` command‑line
option and the output path with `--out`.  Example:

    python cli/run_batch.py --runs 200 --out outputs/my_runs.csv

The output CSV has the following columns:

```
run_id,stability,coil_fraction,pellet_available,memory_errors,risk_score,notes
```

Notes are semicolon‑separated descriptive strings from the risk
analyzer.
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys
from typing import List

# Ensure we can import the `dbe` package when executed as a standalone file.
this_dir = os.path.dirname(__file__)
repo_root = os.path.abspath(os.path.join(this_dir, ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
if os.path.dirname(repo_root) not in sys.path:
    sys.path.insert(0, os.path.dirname(repo_root))

from dbe.risk import RiskAnalyzer
from dbe.plasma import PlasmaState


class DummyCoil:
    def __init__(self, I_set: float, I_max: float) -> None:
        self.I_set = I_set
        self.I_max = I_max


class DummyPellet:
    def __init__(self, available: bool) -> None:
        self.available = available

    def can_fire(self, _time: float) -> bool:
        return self.available


class DummyMemory:
    def __init__(self, error_count: int) -> None:
        self.error_count = error_count


class DummyController:
    def __init__(self, coil: DummyCoil, pellet: DummyPellet, memory: DummyMemory) -> None:
        self.rmp_coil = coil
        self.pellet_injector = pellet
        self.memory = memory



def generate_runs(num_runs: int) -> List[dict]:
    """Generate a list of scenario dictionaries for batch runs.

    Each run is represented by a dictionary with keys:
    ``stability``, ``coil_fraction``, ``pellet_available``, ``memory_errors``.
    """
    runs = []
    for run_id in range(num_runs):
        stability = random.uniform(0.0, 1.0)
        coil_fraction = random.choice([0.0, 0.5, 1.0])
        pellet_available = random.choice([True, False])
        memory_errors = random.choice([0, 1, 2, 5])
        runs.append({
            "run_id": run_id,
            "stability": stability,
            "coil_fraction": coil_fraction,
            "pellet_available": pellet_available,
            "memory_errors": memory_errors,
        })
    return runs



def main(args: List[str]) -> None:
    parser = argparse.ArgumentParser(description="Run DBE risk batch simulations.")
    parser.add_argument(
        "--runs", type=int, default=100, help="Number of runs to generate."
    )
    parser.add_argument(
        "--out",
        type=str,
        default=os.path.join("outputs", "batch_runs.csv"),
        help="Output CSV filename.",
    )
    ns = parser.parse_args(args)

    num_runs = ns.runs
    out_file = ns.out
    # Ensure output directory exists
    out_dir = os.path.dirname(out_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    runs = generate_runs(num_runs)
    analyzer = RiskAnalyzer()

    with open(out_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "run_id",
            "stability",
            "coil_fraction",
            "pellet_available",
            "memory_errors",
            "risk_score",
            "notes",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for run in runs:
            coil = DummyCoil(I_set=run["coil_fraction"], I_max=1.0)
            pellet = DummyPellet(available=run["pellet_available"])
            memory = DummyMemory(error_count=run["memory_errors"])
            controller = DummyController(coil, pellet, memory)
            plasma = PlasmaState(stability=run["stability"])
            report = analyzer.assess(plasma, controller)
            writer.writerow({
                "run_id": run["run_id"],
                "stability": f"{run['stability']:.4f}",
                "coil_fraction": run["coil_fraction"],
                "pellet_available": run["pellet_available"],
                "memory_errors": run["memory_errors"],
                "risk_score": f"{report.score:.4f}",
                "notes": "; ".join(report.notes),
            })
    print(f"Wrote {num_runs} runs to {out_file}")



if __name__ == "__main__":
    main(sys.argv[1:])
