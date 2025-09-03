# cli/fast_endpoint.py
import os
from typing import Optional, List

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your existing modules (already in repo)
from dbe.controller import DBEController
from dbe.plasma import PlasmaState
from dbe.risk import RiskAnalyzer

app = FastAPI(title="DBE Simulation API", version="0.2.0")

# ----- CORS (reads comma-separated origins from env) -----
allow_origins = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "").split(",") if o.strip()]
if allow_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=False,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

# ----- Simple API key auth -----
API_KEY = os.getenv("DBE_API_KEY", "")

def require_api_key(x_api_key: str) -> None:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# ----- Models -----
class SimRequest(BaseModel):
    qubits_alloc: int
    memory_alloc: int
    engage_time_crystal: bool = False
    engage_compression: bool = False
    gamma_physical: float = 1.0

class SimResponse(BaseModel):
    success: bool
    mitigation_probability: float
    new_stability: float

class SimBatchRequest(BaseModel):
    runs: List[SimRequest]

# ----- Meta endpoints -----
@app.get("/")
def root():
    return {"ok": True, "message": "DBE endpoint ready"}

@app.get("/version")
def version():
    return {"version": app.version}

@app.get("/health")
def health():
    # light probe using existing modules
    controller = DBEController()
    ra = RiskAnalyzer()
    _ = ra.assess(PlasmaState(stability=0.8), controller)
    return {"status": "ok"}

# ----- Core endpoints -----
@app.post("/simulate", response_model=SimResponse)
def simulate(req: SimRequest, x_api_key: str = Header(default="")):
    require_api_key(x_api_key)

    # minimal guardrails
    if not (0 <= req.qubits_alloc <= 256 and 0 <= req.memory_alloc <= 1024):
        raise HTTPException(status_code=400, detail="unreasonable allocation")
    if not (0.0 <= req.gamma_physical <= 10.0):
        raise HTTPException(status_code=400, detail="gamma out of range")

    # Tie into your existing modules (simple heuristic placeholder)
    controller = DBEController()
    risk_analyzer = RiskAnalyzer()

    # crude mitigation probability combining inputs; replace with your more
    # detailed simulate_event if desired
    base = 0.40
    bonus = 0.004 * req.qubits_alloc + 0.003 * req.memory_alloc
    if req.engage_time_crystal: bonus += 0.08
    if req.engage_compression:  bonus += 0.04
    p = max(0.0, min(0.99, base + bonus))

    new_stability = max(0.0, min(1.0, 0.75 + 0.2 * (p - 0.5)))
    return SimResponse(success=(p > 0.5), mitigation_probability=p, new_stability=new_stability)

@app.post("/simulate_batch")
def simulate_batch(req: SimBatchRequest, x_api_key: str = Header(default="")):
    require_api_key(x_api_key)
    results: List[SimResponse] = []
    for r in req.runs:
        results.append(simulate(r, x_api_key=x_api_key))  # reuse single-run logic
    return {"count": len(results), "results": [r.dict() for r in results]}
