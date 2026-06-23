from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import pipeline_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = pipeline_tool(path)
    state["cicd_review"] = review
    
    for rec in review.get("recommendations", []):
        state.setdefault("recommendations", []).append({
            "area": "cicd",
            "action": rec
        })
        
    return state

def cicd_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "CI/CD Agent",
        "ML Governance Agent",
        "cicd_review_ready",
        _execute,
    )
