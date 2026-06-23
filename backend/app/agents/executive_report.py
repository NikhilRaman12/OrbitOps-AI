from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import executive_report_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    report = executive_report_tool(state)
    state["executive_summary"] = report
    return state

def executive_report_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "Executive Report Agent",
        "Dashboard",
        "executive_report_ready",
        _execute,
    )
