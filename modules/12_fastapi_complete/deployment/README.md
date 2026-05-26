# Deployment

Estimated time: 2 hours

## 1. Definition

**Deployment** is the process of packaging, configuring, and running a FastAPI application in a production environment. It encompasses environment-based configuration, process management, container packaging, health probes, and graceful shutdown.

### Key Characteristics

- **`pydantic-settings`**: loads configuration from environment variables with type validation.
- **`lifespan` context manager**: replaces `@on_event` for startup/shutdown hooks.
- **Multi-stage Docker build**: separate build and runtime stages for smaller images.
- **Non-root Docker user**: security best practice — never run as root in containers.
- **Health + readiness probes**: liveness (is the process alive?) and readiness (is it ready for traffic?).

## 2. Practical Application

### Use Cases

- Loading `DATABASE_URL`, `SECRET_KEY`, and `WORKERS` from environment variables validated by Pydantic.
- Docker Compose for local development with separate DB and Redis services.
- Kubernetes deployment with health probes and HPA for auto-scaling.
- Graceful shutdown: draining in-flight requests before closing DB connections.

### Code Example

```python
from pydantic_settings import BaseSettings
from contextlib import asynccontextmanager
from fastapi import FastAPI

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    workers: int = 4

settings = Settings()

@asynccontextmanager
async def lifespan(app):
    # startup
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)
```

## 3. Why Is It Important?

### Problem It Solves

Hardcoded secrets, missing startup/shutdown logic, and single-process deployments are the most common production failures. Configuration in source code prevents environment-specific overrides.

### Solution and Benefits

`pydantic-settings` validates the environment at startup — the app fails fast with a clear error if `SECRET_KEY` is missing. Lifespan hooks ensure the DB pool is properly closed on shutdown. Multi-stage Docker builds produce minimal, secure images.

## 4. References

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Twelve-Factor App](https://12factor.net/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `Settings` class with `pydantic-settings` for `app_name`, `debug`, `port`, and `database_url`. Verify it loads from environment variables.

### Intermediate Level

Add a `lifespan` function that prints startup/shutdown messages and simulate DB connection setup. Verify shutdown runs after all requests complete.

### Advanced Level

Write a multi-stage `Dockerfile` with a non-root user and a health check. Write a `docker-compose.yml` with the API, a PostgreSQL service, and a Redis service, all with health checks.

### Success Criteria

- App fails to start if `SECRET_KEY` is not set (in production environment).
- Shutdown log message appears after all responses are sent.
- Docker health check passes: `curl http://localhost:8000/health` returns 200.
- `docker compose up` brings up API + DB + Redis.

## 6. Summary

Production deployment requires configuration from environment (`pydantic-settings`), graceful lifecycle management (`lifespan`), containerisation with a non-root user and health check, and a process supervisor (Gunicorn or Kubernetes). Each piece addresses a different operational risk.

## 7. Reflection Prompt

The Twelve-Factor App methodology says "store config in the environment." However, secrets management systems (Vault, AWS Secrets Manager) inject secrets differently. How would you integrate `pydantic-settings` with a secrets manager while keeping the app portable across environments?
