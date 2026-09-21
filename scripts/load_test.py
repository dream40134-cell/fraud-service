import asyncio
import time
import httpx

URL = "http://localhost:8000/v1/predict"
PAYLOAD = {"transaction_id": "TXN-TEST-1", "amount_sar": 500, "is_night": 0}
DURATION = 30  # seconds
CONCURRENCY = 10

async def worker(client, stats, stop_time):
    while time.time() < stop_time:
        start = time.time()
        try:
            r = await client.post(URL, json=PAYLOAD, timeout=10)
            elapsed = time.time() - start
            stats.append((elapsed, r.status_code))
        except Exception:
            stats.append((time.time() - start, 0))

async def main():
    stats = []
    stop_time = time.time() + DURATION
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[
            worker(client, stats, stop_time) for _ in range(CONCURRENCY)
        ])

    latencies = sorted([s[0] for s in stats])
    n = len(latencies)
    if n == 0:
        print("No requests completed.")
        return
    p50 = latencies[int(n * 0.5)] * 1000
    p99 = latencies[int(n * 0.99)] * 1000
    success = sum(1 for _, code in stats if code == 200)
    print(f"Total requests: {n}")
    print(f"Success: {success} / {n}")
    print(f"p50 latency: {p50:.1f} ms")
    print(f"p99 latency: {p99:.1f} ms")
    print(f"Throughput: {n / DURATION:.1f} req/s")

asyncio.run(main())