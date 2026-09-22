import json
import pathlib

import pytest
from fastapi.testclient import TestClient

from fraud_service.api.app import create_app

MALFORMED = sorted(
    pathlib.Path("payloads/malformed").glob("*.json"))


@pytest.mark.integration
def test_predict_contract(client_factory, sample_txn):
    client = client_factory(probability=0.93)  # forces block
    r = client.post("/v1/predict",
                     json=json.loads(sample_txn.model_dump_json()))
    assert r.status_code == 200
    assert r.json()["decision"] == "block"


@pytest.mark.integration
@pytest.mark.parametrize("payload_file", MALFORMED)
def test_malformed_corpus_rejected(client_factory, payload_file):
    r = client_factory().post("/v1/predict",
                               content=payload_file.read_bytes(),
                               headers={"content-type": "application/json"})
    assert 400 <= r.status_code < 500, payload_file.name


@pytest.mark.integration
def test_predict_500_hides_stack_trace(client_factory, sample_txn,
                                        monkeypatch):
    client = client_factory()

    def boom(self, txn):
        raise ZeroDivisionError("seeded failure")

    monkeypatch.setattr(
        "fraud_service.service.scorer.FraudScorer.score", boom)
    r = client.post("/v1/predict",
                     json=json.loads(sample_txn.model_dump_json()))
    assert r.status_code == 500
    assert "ZeroDivisionError" not in r.text


@pytest.mark.integration
def test_predict_503_when_model_not_ready():
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    r = client.post("/v1/predict", json={
        "transaction_id": "TXN-TEST-1", "amount_sar": 500, "is_night": 0
    })
    assert r.status_code == 503
    assert r.headers.get("Retry-After") == "5"


@pytest.mark.integration
def test_ready_503_when_model_not_ready():
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    r = client.get("/v1/ready")
    assert r.status_code == 503


@pytest.mark.integration
def test_lifespan_loads_real_model():
    app = create_app()
    with TestClient(app) as client:
        r = client.get("/v1/ready")
        assert r.status_code == 200
        assert r.json()["status"] == "ready"