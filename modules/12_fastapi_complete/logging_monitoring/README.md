# Logging & Monitoring

Estimated time: 90 minutes

## 1. Definition

**Structured logging** emits log records as JSON objects rather than free-form strings, making them machine-parseable by log aggregators (ELK, Datadog, Splunk). **Monitoring** exposes operational metrics (request count, latency, error rate) via a `/metrics` endpoint for dashboards and alerting.

### Key Characteristics

- **JSON formatter**: custom `logging.Formatter` that serialises records as JSON lines.
- **Correlation ID**: a UUID assigned per request, propagated to every log line via `ContextVar`.
- **`extra={}`**: attach arbitrary structured fields to any log call.
- **Liveness probe (`/health`)**: returns 200 if the process is alive — used by K8s/ECS.
- **Readiness probe (`/ready`)**: returns 200 when the app is ready to serve — checks DB, cache.

## 2. Practical Application

### Use Cases

- Tracing a single failed request across 20 log lines by correlation ID.
- Alerting when error rate exceeds 1% over a 5-minute window.
- Debugging slow requests by filtering logs for `elapsed_ms > 500`.
- Kubernetes readiness probe preventing traffic to pods before DB connection is established.

### Code Example

```python
import logging, json
from contextvars import ContextVar

_cid: ContextVar[str] = ContextVar("cid", default="-")

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "ts": self.formatTime(record),
            "level": record.levelname,
            "msg": record.getMessage(),
            "cid": _cid.get(),
        })
```

## 3. Why Is It Important?

### Problem It Solves

Plain-text logs are difficult to query, filter, and aggregate at scale. Without correlation IDs, tracing a single request across multiple log entries requires grepping through time-sorted logs.

### Solution and Benefits

JSON logs are indexed and queryable by any log aggregator. Correlation IDs make a single request traceable across all log lines, middleware, and downstream service calls in milliseconds.

## 4. References

- [Python Logging](https://docs.python.org/3/library/logging.html)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [prometheus_fastapi_instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Replace the default logging format with a JSON formatter. Add `extra={"endpoint": "/items"}` to a log call and verify it appears in the JSON output.

### Intermediate Level

Create `CorrelationIdMiddleware` that reads `X-Correlation-ID` from the header (or generates a UUID), stores it in a `ContextVar`, and includes it in every log line via the formatter.

### Advanced Level

Add `/health` (liveness) and `/ready` (readiness) endpoints. Simulate a "not ready" state when a config flag is set. Add an in-memory `Metrics` class tracking `request_count`, `error_count`, and `avg_latency_ms`.

### Success Criteria

- Every log line is valid JSON with `ts`, `level`, `msg`, and `cid` fields.
- Correlation ID is consistent across all log lines for a single request.
- `/health` returns 200; `/ready` returns 503 when simulated DB check fails.

## 6. Summary

Structured JSON logging + correlation IDs are the minimum viable observability stack. `ContextVar` stores the correlation ID safely across async tasks. Health and readiness probes are required for orchestrated deployments. For production, add Prometheus metrics and OpenTelemetry tracing.

## 7. Reflection Prompt

There is a tension between logging detail and log volume cost. How would you decide what log level to use for different event types (incoming request, cache miss, DB query, validation error, unhandled exception)? What would you include in each level?
