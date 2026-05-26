"""
Basic example: FastAPI Performance
=====================================

FastAPI performance comes from async I/O, connection pooling,
and avoiding unnecessary work. This example demonstrates
measurable, concrete optimizations.

Standalone runnable — no HTTP server needed for the benchmarks.

Demonstrates:
1. Async vs sync endpoint performance (simulated I/O)
2. Response caching with functools.lru_cache and TTL
3. Background pre-computation
4. Streaming large responses (avoids buffering)
5. GZip compression middleware

Run:
    python example_basic.py    ← benchmarks
    uvicorn example_basic:app --reload  ← API
    Visit http://localhost:8000/docs
"""

import asyncio
import gzip
import json
import time
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from threading import Lock

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse

# =============================================================================
# 1. TTL CACHE — avoids repeated expensive computations
# =============================================================================


class TTLCache:
    """
    Simple TTL (time-to-live) cache backed by a dict.

    After `ttl_seconds` the cached value is considered stale and recomputed.
    Thread-safe for synchronous access patterns.
    """

    def __init__(self, ttl_seconds: float = 60.0):
        self._store: dict = {}
        self._lock = Lock()
        self.ttl = ttl_seconds

    def get(self, key: str):
        with self._lock:
            entry = self._store.get(key)
            if entry and datetime.now() < entry["expires"]:
                return entry["value"]
            return None

    def set(self, key: str, value):
        with self._lock:
            self._store[key] = {
                "value": value,
                "expires": datetime.now() + timedelta(seconds=self.ttl),
            }

    def invalidate(self, key: str):
        with self._lock:
            self._store.pop(key, None)


stats_cache = TTLCache(ttl_seconds=30.0)


# =============================================================================
# 2. ASYNC SIMULATION — I/O bound vs CPU bound
# =============================================================================


async def fetch_user_from_db(user_id: int) -> dict:
    """Simulate async DB query (non-blocking)."""
    await asyncio.sleep(0.01)  # 10ms DB round trip
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}


async def fetch_many_users(user_ids: list[int]) -> list[dict]:
    """
    Fetch multiple users concurrently using asyncio.gather.

    Sequential: N × 10ms = N * 10ms total
    Concurrent: max(10ms each) = ~10ms total (N times faster)
    """
    return await asyncio.gather(*[fetch_user_from_db(uid) for uid in user_ids])


def benchmark_async():
    """Compare sequential vs concurrent async fetches."""
    print("─" * 55)
    print("1. ASYNC CONCURRENCY BENCHMARK")
    print("─" * 55)

    user_ids = list(range(1, 11))  # 10 users

    # Sequential
    async def sequential():
        results = []
        for uid in user_ids:
            results.append(await fetch_user_from_db(uid))
        return results

    start = time.perf_counter()
    asyncio.run(sequential())
    seq_time = (time.perf_counter() - start) * 1000

    # Concurrent
    start = time.perf_counter()
    asyncio.run(fetch_many_users(user_ids))
    conc_time = (time.perf_counter() - start) * 1000

    print(f"  Sequential  (10 users × 10ms each): {seq_time:.1f}ms")
    print(f"  Concurrent  (asyncio.gather):        {conc_time:.1f}ms")
    print(f"  Speedup:                             {seq_time / conc_time:.1f}x")


# =============================================================================
# 3. TTL CACHE BENCHMARK
# =============================================================================


def expensive_aggregation(n: int) -> dict:
    """Simulate an expensive DB aggregation (50ms)."""
    time.sleep(0.05)
    return {"count": n, "computed_at": datetime.now().isoformat()}


def benchmark_cache():
    print()
    print("─" * 55)
    print("2. TTL CACHE BENCHMARK")
    print("─" * 55)

    cache = TTLCache(ttl_seconds=5.0)

    times = []
    for i in range(4):
        start = time.perf_counter()
        cached = cache.get("stats")
        if cached is None:
            result = expensive_aggregation(100)
            cache.set("stats", result)
        else:
            result = cached
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
        hit = "MISS" if i == 0 else "HIT "
        print(f"  Request {i + 1} [{hit}]: {elapsed:.2f}ms  →  {result['computed_at'][:19]}")

    speedup = times[0] / max(times[1], 0.001)
    print(f"  Cache speedup: {speedup:.0f}x faster on hits")


# =============================================================================
# 4. RESPONSE SIZE — GZIP COMPRESSION
# =============================================================================


def benchmark_gzip():
    print()
    print("─" * 55)
    print("3. GZIP COMPRESSION")
    print("─" * 55)

    data = json.dumps([{"id": i, "name": f"Item {i}", "desc": "A " * 50} for i in range(200)])
    original = data.encode()
    compressed = gzip.compress(original, compresslevel=6)

    ratio = len(compressed) / len(original)
    print(f"  Uncompressed: {len(original):,} bytes")
    print(f"  Compressed:   {len(compressed):,} bytes ({ratio:.1%} of original)")
    print(f"  Savings:      {len(original) - len(compressed):,} bytes ({1 - ratio:.0%})")
    print("  GZipMiddleware applies this automatically when:")
    print("    - minimum_size=1000 (bytes) threshold is met")
    print("    - Client sends Accept-Encoding: gzip header")


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="FastAPI Performance Example", version="1.0.0")

# GZip compresses responses larger than 1KB when client supports it
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/users/concurrent")
async def get_users_concurrent(count: int = 10):
    """
    Fetch multiple users concurrently with asyncio.gather.

    Much faster than sequential awaits for I/O-bound operations.
    """
    user_ids = list(range(1, min(count + 1, 51)))
    start = time.perf_counter()
    users = await fetch_many_users(user_ids)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "users": users,
        "count": len(users),
        "elapsed_ms": round(elapsed_ms, 2),
    }


@app.get("/stats/cached")
async def get_stats_cached():
    """
    Return statistics, using TTL cache to avoid repeated computation.

    First call: ~50ms (recomputes). Subsequent calls within 30s: <1ms.
    """
    cached = stats_cache.get("global_stats")
    if cached is not None:
        return {"data": cached, "source": "cache"}

    # Simulate expensive aggregation
    await asyncio.sleep(0.05)
    result = {
        "total_users": 12345,
        "active_today": 987,
        "computed_at": datetime.now().isoformat(),
    }
    stats_cache.set("global_stats", result)
    return {"data": result, "source": "computed"}


@app.get("/data/stream")
async def stream_large_response():
    """
    Stream a large dataset instead of buffering it in memory.

    StreamingResponse sends each chunk as it's generated,
    keeping memory usage flat regardless of dataset size.
    """

    async def generate() -> AsyncGenerator[str, None]:
        yield '{"items":['
        for i in range(1000):
            row = json.dumps({"id": i, "value": f"item_{i}"})
            if i > 0:
                yield ","
            yield row
            if i % 100 == 0:
                await asyncio.sleep(0)  # yield control to event loop
        yield "]}"

    return StreamingResponse(generate(), media_type="application/json")


@app.get("/")
async def root():
    return {
        "message": "FastAPI Performance Demo",
        "tips": [
            "Use async def for I/O-bound routes",
            "Use asyncio.gather for concurrent I/O",
            "Cache expensive computations with TTL",
            "Stream large responses with StreamingResponse",
            "GZipMiddleware reduces transfer size automatically",
        ],
        "docs": "/docs",
    }


# =============================================================================
# MAIN
# =============================================================================


def main():
    """Entry point to demonstrate the implementation."""
    print("=" * 55)
    print("FASTAPI PERFORMANCE — DEMO")
    print("=" * 55)
    benchmark_async()
    benchmark_cache()
    benchmark_gzip()
    print()
    print("─" * 55)
    print("4. PERFORMANCE TIPS SUMMARY")
    print("─" * 55)
    tips = [
        ("Use async def", "Releases event loop during I/O waits"),
        ("asyncio.gather()", "N concurrent I/O ops in ~1 round-trip time"),
        ("TTL cache", "Avoid re-running expensive aggregations"),
        ("StreamingResponse", "Flat memory for large datasets"),
        ("GZipMiddleware", "50-80% bandwidth reduction for JSON"),
        ("Connection pooling", "Reuse DB connections (pool_size=10)"),
        ("response_model_exclude_unset", "Skip serializing null fields"),
        ("Avoid sync in async", "Use run_in_executor for CPU-heavy ops"),
    ]
    for tip, detail in tips:
        print(f"  {tip:<30} — {detail}")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 55)


if __name__ == "__main__":
    main()
