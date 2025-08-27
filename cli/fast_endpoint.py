"""
FastAPI endpoint for DBE simulation (Phase 11).

This module exposes a minimal API to call the simulate_event function from the DBE simulation.
Run with: uvicorn cli.fast_endpoint:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from dbe_simulation import simulate_event, DBEState, PlasmaState

# Initialize global state; these objects persist across requests

dbe_state = DBEState()
plasma_state = PlasmaState()
ALPHA = 0.3
BETA = 0.2

app = FastAPI(title="DBE Simulation API")

class SimulationRequest(BaseModel):
    qubits_alloc: int
    memory_alloc: int
    engage_time_crystal: bool = False
    engage_compression: bool = False
    execute_mitigation: bool = True
    gamma_physical: float = 1.0
    alpha: Optional[float] = None
    beta: Optional[float] = None

class SimulationResponse(BaseModel):
    success: bool
    mitigation_probability: float
    new_stability: float

@app.post("/simulate", response_model=SimulationResponse)
def simulate(req: SimulationRequest) -> SimulationResponse:
    """Handle a simulation request and return the result."""
    alpha = req.alpha if req.alpha is not None else ALPHA
    beta = req.beta if req.beta is not None else BETA
    success, prob, new_stability, _, _ = simulate_event(
        dbe_state=dbe_state,
        plasma_state=plasma_state,
        gamma_physical=req.gamma_physical,
        alpha=alpha,
        beta=beta,
        qubits_alloc=req.qubits_alloc,
        memory_alloc=req.memory_alloc,
        engage_time_crystal=req.engage_time_crystal,
        engage_compression=req.engage_compression,
        execute_mitigation=req.execute_mitigation,
    )
    return SimulationResponse(
        success=success,
        mitigation_probability=prob,
        new_stability=new_stability,
    )
