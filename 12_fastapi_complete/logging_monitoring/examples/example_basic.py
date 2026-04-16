"""
Basic example: Logging & Monitoring
=========================================

Production APIs need structured logging (JSON) and monitoring hooks.
This standalone example demonstrates patterns you can adopt without
any external monitoring infrastructure.

Demonstrates:
1. Structured JSON logging with stdlib logging
2. Correlation ID propagation across log entries
3. Request/response logging middleware
4. Custom log filters
5. Health/metrics endpoint for monitoring probes

Run:
    python example_basic.py       ← structured logging demo
    uvicorn example_basic:app --reload  ← full API with log middleware
"""

import json
import logging
import time
import uuid
from contextvars import ContextVar
from datetime import datetime
from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel


# =============================================================================
# 1. CORRELATION ID — thread/async context variable
# =============================================================================

# ContextVar stores the correlation ID per async task (request)
_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="no-cid")


def get_correlation_id() -> str:
    return _correlation_id.get()


def set_correlation_id(cid: str) -> None:
    _correlation_id.set(cid)


# =============================================================================
# 2. STRUCTURED JSON LOG FORMATTER
# =============================================================================


class JSONFormatter(logging.Formatter):
    """
    Formats log records as JSON lines — structured and machine-readable.

    Output example:
    {"ts": "2024-01-15T10:30:00.123", "level": "INFO", "msg": "Request received",
     "logger": "api.requests", "cid": "abc12345", "path": "/items"}
    """

    def format(self, record: logging.LogRecord) -> str:
        data = {
            "ts": datetime.fromtimestamp(record.created).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "cid": get_correlation_id(),
        }

        # Include extra fields passed via extra={} in the logging call
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in (
                "args", "created", "exc_info", "exc_text", "filename",
                "funcName", "levelname", "levelno", "lineno", "message",
                "module", "msecs", "msg", "name", "pathname",
                "process", "processName", "relativeCreated",
                "stack_info", "thread", "threadName",
            ):
                continue
            if key not in ("asctime",):
                data[key] = value

        if record.exc_info:
            data["exc"] = self.formatException(record.exc_info)

        return json.dumps(data, default=str)


def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with JSON output."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)

    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


setup_logging()
logger = logging.getLogger("api")
request_logger = logging.getLogger("api.requests")
error_logger = logging.getLogger("api.errors")


# =============================================================================
# 3. REQUEST / RESPONSE LOGGING MIDDLEWARE
# =============================================================================


class LoggingMiddleware:
    """
    Logs every request and response as structured JSON.

    Each log line includes the correlation ID so you can trace
    a single request across multiple log entries.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        # Set correlation ID from header or generate one
        cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4())[:8])
        set_correlation_id(cid)

        start = time.perf_counter()
        status_code = 500

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                # Inject correlation ID into response headers
                headers = dict(message.get("headers", []))
                headers[b"x-correlation-id"] = cid.encode()
                message = {**message, "headers": list(headers.items())}
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            request_logger.info(
                "%s %s → %s",
                request.method,
                request.url.path,
                status_code,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status": status_code,
                    "elapsed_ms": round(elapsed_ms, 2),
                    "client": request.client.host if request.client else "unknown",
                },
            )


# =============================================================================
# 4. IN-MEMORY METRICS
# =============================================================================


class Metrics:
    """Simple in-memory counters for a /metrics health endpoint."""

    def __init__(self):
        self.request_count: int = 0
        self.error_count: int = 0
        self.start_time: float = time.time()
        self._latencies: list[float] = []

    def record_request(self, status_code: int, latency_ms: float):
        self.request_count += 1
        if status_code >= 500:
            self.error_count += 1
        self._latencies.append(latency_ms)
        if len(self._latencies) > 1000:
            self._latencies = self._latencies[-1000:]

    @property
    def uptime_seconds(self) -> float:
        return round(time.time() - self.start_time, 1)

    @property
    def avg_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return round(sum(self._latencies) / len(self._latencies), 2)

    @property
    def p95_latency_ms(self) -> float:
        if not self._latencies:
            return 0.0
        sorted_lat = sorted(self._latencies)
        idx = int(len(sorted_lat) * 0.95)
        return round(sorted_lat[idx], 2)


metrics = Metrics()

# =============================================================================
# 5. APP
# =============================================================================

app = FastAPI(title="Logging & Monitoring Example", version="1.0.0")
app.add_middleware(LoggingMiddleware)


@app.middleware("http")
async def track_metrics(request: Request, call_next: Callable) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    metrics.record_request(response.status_code, elapsed_ms)
    return response


@app.get("/")
async def root():
    logger.info("Root endpoint accessed", extra={"endpoint": "root"})
    return {"message": "Logging & Monitoring Demo", "docs": "/docs"}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id > 100:
        error_logger.error(
            "Item not found",
            extra={"item_id": item_id, "reason": "id_out_of_range"},
        )
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    logger.info("Item fetched", extra={"item_id": item_id})
    return {"id": item_id, "name": f"Item {item_id}"}


@app.get("/health")
async def health():
    """Liveness probe — returns 200 if the service is running."""
    return {"status": "healthy", "uptime_seconds": metrics.uptime_seconds}


@app.get("/ready")
async def ready():
    """Readiness probe — returns 200 when the service is ready to serve traffic."""
    return {"status": "ready"}


@app.get("/metrics")
async def get_metrics():
    """Expose operational metrics for monitoring dashboards."""
    return {
        "uptime_seconds": metrics.uptime_seconds,
        "request_count": metrics.request_count,
        "error_count": metrics.error_count,
        "error_rate": (
            round(metrics.error_count / metrics.request_count, 4)
            if metrics.request_count else 0
        ),
        "avg_latency_ms": metrics.avg_latency_ms,
        "p95_latency_ms": metrics.p95_latency_ms,
    }


# =============================================================================
# 6. STANDALONE DEMO
# =============================================================================


def demo():
    print("=" * 65)
    print("LOGGING & MONITORING — DEMO")
    print("=" * 65)
    print()
    print("Structured JSON log output:")
    print()
    logger.info("Application started", extra={"version": "1.0.0", "env": "demo"})
    logger.warning("High memory usage", extra={"used_mb": 450, "limit_mb": 512})
    logger.error("DB connection failed", extra={"host": "db:5432", "retries": 3})

    print()
    print("Key patterns:")
    print("  ContextVar      — correlation ID per async request (no thread issues)")
    print("  JSONFormatter   — machine-readable, parseable by Datadog/Splunk/ELK")
    print("  extra={}        — attach structured fields to any log call")
    print("  /health         — liveness probe (K8s, ECS)")
    print("  /ready          — readiness probe (wait for DB/cache before serving)")
    print("  /metrics        — internal counters (latency, error rate)")
    print()
    print("For production monitoring:")
    print("  - Export metrics to Prometheus (prometheus_fastapi_instrumentator)")
    print("  - Ship logs to ELK or Datadog via log shipping agent")
    print("  - Trace requests with OpenTelemetry")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
