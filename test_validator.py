from fastapi.testclient import TestClient

from validation_agent import app


def test_validator_accepts_simple_code() -> None:
    client = TestClient(app)
    response = client.post("/validate", json={"code": "print('hello world')"})

    assert response.status_code == 200
    assert response.json()["risk_level"] == "low"
