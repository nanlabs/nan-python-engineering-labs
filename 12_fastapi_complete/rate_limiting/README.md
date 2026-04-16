# Rate Limiting

Estimated time: 90 minutes

## 1. Definition

**Rate limiting** restricts how many requests a client can make within a time window, protecting your API from brute-force attacks, abusive usage, and accidental DoS caused by runaway clients.

### Key Characteristics

- **Token bucket**: client starts with N tokens; each request costs one; tokens refill at a fixed rate.
- **Sliding window**: tracks timestamps of past requests; allows at most N within the last T seconds.
- **Fixed window**: simpler counter per window period; vulnerable to burst at window boundary.
- **Key**: rate-limit per IP, per API key, or per user ID.
- **Redis-backed**: distributed rate limiting for multi-instance deployments.

## 2. Practical Application

### Use Cases

- `POST /login`: max 5 attempts per IP per minute (brute-force protection).
- `POST /send-email`: max 10 per user per hour (spam prevention).
- Public read APIs: max 100 req/min per IP (prevent scraping).
- Paid tiers: 1,000 req/min for Pro, 100 req/min for Free.

### Code Example

```python
import time
from fastapi import FastAPI, Request, HTTPException

_buckets: dict[str, list[float]] = {}

def check_rate_limit(key: str, max_calls: int = 10, window: float = 60.0):
    now = time.time()
    bucket = [t for t in _buckets.get(key, []) if t > now - window]
    if len(bucket) >= max_calls:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)
    _buckets[key] = bucket
```

## 3. Why Is It Important?

### Problem It Solves

Without rate limiting, a single malicious or buggy client can exhaust server resources, overwhelm a database, or brute-force credentials. APIs exposed to the internet are probed constantly.

### Solution and Benefits

Rate limiting caps the blast radius of any single client. It defends login endpoints against brute force, protects downstream services from amplification, and enforces fair usage across a shared API.

## 4. References

- [slowapi (FastAPI rate limiting)](https://github.com/laurentS/slowapi)
- [Redis rate limiting patterns](https://redis.io/docs/manual/patterns/rate-limiting/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Implement an in-memory sliding window rate limiter (5 req/10s per IP). Apply it as a dependency on `POST /login`.

### Intermediate Level

Add a `Retry-After` header to 429 responses indicating how many seconds until the limit resets.

### Advanced Level

Make the rate limiter configurable per route: some routes allow 100/min, others 5/min. Implement it as a parameterised dependency factory `rate_limit(max_calls=100, window=60)`.

### Success Criteria

- 6th request within 10 seconds returns 429.
- Response includes `Retry-After: N` seconds.
- Different routes enforce different limits independently.

## 6. Summary

Rate limiting is a necessary defence for any public-facing API. The sliding window algorithm is accurate and simple to implement in-memory. For distributed deployments, use Redis with `EXPIRE` or a purpose-built library like `slowapi`.

## 7. Reflection Prompt

Rate limiting by IP address can unfairly block many users behind a corporate NAT or CDN. What alternative rate limit keys would you use for authenticated vs. unauthenticated endpoints, and how would you handle the IP-behind-NAT problem?
