from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    languages = state.get("repository_analysis", {}).get("languages", {})
    python_weight = languages.get(".py", 0)
    has_ml_surface = python_weight > 0
    governance_score = 74 if has_ml_surface else 88
    state["ml_review"] = {
        "ml_risk": "Medium" if has_ml_surface else "Low",
        "drift_probability": 0.31 if has_ml_surface else 0.08,
        "governance_score": governance_score,
        "lineage_status": "manual-review-required" if has_ml_surface else "not-applicable",
    }
    if has_ml_surface:
        state.setdefault("recommendations", []).append(
            {"area": "ml_governance", "action": "Add dataset lineage, model cards, and drift monitoring hooks."}
        )
    return state


def ml_governance_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "ML Governance Agent", "Documentation Agent", "ml_governance_ready", _execute)

