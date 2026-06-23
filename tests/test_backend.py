from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_demo_endpoint() -> None:
    response = client.get("/api/demo")
    assert response.status_code == 200
    payload = response.json()
    assert payload["run_id"] == "demo-run-uuid-1234"
    assert payload["repository_context"]["provider"] == "gitlab-orbit"
    assert payload["release_review"]["approval_status"] == "APPROVED_WITH_WARNINGS"
    assert len(payload["a2a_messages"]) == 8
    assert len(payload["timeline"]) == 8

def test_analyze_endpoint_and_report_fetching() -> None:
    response = client.post("/api/analyze", json={"repository_path": "."})
    assert response.status_code == 200
    payload = response.json()
    
    # Assert core components exist
    assert "run_id" in payload
    assert "repository_context" in payload
    assert "repository_analysis" in payload
    assert "code_review" in payload
    assert "security_review" in payload
    assert "dependency_review" in payload
    assert "documentation_review" in payload
    assert "cicd_review" in payload
    assert "ml_review" in payload
    assert "release_review" in payload
    assert "risk_review" in payload
    assert "executive_summary" in payload
    assert "a2a_messages" in payload
    assert "agent_status" in payload
    
    # Verify release gate details
    assert payload["release_review"]["approval_status"] in {"APPROVED", "APPROVED_WITH_WARNINGS", "BLOCKED"}
    assert len(payload["a2a_messages"]) == 8
    
    # Verify we can fetch the run using get_report
    run_id = payload["run_id"]
    report_response = client.get(f"/api/report/{run_id}")
    assert report_response.status_code == 200
    assert report_response.json()["run_id"] == run_id

def test_orbitops_run_compat_alias() -> None:
    response = client.post("/api/orbitops/run", json={"repository_path": "."})
    assert response.status_code == 200
    payload = response.json()
    assert "repository_analysis" in payload
    assert "executive_summary" in payload
    assert len(payload["a2a_messages"]) == 8
