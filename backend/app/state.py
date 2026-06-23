from __future__ import annotations
from typing import Any, Dict, List, TypedDict

class OrbitState(TypedDict, total=False):
    repository_context: Dict[str, Any]
    repository_analysis: Dict[str, Any]
    code_review: Dict[str, Any]
    security_review: Dict[str, Any]
    dependency_review: Dict[str, Any]
    documentation_review: Dict[str, Any]
    cicd_review: Dict[str, Any]
    ml_review: Dict[str, Any]
    release_review: Dict[str, Any]
    risk_review: Dict[str, Any]
    executive_summary: Dict[str, Any]
    a2a_messages: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    agent_status: Dict[str, str]

def initial_state(repository_context: Dict[str, Any] | None = None) -> OrbitState:
    return {
        "repository_context": repository_context or {},
        "repository_analysis": {},
        "code_review": {},
        "security_review": {},
        "dependency_review": {},
        "documentation_review": {},
        "cicd_review": {},
        "ml_review": {},
        "release_review": {},
        "risk_review": {},
        "executive_summary": {},
        "a2a_messages": [],
        "recommendations": [],
        "agent_status": {},
    }
