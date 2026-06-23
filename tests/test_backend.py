from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_orbitops_run_returns_core_sections() -> None:
    response = client.post("/api/orbitops/run", json={"repository_path": "."})
    assert response.status_code == 200
    payload = response.json()
    assert payload["repository_analysis"]
    assert payload["executive_summary"]["release_decision"] in {"GO", "NO-GO"}
    assert len(payload["a2a_messages"]) >= 8

