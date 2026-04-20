# Redis Caching

Estimated time: 2 hours

## 1. Definition

**Redis** is an in-memory data store commonly used as a cache. The **cache-aside** (lazy loading) pattern reads from the cache first; on a miss, fetches from the source of truth, stores the result in Redis, then returns it. Subsequent requests within the TTL window hit the cache instead.

### Key Characteristics

- **Cache-aside**: read from cache → miss → read from DB → write to cache → return.
- **TTL (Time to Live)**: Redis automatically evicts entries after the configured seconds.
- **Cache invalidation**: when data changes, explicitly delete the cached key.
- **Key namespacing**: prefix keys (`myapp:product:1`) to avoid collisions.
- **JSON serialization**: store Python objects as JSON strings; deserialize on read.

## 2. Practical Application

### Use Cases

- Caching expensive `GET /reports/summary` aggregations (TTL 60s).
- Caching per-product data (`GET /products/1`) with invalidation on `PUT /products/1`.
- Caching full list responses (`GET /products`) with a short TTL (10s).
- Session storage: user session data with sliding TTL.

### Code Example

```python
import json, redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_product(product_id: int):
    key = f"product:{product_id}"
    cached = client.get(key)
    if cached:
        return json.loads(cached)  # cache hit
    product = db.query_product(product_id)  # cache miss
    client.set(key, json.dumps(product), ex=30)
    return product
```

## 3. Why Is It Important?

### Problem It Solves

Repeated DB aggregations for the same data on every request waste DB resources and add latency. Under load, a query that takes 100ms per call at 100 req/s generates 10 full DB aggregations per second.

### Solution and Benefits

A cache hit takes \<1ms. The same query at 100 req/s now runs once per TTL window (e.g. every 30 seconds) instead of 100 times per second — a 3,000× reduction in DB load.

## 4. References

- [Redis Documentation](https://redis.io/docs/)
- [redis-py](https://redis-py.readthedocs.io/)
- [Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Implement `GET /products/{id}` with cache-aside using an in-memory dict as a mock cache. Return `{"_cache": "HIT"}` or `{"_cache": "MISS"}` to show which path was taken.

### Intermediate Level

Implement `PUT /products/{id}` that updates the product and explicitly deletes the cache key (`cache_delete(key)`). Verify the next `GET` is a MISS.

### Advanced Level

Connect to a real Redis instance (or use `fakeredis`). Add `GET /cache/stats` that lists current keys and their TTLs. Add `DELETE /cache` to flush all keys in the namespace.

### Success Criteria

- First `GET /products/1`: MISS (~50ms simulated).
- Second `GET /products/1` within TTL: HIT (\<1ms).
- After `PUT /products/1`: next GET is MISS again.

## 6. Summary

The cache-aside pattern decouples the cache from the data source. Redis TTL handles expiry automatically. Explicit invalidation on write keeps the cache consistent. Key namespacing prevents collisions across services. In production, use Redis with persistence enabled for durability.

## 7. Reflection Prompt

Cache invalidation is one of the hardest problems in computer science. If you have a product that is referenced in three different cache keys (single product, category list, search results), how would you ensure all three are invalidated when the product is updated?
