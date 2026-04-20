"""
Basic example: Middleware
===========================

FastAPI (Starlette) middleware intercepts every request before it reaches
route handlers and every response before it reaches the client.

This example demonstrates:
1. Request timing middleware
2. Request ID / correlation ID middleware
3. Request logging middleware
4. Custom security header middleware
5. Combining multiple middlewares

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

import logging
import time
import uuid
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# =============================================================================
# LOGGING SETUP
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("api")


# =============================================================================
# 1. TIMING MIDDLEWARE
# =============================================================================


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Adds X-Process-Time header to every response.

    Measures time from request arrival to response dispatch.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
        return response


# =============================================================================
# 2. CORRELATION ID MIDDLEWARE
# =============================================================================


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Assigns a unique correlation ID to every request.

    - Reads `X-Correlation-ID` from the incoming request if provided.
    - Generates a new UUID if the header is absent.
    - Echoes the ID back in the response header.
    - Makes the ID available via request.state.correlation_id.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4())[:8])
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


# =============================================================================
# 3. REQUEST LOGGING MIDDLEWARE
# =============================================================================


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming request and the corresponding response status.

    Log format:
        IN  | GET /items | correlation_id=abc123
        OUT | 200 OK     | GET /items | 12.34ms
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = getattr(request.state, "correlation_id", "-")
        logger.info(
            "IN  | %s %s | cid=%s | client=%s",
            request.method,
            request.url.path,
            correlation_id,
            request.client.host if request.client else "unknown",
        )
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "OUT | %s | %s %s | %.2fms | cid=%s",
            response.status_code,
            request.method,
            request.url.path,
            elapsed_ms,
            correlation_id,
        )
        return response


# =============================================================================
# 4. SECURITY HEADERS MIDDLEWARE
# =============================================================================


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds security-related HTTP headers to every response.

    These headers harden the API against common web vulnerabilities.
    """

    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Cache-Control": "no-store",
    }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        for header, value in self.SECURITY_HEADERS.items():
            response.headers[header] = value
        return response


# =============================================================================
# APP — MIDDLEWARE REGISTRATION ORDER MATTERS
# =============================================================================

# Middlewares are applied in LIFO (last added = first to run on request).
# Registration order: SecurityHeaders → Logging → CorrelationId → Timing
# Execution order on request:  Timing → CorrelationId → Logging → SecurityHeaders

app = FastAPI(title="Middleware Example", version="1.0.0")

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(TimingMiddleware)


# =============================================================================
# ROUTES
# =============================================================================


@app.get("/")
async def root(request: Request):
    return {
        "message": "Middleware Demo",
        "correlation_id": getattr(request.state, "correlation_id", None),
        "docs": "/docs",
    }


@app.get("/items")
async def list_items(request: Request):
    """Simulate a slow endpoint to see timing in action."""
    time.sleep(0.05)  # 50ms simulated DB query
    return {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 6)],
        "correlation_id": getattr(request.state, "correlation_id", None),
    }


@app.get("/headers")
async def inspect_headers(request: Request):
    """Return all request headers — useful for debugging middleware."""
    return {
        "request_headers": dict(request.headers),
        "correlation_id": getattr(request.state, "correlation_id", None),
    }


@app.get("/slow")
async def slow_endpoint():
    """Artificially slow endpoint to demonstrate timing middleware."""
    time.sleep(0.2)
    return {"message": "That was slow!", "hint": "Check X-Process-Time-Ms header"}


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("MIDDLEWARE — DEMO")
    print("=" * 65)
    print()
    print("Registered middleware (execution order on each request):")
    print("  1. TimingMiddleware       → X-Process-Time-Ms header")
    print("  2. CorrelationIdMiddleware → X-Correlation-ID header")
    print("  3. RequestLoggingMiddleware → console logs IN/OUT")
    print("  4. SecurityHeadersMiddleware → security headers")
    print()
    print("After any request, response headers include:")
    print("  X-Process-Time-Ms: 12.34")
    print("  X-Correlation-ID: abc12345")
    print("  X-Content-Type-Options: nosniff")
    print("  X-Frame-Options: DENY")
    print("  Strict-Transport-Security: max-age=31536000; ...")
    print()
    print("Test with curl:")
    print('  curl -v "http://localhost:8000/slow"')
    print('  curl -H "X-Correlation-ID: myid-001" "http://localhost:8000/"')
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
