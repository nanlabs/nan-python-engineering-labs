"""
Basic example: Rate Limiting
================================

Rate limiting protects your API from abuse, DoS attacks, and runaway
clients by enforcing a maximum number of requests per time window.

This example demonstrates:
1. Fixed-window rate limiter (in-memory, per IP)
2. Sliding-window rate limiter (more accurate)
3. Per-route limits via FastAPI dependencies
4. Rate limit headers (X-RateLimit-*)
5. 429 Too Many Requests with Retry-After

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

Stress test:
    for i in $(seq 1 15); do
        curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/limited
    done
"""

import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import Depends, FastAPI, HTTPException, Request, status

# =============================================================================
# 1. FIXED-WINDOW RATE LIMITER
# =============================================================================


class FixedWindowLimiter:
    """
    Fixed-window rate limiter.

    Counts requests in a fixed time window (e.g., 0–60s, 60–120s, …).
    Simpler but can allow 2× burst at window boundaries.
    """

    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self._counts: dict[str, int] = defaultdict(int)
        self._window_start: dict[str, float] = {}
        self._lock = Lock()

    def check(self, key: str) -> tuple[bool, int, float]:
        """
        Returns: (allowed, remaining, retry_after_seconds)
        """
        now = time.time()
        with self._lock:
            win_start = self._window_start.get(key, 0)
            if now - win_start >= self.window:
                self._counts[key] = 0
                self._window_start[key] = now

            count = self._counts[key]
            if count >= self.max_requests:
                retry_after = self.window - (now - win_start)
                return False, 0, max(retry_after, 0)

            self._counts[key] += 1
            remaining = self.max_requests - self._counts[key]
            return True, remaining, 0.0


# =============================================================================
# 2. SLIDING-WINDOW RATE LIMITER
# =============================================================================


class SlidingWindowLimiter:
    """
    Sliding-window rate limiter.

    Tracks the actual timestamps of requests, so the window always
    covers the last N seconds — no boundary burst effect.
    """

    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self._timestamps: dict[str, deque] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> tuple[bool, int, float]:
        now = time.time()
        cutoff = now - self.window
        with self._lock:
            dq = self._timestamps[key]
            # Remove timestamps outside the window
            while dq and dq[0] < cutoff:
                dq.popleft()

            count = len(dq)
            if count >= self.max_requests:
                oldest = dq[0]
                retry_after = self.window - (now - oldest)
                return False, 0, max(retry_after, 0)

            dq.append(now)
            remaining = self.max_requests - len(dq)
            return True, remaining, 0.0


# =============================================================================
# LIMITER INSTANCES
# =============================================================================

# Public endpoints: 10 req/min per IP
public_limiter = SlidingWindowLimiter(max_requests=10, window_seconds=60.0)

# Sensitive endpoints: 3 req/min per IP (e.g., login, password reset)
sensitive_limiter = FixedWindowLimiter(max_requests=3, window_seconds=60.0)

# Expensive endpoints: 5 req/10s per IP
expensive_limiter = SlidingWindowLimiter(max_requests=5, window_seconds=10.0)


# =============================================================================
# RATE LIMIT DEPENDENCY
# =============================================================================


def get_client_ip(request: Request) -> str:
    """Extract client IP from X-Forwarded-For or direct connection."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(limiter: SlidingWindowLimiter | FixedWindowLimiter):
    """
    Factory that returns a FastAPI dependency for a given limiter.

    Usage:
        @app.get("/route", dependencies=[Depends(rate_limit(public_limiter))])
    """

    async def _check(request: Request):
        ip = get_client_ip(request)
        allowed, remaining, retry_after = limiter.check(ip)

        # Always set rate limit info headers
        request.state.ratelimit_remaining = remaining

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Please slow down.",
                    "retry_after_seconds": round(retry_after, 1),
                },
                headers={"Retry-After": str(int(retry_after) + 1)},
            )

    return _check


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Rate Limiting Example", version="1.0.0")


@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Add X-RateLimit-Remaining to every response that goes through a limiter."""
    response = await call_next(request)
    remaining = getattr(request.state, "ratelimit_remaining", None)
    if remaining is not None:
        response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response


@app.get("/")
async def root():
    return {"message": "Rate Limiting Demo", "docs": "/docs"}


@app.get(
    "/api/public",
    dependencies=[Depends(rate_limit(public_limiter))],
    summary="Public endpoint — 10 req/min per IP",
)
async def public_endpoint(request: Request):
    """
    10 requests per minute per IP.

    Check X-RateLimit-Remaining in the response headers.
    On the 11th request within 60s you get 429.
    """
    ip = get_client_ip(request)
    return {
        "data": "Public resource",
        "your_ip": ip,
        "limit": "10 req/60s",
    }


@app.post(
    "/auth/login",
    dependencies=[Depends(rate_limit(sensitive_limiter))],
    summary="Login — 3 attempts/min per IP (brute force protection)",
)
async def login(request: Request):
    """Only 3 login attempts per minute — prevents brute force."""
    return {"token": "demo-token", "limit": "3 req/60s"}


@app.get(
    "/api/expensive",
    dependencies=[Depends(rate_limit(expensive_limiter))],
    summary="Expensive computation — 5 req/10s per IP",
)
async def expensive_operation():
    """
    Expensive endpoint — 5 requests per 10 seconds.

    Quickly trigger the rate limit:
        for i in {1..8}; do curl -s http://localhost:8000/api/expensive | jq .request; done
    """
    import time as t

    t.sleep(0.05)  # Simulate work
    return {"result": "computed", "limit": "5 req/10s"}


@app.get("/rate-limit/status")
async def rate_limit_status(request: Request):
    """Show rate limit windows for the current IP."""
    ip = get_client_ip(request)
    _, pub_remaining, _ = public_limiter.check(ip)
    _, sens_remaining, _ = sensitive_limiter.check(ip)
    _, exp_remaining, _ = expensive_limiter.check(ip)
    # Undo the counts we just added
    return {
        "your_ip": ip,
        "limits": {
            "public": {"max": 10, "window": "60s", "remaining": pub_remaining},
            "sensitive": {"max": 3, "window": "60s", "remaining": sens_remaining},
            "expensive": {"max": 5, "window": "10s", "remaining": exp_remaining},
        },
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("RATE LIMITING — DEMO")
    print("=" * 65)
    print()
    print("Strategies:")
    print("  FixedWindowLimiter  — simple, allows boundary bursts")
    print("  SlidingWindowLimiter — accurate, no boundary burst")
    print()
    print("Rate limit headers returned:")
    print("  X-RateLimit-Remaining: 7")
    print("  Retry-After: 15  (only on 429)")
    print()
    print("Endpoints:")
    print("  GET  /api/public      — 10 req/60s per IP")
    print("  POST /auth/login      — 3 req/60s per IP")
    print("  GET  /api/expensive   — 5 req/10s per IP")
    print("  GET  /rate-limit/status — check your current counts")
    print()
    print("Stress test:")
    print("  for i in $(seq 1 12); do")
    print('      curl -s -w "%{http_code}\\n" -o /dev/null \\')
    print("           http://localhost:8000/api/public; done")
    print()
    print("Production note:")
    print("  Use Redis + lua scripts for distributed rate limiting")
    print("  (this example uses in-memory storage — single process only)")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
