from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import repository_analysis_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    analysis = repository_analysis_tool(path)
    health = 92 if analysis["source_files"] > 5 else 72
    if analysis["risk_files"]:
        health -= 10
    state["repository_analysis"] = {
        "repository_health": max(40, health),
        "active_branches": analysis["active_branches"],
        "contributors": analysis["contributors"],
        "risk_files": analysis["risk_files"],
        "languages": analysis["languages"],
        "source_files": analysis["source_files"],
    }
    return state


def repository_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "Repository Intelligence Agent",
        "Code Quality Agent",
        "repository_context_ready",
        _execute,
    )

