"""
dbe.risk
--------
Phase 1 risk scaffolding. Emits structured messages later.
"""

from dataclasses import dataclass

@dataclass
class RiskReport:
    score: float = 0.0
    notes: list[str] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []

def assess_placeholder(_) -> RiskReport:
    return RiskReport(score=0.0, notes=["Phase 1 placeholder"])
