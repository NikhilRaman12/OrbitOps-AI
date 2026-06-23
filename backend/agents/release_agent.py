from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import release_assessment_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    state["release_review"] = release_assessment_tool(state)
    return state


def release_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Release Readiness Agent", "Engineering Risk Agent", "release_review_ready", _execute)

