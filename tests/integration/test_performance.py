"""T021 — SC-003: p95 redirect latency < 100 ms (local smoke test)."""
import statistics
import time


def test_redirect_p95_under_100ms(client, make_link):
    code = make_link().json()["code"]
    samples = []
    for _ in range(200):
        start = time.perf_counter()
        client.get(f"/{code}")
        samples.append((time.perf_counter() - start) * 1000)
    p95 = statistics.quantiles(samples, n=20)[18]
    assert p95 < 100, f"p95 = {p95:.1f} ms"
