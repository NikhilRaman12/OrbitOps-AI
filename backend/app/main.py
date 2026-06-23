from __future__ import annotations
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models import RepositoryRequest, AnalysisResponse
from backend.app.services.orbit_service import OrbitOpsService

app = FastAPI(
    title="OrbitOps AI",
    description="Autonomous DevMLSecOps Intelligence Platform powered by GitLab Orbit context.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = OrbitOpsService()

# Realistic pre-compiled demo state for offline testing
DEMO_STATE = {
    "run_id": "demo-run-uuid-1234",
    "repository_context": {
        "provider": "gitlab-orbit",
        "repository_url": "https://github.com/NikhilRaman12/OrbitOps-AI.git",
        "default_branch": "main",
        "context_freshness": "live-gitlab-orbit",
        "integration_status": "active",
        "orbit_metadata": {
            "project_id": "orbitops-ai-demo",
            "api_endpoint": "https://gitlab.com/api/v4",
            "duo_chat_enabled": True,
            "context_tokens_analyzed": 5120
        }
    },
    "repository_analysis": {
        "repository_health": 88,
        "active_branches": 3,
        "contributors": 4,
        "source_files": 32,
        "total_files": 45,
        "languages": {".py": 16, ".jsx": 8, ".css": 2, ".yml": 4, ".json": 3},
        "risk_files": [
            {"path": "frontend/package-lock.json", "size_kb": 75.6}
        ]
    },
    "code_review": {
        "quality_score": 85,
        "total_lines": 3450,
        "critical_smells": [],
        "recommendations": [
            "Break down long functions and isolate orchestration from business rules.",
            "Refactor code lines exceeding 120 characters in highlighted areas."
        ]
    },
    "security_review": {
        "security_score": 92,
        "critical_findings": [],
        "insecure_configs": [
            {"severity": "medium", "type": "cors_allow_all", "path": "backend/app/main.py", "description": "Insecure config pattern 'cors_allow_all' detected"}
        ],
        "owasp_coverage": ["secrets", "insecure-configs-heuristics", "tls-validation"]
    },
    "dependency_review": {
        "dependency_score": 85,
        "manifests": ["requirements.txt", "frontend/package.json"],
        "risky_dependencies": [
            {"package": "urllib3", "file": "requirements.txt", "severity": "medium", "description": "urllib3 v1 is deprecated and has multiple CVEs. Upgrade to v2"}
        ],
        "packages_count": 18
    },
    "documentation_review": {
        "documentation_score": 76,
        "readme_present": True,
        "missing_sections": ["security", "api"],
        "recommendations": ["Document runbooks, environment variables, and deployment gates in README."]
    },
    "cicd_review": {
        "pipeline_health": 90,
        "pipeline_present": True,
        "docker_present": True,
        "compose_present": True,
        "tests_present": True,
        "checks_passed": [
            "GitLab CI pipeline configuration found",
            "Dockerfile found",
            "Docker Compose setup found",
            "Tests folder found"
        ],
        "recommendations": []
    },
    "ml_review": {
        "governance_score": 50,
        "ml_detected": True,
        "frameworks": ["sklearn"],
        "model_files": [],
        "model_card_present": False,
        "dataset_card_present": False,
        "governance_status": "manual-review-required",
        "recommendations": [
            "Add MODEL_CARD.md documenting model specifications, usage limits, and performance metrics.",
            "Add DATASET_CARD.md outlining dataset origin, licensing, and leakage risk checks."
        ]
    },
    "release_review": {
        "release_ready": True,
        "blocking_issues": [],
        "approval_status": "APPROVED_WITH_WARNINGS",
        "readiness_score": 81
    },
    "risk_review": {
        "overall_risk": "Medium",
        "risk_score": 24,
        "top_risks": [
            "ml_governance score is 50",
            "documentation score is 76"
        ],
        "score_breakdown": {
            "repository": 88,
            "code": 85,
            "security": 92,
            "dependency": 85,
            "documentation": 76,
            "pipeline": 90,
            "ml_governance": 50
        }
    },
    "executive_summary": {
        "summary": "OrbitOps completed autonomous review of the repository. Overall risk is categorized as Medium with a score of 24/100. The autonomous Release Decision Agent has determined that deployment is APPROVED_WITH_WARNINGS.",
        "critical_findings": [
            "ml_governance score is 50",
            "documentation score is 76"
        ],
        "recommended_actions": [
            "Break down long functions and isolate orchestration from business rules.",
            "Refactor code lines exceeding 120 characters in highlighted areas.",
            "Resolve insecure config 'cors_allow_all' in backend/app/main.py.",
            "Upgrade urllib3 in requirements.txt: urllib3 v1 is deprecated and has multiple CVEs. Upgrade to v2.",
            "Add README section for 'security'.",
            "Add README section for 'api'.",
            "Add MODEL_CARD.md documenting model specifications, usage limits, and performance metrics.",
            "Add DATASET_CARD.md outlining dataset origin, licensing, and leakage risk checks."
        ],
        "release_decision": "APPROVED_WITH_WARNINGS",
        "explanation": "The project has an overall readiness score of 81/100. Deployment status is 'APPROVED_WITH_WARNINGS' based on evaluated security, dependency, pipeline, and documentation posture. Review the dashboard metrics to remediate any warnings."
    },
    "recommendations": [
        {"area": "code_quality", "action": "Break down long functions and isolate orchestration from business rules."},
        {"area": "code_quality", "action": "Refactor code lines exceeding 120 characters in highlighted areas."},
        {"area": "security", "action": "Resolve insecure config 'cors_allow_all' in backend/app/main.py."},
        {"area": "dependency", "action": "Upgrade urllib3 in requirements.txt: urllib3 v1 is deprecated and has multiple CVEs. Upgrade to v2."},
        {"area": "documentation", "action": "Add README section for 'security'."},
        {"area": "documentation", "action": "Add README section for 'api'."},
        {"area": "ml_governance", "action": "Add MODEL_CARD.md documenting model specifications, usage limits, and performance metrics."},
        {"area": "ml_governance", "action": "Add DATASET_CARD.md outlining dataset origin, licensing, and leakage risk checks."}
    ],
    "agent_status": {
        "Repository Context Agent": "completed",
        "Security Agent": "completed",
        "Dependency Agent": "completed",
        "Documentation Agent": "completed",
        "CI/CD Agent": "completed",
        "ML Governance Agent": "completed",
        "Release Decision Agent": "completed",
        "Executive Report Agent": "completed"
    },
    "a2a_messages": [
        {"id": "msg-1", "timestamp": "2026-06-23T18:00:01Z", "sender": "Repository Context Agent", "receiver": "Security Agent", "intent": "repository_context_ready", "payload": {}},
        {"id": "msg-2", "timestamp": "2026-06-23T18:00:03Z", "sender": "Security Agent", "receiver": "Dependency Agent", "intent": "security_review_ready", "payload": {}},
        {"id": "msg-3", "timestamp": "2026-06-23T18:00:05Z", "sender": "Dependency Agent", "receiver": "Documentation Agent", "intent": "dependency_review_ready", "payload": {}},
        {"id": "msg-4", "timestamp": "2026-06-23T18:00:07Z", "sender": "Documentation Agent", "receiver": "CI/CD Agent", "intent": "documentation_review_ready", "payload": {}},
        {"id": "msg-5", "timestamp": "2026-06-23T18:00:09Z", "sender": "CI/CD Agent", "receiver": "ML Governance Agent", "intent": "cicd_review_ready", "payload": {}},
        {"id": "msg-6", "timestamp": "2026-06-23T18:00:11Z", "sender": "ML Governance Agent", "receiver": "Release Decision Agent", "intent": "ml_governance_ready", "payload": {}},
        {"id": "msg-7", "timestamp": "2026-06-23T18:00:13Z", "sender": "Release Decision Agent", "receiver": "Executive Report Agent", "intent": "release_decision_made", "payload": {}},
        {"id": "msg-8", "timestamp": "2026-06-23T18:00:15Z", "sender": "Executive Report Agent", "receiver": "Dashboard", "intent": "executive_report_ready", "payload": {}}
    ],
    "timeline": [
        {"agent": "Repository Context Agent", "handoff_to": "Security Agent", "intent": "repository_context_ready", "timestamp": "2026-06-23T18:00:01Z"},
        {"agent": "Security Agent", "handoff_to": "Dependency Agent", "intent": "security_review_ready", "timestamp": "2026-06-23T18:00:03Z"},
        {"agent": "Dependency Agent", "handoff_to": "Documentation Agent", "intent": "dependency_review_ready", "timestamp": "2026-06-23T18:00:05Z"},
        {"agent": "Documentation Agent", "handoff_to": "CI/CD Agent", "intent": "documentation_review_ready", "timestamp": "2026-06-23T18:00:07Z"},
        {"agent": "CI/CD Agent", "handoff_to": "ML Governance Agent", "intent": "cicd_review_ready", "timestamp": "2026-06-23T18:00:09Z"},
        {"agent": "ML Governance Agent", "handoff_to": "Release Decision Agent", "intent": "ml_governance_ready", "timestamp": "2026-06-23T18:00:11Z"},
        {"agent": "Release Decision Agent", "handoff_to": "Executive Report Agent", "intent": "release_decision_made", "timestamp": "2026-06-23T18:00:13Z"},
        {"agent": "Executive Report Agent", "handoff_to": "Dashboard", "intent": "executive_report_ready", "timestamp": "2026-06-23T18:00:15Z"}
    ]
}

@app.get("/")
def root() -> Dict[str, str]:
    return {
        "name": "OrbitOps AI",
        "status": "online",
        "tagline": "Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit"
    }

@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "healthy"}

@app.get("/api/demo", response_model=AnalysisResponse)
def demo() -> Dict[str, Any]:
    return DEMO_STATE

@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(request: RepositoryRequest) -> Dict[str, Any]:
    try:
        return service.run(request.repository_path, request.repository_url, request.branch)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/orbitops/run", response_model=AnalysisResponse)
def run_orbitops(request: RepositoryRequest) -> Dict[str, Any]:
    """Alias for backwards compatibility with the frontend."""
    return analyze(request)

@app.get("/api/report/{run_id}", response_model=AnalysisResponse)
def get_report(run_id: str) -> Dict[str, Any]:
    report = service.get_run(run_id)
    if not report:
        # Fallback to demo state if report run_id is demo or not found
        if run_id == "demo-run-uuid-1234" or run_id == "demo":
            return DEMO_STATE
        raise HTTPException(status_code=404, detail=f"Report with run ID {run_id} not found.")
    return report
