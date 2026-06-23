from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import pipeline_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = pipeline_tool(path)
    state["cicd_review"] = review
    for item in review.get("recommendations", []):
        state.setdefault("recommendations", []).append({"area": "cicd", "action": item})
    return state


def cicd_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "CI/CD Agent", "Release Readiness Agent", "cicd_review_ready", _execute)

