import pytest

pytestmark = [pytest.mark.behavioural]


def _score(model, txn):
    return model.predict_proba(txn.to_features().values)


def test_invariance_to_transaction_id_casing(real_model, sample_txn):
    a = _score(real_model, sample_txn)
    b = _score(real_model, sample_txn.model_copy(
        update={"transaction_id": sample_txn.transaction_id.lower()}))
    assert a == pytest.approx(b, abs=1e-9)


def test_directional_amount(real_model, sample_txn):
    small = _score(real_model, sample_txn.model_copy(
        update={"amount_sar": 50.0}))
    large = _score(real_model, sample_txn.model_copy(
        update={"amount_sar": 50_000.0}))
    assert large >= small - 1e-6