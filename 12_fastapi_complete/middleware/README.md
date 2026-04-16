# Middleware

Estimated time: 90 minutes

## 1. Definition

**Middleware** is code that wraps every request and response in your FastAPI application. It runs before the request reaches any route handler and after the route returns a response, giving you a cross-cutting hook for logging, timing, header injection, and request transformation.

### Key Characteristics

- **`BaseHTTPMiddleware`**: Starlette base class for function-style middleware.
- **`dispatch(request, call_next)`**: receives the request, optionally modifies it, calls `call_next`, then processes the response.
- **Execution order**: last `add_middleware()` call runs first on the request (LIFO).
- **`@app.middleware("http")`**: alternative decorator-style registration.
- **Scope**: middleware sees every request, including static files and docs — unlike route dependencies.

## 2. Practical Application

### Use Cases

- Adding `X-Process-Time-Ms` header to every response.
- Assigning a correlation ID to every request for log tracing.
- Enforcing security headers (`X-Content-Type-Options`, `Strict-Transport-Security`).
- Logging request/response pairs with timing.

### Code Example

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed:.2f}"
        return response

app = FastAPI()
app.add_middleware(TimingMiddleware)
```

## 3. Why Is It Important?

### Problem It Solves

Without middleware, cross-cutting concerns (logging, timing, security headers) must be duplicated in every route handler or added as a dependency to every router. Any omission creates inconsistency.

### Solution and Benefits

Middleware guarantees that the concern applies to every request unconditionally — no per-route boilerplate. A single middleware change propagates across the entire application.

## 4. References

- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Starlette Middleware](https://www.starlette.io/middleware/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `TimingMiddleware` that adds `X-Process-Time-Ms` to every response. Verify it appears in curl output.

### Intermediate Level

Create a `CorrelationIdMiddleware` that reads `X-Correlation-ID` from the request header (or generates a UUID if absent), stores it in `request.state`, and echoes it in the response.

### Advanced Level

Create a `SecurityHeadersMiddleware` that adds all OWASP-recommended headers. Combine it with the timing and correlation ID middlewares. Verify that order matters and document why.

### Success Criteria

- Every response includes `X-Process-Time-Ms`.
- Providing `X-Correlation-ID: my-id-001` echoes the same value in the response.
- Security headers are present on all responses including `/docs`.

## 6. Summary

Middleware intercepts every request and response at the ASGI level. `BaseHTTPMiddleware` provides a clean `dispatch` interface. Stacking multiple middlewares in the correct order is essential — registration order determines execution order (LIFO for requests).

## 7. Reflection Prompt

Why is middleware the right place for security headers, but not the right place for business logic like authentication? What is the architectural distinction between middleware and a dependency?
