from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.mcp_tools import documentation_analyzer_tool
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    review = documentation_analyzer_tool(path)
    state["documentation_review"] = review
    for section in review.get("missing_sections", []):
        state.setdefault("recommendations", []).append(
            {"area": "documentation", "action": f"Add README section for {section}."}
        )
    return state


def documentation_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Documentation Agent", "CI/CD Agent", "documentation_review_ready", _execute)

