from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import ml_governance_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = ml_governance_tool(path)
    state["ml_review"] = review
    
    for rec in review.get("recommendations", []):
        state.setdefault("recommendations", []).append({
            "area": "ml_governance",
            "action": rec
        })
        
    return state

def ml_governance_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "ML Governance Agent",
        "Release Decision Agent",
        "ml_governance_ready",
        _execute,
    )
