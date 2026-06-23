from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import code_quality_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = code_quality_tool(path)
    state["code_review"] = review
    for item in review.get("recommendations", []):
        state.setdefault("recommendations", []).append({"area": "code_quality", "action": item})
    return state


def code_quality_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Code Quality Agent", "Security Agent", "code_quality_ready", _execute)

