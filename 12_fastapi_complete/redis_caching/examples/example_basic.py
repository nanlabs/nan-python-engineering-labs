"""
Basic example: Redis Caching
================================

Redis is a fast in-memory data store commonly used for caching
API responses, session data, and computed results.

This standalone script demonstrates Redis caching patterns
WITHOUT requiring a Redis server — using a mock that simulates
the same interface so the logic runs identically.

Demonstrates:
1. Cache-aside pattern (read-through, lazy population)
2. TTL-based expiration
3. Cache invalidation on update
4. Cache key namespacing
5. Connection pooling strategy

To use a real Redis:
    pip install redis
    docker run -d -p 6379:6379 redis:7-alpine

Run:
    python example_basic.py
    uvicorn example_basic:app --reload  (uses mock Redis unless real one is available)
"""

import json
import time
from datetime import datetime
from typing import Optional, Any

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel


# =============================================================================
# 1. MOCK REDIS (same interface as redis.Redis)
# =============================================================================


class MockRedis:
    """
    In-memory Redis mock for demo purposes.

    Supports: get, set, delete, exists, keys, flushdb.
    TTL is enforced on every get().
    """

    def __init__(self):
        self._store: dict[str, tuple[Any, Optional[float]]] = {}

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        expires_at = time.time() + ex if ex else None
        self._store[key] = (value, expires_at)
        return True

    def get(self, key: str) -> Optional[str]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at and time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def delete(self, *keys: str) -> int:
        count = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                count += 1
        return count

    def exists(self, key: str) -> int:
        return 1 if self.get(key) is not None else 0

    def keys(self, pattern: str = "*") -> list[str]:
        import fnmatch
        all_keys = list(self._store.keys())
        if pattern == "*":
            return all_keys
        return [k for k in all_keys if fnmatch.fnmatch(k, pattern)]

    def flushdb(self) -> bool:
        self._store.clear()
        return True

    def ttl(self, key: str) -> int:
        entry = self._store.get(key)
        if entry is None:
            return -2  # Key does not exist
        _, expires_at = entry
        if expires_at is None:
            return -1  # No expiry
        remaining = int(expires_at - time.time())
        return max(remaining, 0)


# =============================================================================
# 2. CACHE CLIENT SETUP
# =============================================================================

# Try to connect to a real Redis; fall back to the mock
def get_redis_client():
    try:
        import redis
        client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        client.ping()  # raises ConnectionError if not available
        print("[redis] Connected to real Redis at localhost:6379")
        return client
    except Exception:
        print("[redis] Redis not available — using in-memory mock")
        return MockRedis()


redis_client = get_redis_client()


# =============================================================================
# 3. CACHE HELPERS
# =============================================================================

CACHE_PREFIX = "fastapi_demo"
DEFAULT_TTL = 30  # seconds


def cache_key(*parts: str) -> str:
    """Build a namespaced cache key."""
    return f"{CACHE_PREFIX}:{':'.join(parts)}"


def cache_get(key: str) -> Optional[Any]:
    """Deserialize a cached JSON value."""
    raw = redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    """Serialize and store a value with TTL."""
    redis_client.set(key, json.dumps(value, default=str), ex=ttl)


def cache_delete(key: str) -> None:
    redis_client.delete(key)


def cache_delete_pattern(pattern: str) -> int:
    """Delete all keys matching a pattern (use with caution in production)."""
    keys = redis_client.keys(pattern)
    if keys:
        return redis_client.delete(*keys)
    return 0


# =============================================================================
# 4. MODELS AND FAKE DB
# =============================================================================


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    updated_at: datetime


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


_db: dict[int, Product] = {
    1: Product(id=1, name="Widget A", price=9.99, stock=100, updated_at=datetime.now()),
    2: Product(id=2, name="Widget B", price=19.99, stock=50, updated_at=datetime.now()),
    3: Product(id=3, name="Widget C", price=4.99, stock=200, updated_at=datetime.now()),
}


# =============================================================================
# 5. APP
# =============================================================================

app = FastAPI(title="Redis Caching Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Redis Caching Demo", "docs": "/docs"}


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """
    Cache-aside pattern:
    1. Check cache → return if found (cache HIT)
    2. Query DB (cache MISS) → store in cache → return
    """
    key = cache_key("product", str(product_id))
    cached = cache_get(key)

    if cached is not None:
        cached["_cache"] = "HIT"
        return cached

    # Cache miss — fetch from DB
    product = _db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    data = product.model_dump()
    cache_set(key, data, ttl=30)
    data["_cache"] = "MISS"
    return data


@app.put("/products/{product_id}")
async def update_product(product_id: int, updates: ProductUpdate):
    """
    Update a product and invalidate its cache entry.

    Cache invalidation ensures the next GET fetches fresh data.
    """
    product = _db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated = product.model_copy(
        update={k: v for k, v in updates.model_dump().items() if v is not None}
    )
    updated = updated.model_copy(update={"updated_at": datetime.now()})
    _db[product_id] = updated

    # Invalidate the specific product cache
    key = cache_key("product", str(product_id))
    cache_delete(key)

    return {"updated": updated, "cache": "INVALIDATED"}


@app.get("/products")
async def list_products():
    """
    Cache the entire product list with a short TTL (10s).

    Since lists change more frequently, keep TTL lower.
    """
    key = cache_key("products", "all")
    cached = cache_get(key)

    if cached is not None:
        return {"products": cached, "_cache": "HIT"}

    products = [p.model_dump() for p in _db.values()]
    cache_set(key, products, ttl=10)
    return {"products": products, "_cache": "MISS"}


@app.delete("/cache")
async def flush_cache():
    """Flush all keys in the demo namespace (admin operation)."""
    deleted = cache_delete_pattern(f"{CACHE_PREFIX}:*")
    return {"flushed": deleted, "message": "Cache cleared"}


@app.get("/cache/stats")
async def cache_stats():
    """Show current cache keys and their TTLs."""
    keys = redis_client.keys(f"{CACHE_PREFIX}:*")
    stats = []
    for key in keys:
        stats.append({
            "key": key,
            "ttl_seconds": redis_client.ttl(key),
        })
    return {"entries": stats, "count": len(stats)}


# =============================================================================
# 6. STANDALONE DEMO
# =============================================================================


def benchmark():
    print("=" * 60)
    print("REDIS CACHING — DEMO")
    print("=" * 60)
    print()
    print("Simulating cache-aside pattern with 3 products:")
    print()

    client = MockRedis()

    def get_product_demo(product_id: int):
        key = f"product:{product_id}"
        cached = client.get(key)
        if cached:
            return json.loads(cached), "HIT"
        # Simulate DB query
        time.sleep(0.05)
        data = {"id": product_id, "name": f"Product {product_id}", "price": 9.99}
        client.set(key, json.dumps(data), ex=30)
        return data, "MISS"

    for product_id in [1, 2, 1, 1, 2, 3]:
        start = time.perf_counter()
        data, cache_status = get_product_demo(product_id)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  GET product/{product_id}  [{cache_status}]  {elapsed:.2f}ms")

    print()
    print("Cache keys:", client.keys("product:*"))
    print()
    print("Key patterns:")
    print(f"  {CACHE_PREFIX}:product:1     → single product (TTL 30s)")
    print(f"  {CACHE_PREFIX}:products:all  → product list (TTL 10s)")
    print()
    print("Cache invalidation:")
    print("  PUT /products/1  → deletes 'product:1' key immediately")
    print("  Next GET         → cache MISS → fresh DB fetch → re-cached")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    benchmark()
