from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import release_assessment_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    # Compile release assessment
    release = release_assessment_tool(state)
    state["release_review"] = release
    
    # Calculate risk breakdown
    scores = {
        "repository": state.get("repository_analysis", {}).get("repository_health", 100),
        "code": state.get("code_review", {}).get("quality_score", 100),
        "security": state.get("security_review", {}).get("security_score", 100),
        "dependency": state.get("dependency_review", {}).get("dependency_score", 100),
        "documentation": state.get("documentation_review", {}).get("documentation_score", 100),
        "pipeline": state.get("cicd_review", {}).get("pipeline_health", 100),
        "ml_governance": state.get("ml_review", {}).get("governance_score", 100),
    }
    
    # Risk score is 100 minus the average score of all components
    avg_score = sum(scores.values()) / max(1, len(scores))
    risk_score = round(100 - avg_score)
    
    # Determine risk category
    if risk_score >= 40:
        overall_risk = "High"
    elif risk_score >= 20:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"
        
    # Pick top risks (any score below 75)
    top_risks = [
        f"{area} score is {score}"
        for area, score in sorted(scores.items(), key=lambda item: item[1])
        if score < 75
    ][:5]
    
    state["risk_review"] = {
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "top_risks": top_risks,
        "score_breakdown": scores,
    }
    
    return state

def release_decision_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "Release Decision Agent",
        "Executive Report Agent",
        "release_decision_made",
        _execute,
    )
