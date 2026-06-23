from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import executive_report_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    state["executive_summary"] = executive_report_tool(state)
    return state


def executive_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Executive Summary Agent", "Dashboard", "executive_summary_ready", _execute)

