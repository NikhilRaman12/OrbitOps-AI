from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import dependency_scanner_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = dependency_scanner_tool(path)
    state["dependency_review"] = review
    
    for risk in review.get("risky_dependencies", []):
        state.setdefault("recommendations", []).append({
            "area": "dependency",
            "action": f"Upgrade {risk['package']} in {risk['file']}: {risk['description']}."
        })
        
    if not review.get("manifests"):
        state.setdefault("recommendations", []).append({
            "area": "dependency",
            "action": "No package manifest detected. Add a requirements.txt or package.json to track project dependencies."
        })
        
    return state

def dependency_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "Dependency Agent",
        "Documentation Agent",
        "dependency_review_ready",
        _execute,
    )
