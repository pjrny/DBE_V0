"""
dbe.controller
--------------
Phase 1 scaffold for DBEController; actual logic lands in Phase 5.
"""

from dataclasses import dataclass
from typing import Any

@dataclass
class DBEController:
    def decide(self, plasma_state: Any) -> dict:
        # Phase 1: no-op policy
        return {"action": "noop"}
