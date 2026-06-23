from __future__ import annotations

from backend.agents.base import run_agent
from backend.services.state import OrbitState


def _execute(state: OrbitState) -> OrbitState:
    scores = {
        "repository": state.get("repository_analysis", {}).get("repository_health", 0),
        "code": state.get("code_review", {}).get("quality_score", 0),
        "security": state.get("security_review", {}).get("security_score", 0),
        "documentation": state.get("documentation_review", {}).get("documentation_score", 0),
        "pipeline": state.get("cicd_review", {}).get("pipeline_health", 0),
        "ml_governance": state.get("ml_review", {}).get("governance_score", 0),
    }
    risk_score = round(100 - (sum(scores.values()) / max(1, len(scores))))
    top_risks = [
        f"{area} score is {score}"
        for area, score in sorted(scores.items(), key=lambda item: item[1])
        if score < 75
    ][:5]
    if risk_score >= 45:
        overall = "High"
    elif risk_score >= 25:
        overall = "Medium"
    else:
        overall = "Low"
    state["risk_review"] = {
        "overall_risk": overall,
        "risk_score": risk_score,
        "top_risks": top_risks,
        "score_breakdown": scores,
    }
    return state


def risk_agent(state: OrbitState) -> OrbitState:
    return run_agent(state, "Engineering Risk Agent", "Executive Summary Agent", "risk_review_ready", _execute)

