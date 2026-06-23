from __future__ import annotations
from backend.app.agents.base import run_agent
from backend.app.tools.mcp_tools import repository_analysis_tool, code_quality_tool
from backend.app.state import OrbitState

def _execute(state: OrbitState) -> OrbitState:
    path = state.get("repository_context", {}).get("local_path")
    analysis = repository_analysis_tool(path)
    quality = code_quality_tool(path)
    
    # Heuristic for repository health
    health = 95
    if analysis["total_files"] > 500:
        health -= 10
    if len(analysis["risk_files"]) > 0:
        health -= min(15, len(analysis["risk_files"]) * 5)
    if analysis["source_files"] == 0:
        health -= 30
        
    state["repository_analysis"] = {
        "repository_health": max(30, health),
        "active_branches": analysis["active_branches"],
        "contributors": analysis["contributors"],
        "risk_files": analysis["risk_files"],
        "languages": analysis["languages"],
        "source_files": analysis["source_files"],
        "total_files": analysis["total_files"],
    }
    
    state["code_review"] = quality
    
    # Add code quality recommendations to global list
    for rec in quality.get("recommendations", []):
        state.setdefault("recommendations", []).append({
            "area": "code_quality",
            "action": rec
        })
        
    return state

def repository_agent(state: OrbitState) -> OrbitState:
    return run_agent(
        state,
        "Repository Context Agent",
        "Security Agent",
        "repository_context_ready",
        _execute,
    )
