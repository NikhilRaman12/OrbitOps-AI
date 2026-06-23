from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RepositoryRequest(BaseModel):
    repository_path: Optional[str] = Field(default=".", description="Local repository path to analyze")
    repository_url: Optional[str] = Field(default=None, description="GitLab repository URL for Orbit context")
    branch: str = Field(default="main", description="Target branch name")

class HandoffMessage(BaseModel):
    id: str
    timestamp: str
    sender: str
    receiver: str
    intent: str
    payload: Dict[str, Any] = Field(default_factory=dict)

class ReleaseDecision(BaseModel):
    release_ready: bool
    blocking_issues: List[str] = Field(default_factory=list)
    approval_status: str = Field(..., description="APPROVED, APPROVED_WITH_WARNINGS, or BLOCKED")

class RiskReview(BaseModel):
    overall_risk: str
    risk_score: int
    top_risks: List[str] = Field(default_factory=list)
    score_breakdown: Dict[str, int] = Field(default_factory=dict)

class RepositoryAnalysis(BaseModel):
    repository_health: int
    active_branches: int
    contributors: int
    source_files: int
    total_files: int
    languages: Dict[str, int] = Field(default_factory=dict)
    risk_files: List[Dict[str, Any]] = Field(default_factory=list)

class ExecutiveSummary(BaseModel):
    summary: str
    recommended_actions: List[str] = Field(default_factory=list)
    release_decision: str

class AnalysisResponse(BaseModel):
    repository_context: Dict[str, Any]
    repository_analysis: Optional[RepositoryAnalysis] = None
    code_review: Optional[Dict[str, Any]] = None
    security_review: Optional[Dict[str, Any]] = None
    dependency_review: Optional[Dict[str, Any]] = None
    documentation_review: Optional[Dict[str, Any]] = None
    cicd_review: Optional[Dict[str, Any]] = None
    ml_review: Optional[Dict[str, Any]] = None
    release_review: Optional[ReleaseDecision] = None
    risk_review: Optional[RiskReview] = None
    executive_summary: Optional[ExecutiveSummary] = None
    a2a_messages: List[HandoffMessage] = Field(default_factory=list)
    recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    agent_status: Dict[str, str] = Field(default_factory=dict)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
