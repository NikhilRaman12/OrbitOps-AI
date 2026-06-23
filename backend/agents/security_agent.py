from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import security_scanner_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = security_scanner_tool(path)
    state["security_review"] = review
    for finding in review.get("critical_findings", []):
        state.setdefault("recommendations", []).append(
            {"area": "security", "action": f"Rotate and remove suspected {finding['type']} in {finding['path']}."}
        )
    return state


def security_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Security Agent", "ML Governance Agent", "security_review_ready", _execute)

