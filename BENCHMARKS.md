# Benchmarks

Numbers measured against the reference course laptop. Record your own
measurements in the same table — your machine will differ, and that is
expected; what matters is the *shape* of the result (which row is faster,
and by roughly how much), not matching these numbers exactly.

## Day 1 — Module 2 (FastAPI hardening)

| Metric | `async def` (bug) | plain `def` (fixed) |
|---|---|---|
| p50 latency | — | 15 ms |
| p99 latency | 2.4 s | 38 ms |
| Throughput (c=25) | 118 req/s | 1,410 req/s |

- Load test: `hey -n 2000 -c 25 -m POST -D sample.json`
- Malformed corpus: 40/40 payloads rejected with 4xx (`payloads/malformed/`)
- Valid-traffic error rate: 0 non-2xx responses

## Day 2 — Lab 3 (Docker)

_Fill in as you complete each step:_

| Metric | Value |
|---|---|
| Naive build — image size | 1.01 GB |
| Naive build — cold build time | ~100 s |
| Multi-stage build — image size | 813 MB |
| Multi-stage build — cold build time | ~100 s |
| Warm rebuild (one-line code change) | ~52 s (CACHED confirmed) |
| p99 — bare metal (Lab 2, no container) | 38 ms |
| p99 — containerised | 96 ms (custom Python load test, hey unavailable) |
| Time-to-ready (`scripts/startup_time.sh`) | ~0-7 s (already warm) |

## Day 2 — Lab 4 (Tests)

_Fill in after Lab 4 Step 6:_

| Metric | Value |
|---|---|
| `pytest -m "not slow"` — pass count / duration | |
| `pytest -m slow` — pass count / duration | |
| Branch coverage (domain + service + api) | |
