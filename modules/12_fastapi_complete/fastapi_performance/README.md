# FastAPI Performance

Estimated time: 2 hours

## 1. Definition

FastAPI is among the fastest Python web frameworks, but peak throughput requires understanding where bottlenecks arise: blocking I/O in async routes, redundant computation, large uncompressed responses, and unbounded memory usage. Performance optimization targets the largest bottleneck first.

### Key Characteristics

- **`async def` vs `def`**: async routes release the event loop during I/O waits; sync routes run in a thread pool.
- **`asyncio.gather()`**: runs N concurrent I/O operations in parallel; N× faster than sequential.
- **TTL caching**: avoid recomputing expensive aggregations on every request.
- **`StreamingResponse`**: send large datasets in chunks to keep memory flat.
- **`GZipMiddleware`**: compress responses > 1 KB, saving 50–80% bandwidth for JSON.

## 2. Practical Application

### Use Cases

- Concurrent DB lookups for multiple user IDs instead of sequential fetching.
- Caching a complex aggregation (report, count) with a 30-second TTL.
- Streaming 10,000 records from the database to the client without loading all in memory.
- Compressing large catalog responses automatically.

### Code Example

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/batch")
async def get_users_batch(ids: list[int]):
    # Concurrent fetches: ~10ms total instead of N × 10ms
    users = await asyncio.gather(*[fetch_user(uid) for uid in ids])
    return users
```

## 3. Why Is It Important?

### Problem It Solves

A single blocking call in an async route freezes the event loop for all concurrent requests. Sequential I/O for N resources takes N× longer than necessary. Large uncompressed JSON wastes bandwidth.

### Solution and Benefits

Each optimization targets a specific bottleneck: concurrency eliminates sequential I/O wait, TTL caching eliminates redundant computation, streaming prevents OOM on large datasets, and GZip reduces network transfer time.

## 4. References

- [FastAPI Performance](https://fastapi.tiangolo.com/async/)
- [asyncio.gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
- [GZipMiddleware](https://www.starlette.io/middleware/#gzipmiddleware)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Compare sequential vs concurrent fetches for 10 items using `asyncio.gather`. Print elapsed time for both.

### Intermediate Level

Add a TTL cache for `GET /stats` with a 30-second TTL. Verify that the second call within the TTL window is \<1ms while the first is ~50ms.

### Advanced Level

Create `GET /data/stream` that returns 10,000 records using `StreamingResponse` with an async generator. Verify memory usage stays constant.

### Success Criteria

- `asyncio.gather` is at least 5× faster than sequential for 10 items.
- Cached `/stats` returns within 1ms on a cache hit.
- `StreamingResponse` memory usage does not grow with dataset size.

## 6. Summary

FastAPI performance optimisation prioritises I/O concurrency with `asyncio.gather`, avoids redundant computation with TTL caching, handles large datasets with `StreamingResponse`, and reduces bandwidth with `GZipMiddleware`. Profile first — optimise the measured bottleneck.

## 7. Reflection Prompt

The GZip trade-off is CPU (compression work) versus bandwidth (smaller payload). At what payload size does compression become counterproductive? How would you decide the `minimum_size` threshold for `GZipMiddleware`?
