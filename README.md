# Raqib Fraud Detection Service — Lab 3 Starter (SDA-AIE-113)

## What this is

This is the **starting point for Lab 3** — "Containerise the Fraud Service
with Docker." It already contains a **complete, working Lab 1 + Lab 2a
solution**: the domain/service/adapter layers and the FastAPI HTTP layer
are fully implemented, `make serve` runs a working API, and `make test`
is green.

If you finished Lab 2a yourself with a working result, keep using your
own repo instead of this one. This starter exists so nobody falls behind
— everyone begins Lab 3 from the same known-good baseline.

## What already works (Lab 1 + Lab 2a, done for you)

```
src/fraud_service/
├── domain/            # entities.py, policies.py           ✅ implemented
├── service/            # interfaces.py, scorer.py            ✅ implemented
├── adapters/           # sklearn_model.py                    ✅ implemented
├── api/                 # schemas.py, app.py, routes.py       ✅ implemented
├── config.py             #                                     ✅ implemented
└── batch.py               #                                     ✅ implemented — try `make run-batch`
```

```
$ make serve
INFO:     Uvicorn running on http://127.0.0.1:8000

$ curl -s localhost:8000/v1/predict -d '{"transaction_id":"TXN-2026-00042","amount_sar":500,"is_night":0}' -H "content-type: application/json"
{"transaction_id":"TXN-2026-00042","fraud_probability":0.0317,"decision":"allow","model_version":"v3.2.0","trace_id":"a1b2c3d4e5f60718"}
```

`payloads/malformed/` also carries the 40-file malformed-payload corpus
from Day 1, Module 2 — every file in it is rejected by `/v1/predict`
with a 4xx status. Lab 4 reuses this same folder for a parametrised
integration test, so don't delete it.

`BENCHMARKS.md` at the project root already has Day 1's reference
numbers (the `async def` vs plain `def` p99 gap). Lab 3 and Lab 4 each
add their own rows to it — keep it as you go.

## What you build today (Lab 3)

```
Dockerfile                # TODO — multi-stage build (builder + runtime)
.dockerignore              # TODO — keep .git/, notebooks/, tests/, .env out of the build context
docker-compose.yml          # TODO — fraud-api + Redis, gated on health
requirements.lock            # TODO — pip freeze, used by the Dockerfile
scripts/startup_time.sh       # TODO — measures container time-to-ready
Makefile                       # extend with: up, down, image-size, smoke
```

Full step-by-step instructions, expected results, and a troubleshooting
table are in the Day 2 Lab Guide (Lab 3 section) — work through it in
order; this README is just the starting-point map.

## Full project layout

```
fraud-service/
├── src/fraud_service/   (see above)
├── tests/
│   ├── unit/test_policies.py           # existing Lab 1 unit test
│   └── integration/test_api.py         # existing Lab 2a smoke test
├── payloads/malformed/                  # 40-file corpus from Day 1
├── data/transactions_sample.csv
├── models/fraud_model.joblib
├── notebooks/fraud_exploration.ipynb
├── configs/settings.example.env
├── BENCHMARKS.md
├── Makefile
└── pyproject.toml
```

## Quick start

```
pip install -e ".[dev,api]"
make test     # 7 tests, all green
make serve    # http://127.0.0.1:8000/docs
```
