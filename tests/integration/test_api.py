"""Lab 2a optional check: exercise the FastAPI app without a live server.

This will be replaced/extended by a proper integration suite in Lab 4
(tests/integration/test_predict_api.py) — this file just proves the
wiring works end to end today.
"""
import pytest
from fastapi.testclient import TestClient

from fraud_service.api.app import app


@pytest.fixture
def client():
    # the `with` block runs the FastAPI lifespan (model load) on entry
    # and tears it down on exit — a bare TestClient(app) never loads it.
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/v1/health")
    assert response.status_code == 200


def test_predict_valid(client):
    response = client.post("/v1/predict", json={
        "transaction_id": "TXN-TEST-0001",
        "amount_sar": 500.0,
        "is_night": 0,
    })
    assert response.status_code == 200
    assert "fraud_probability" in response.json()
