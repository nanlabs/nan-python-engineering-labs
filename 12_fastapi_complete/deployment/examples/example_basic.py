"""
Basic example: Deployment
============================

This standalone script demonstrates the configuration and tooling
patterns for deploying a FastAPI application to production.

Demonstrates:
1. pydantic-settings — environment-based configuration with validation
2. Environment profiles (development / staging / production)
3. Docker configuration patterns (Dockerfile + docker-compose)
4. Graceful shutdown hooks (lifespan)
5. Health and readiness probes for orchestrators

Dependencies:
    pip install pydantic-settings fastapi uvicorn

Run:
    python example_basic.py      ← configuration demo
    uvicorn example_basic:app --reload  ← development server
"""

import os
from contextlib import asynccontextmanager
from enum import Enum

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# =============================================================================
# 1. SETTINGS — pydantic-settings reads from env vars or .env file
# =============================================================================


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Variable names are uppercased automatically:
        APP_NAME → app_name
        DATABASE_URL → database_url

    Load from a .env file: model_config = SettingsConfigDict(env_file=".env")
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ─────────────────────────────────────────────────────────
    app_name: str = "FastAPI Production App"
    app_version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False

    # ── Server ───────────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = "sqlite:///./app.db"
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # ── Security ─────────────────────────────────────────────────────────────
    secret_key: SecretStr = SecretStr("dev-secret-change-in-production")
    allowed_hosts: list[str] = ["*"]
    cors_origins: list[str] = ["http://localhost:3000"]

    # ── External Services ─────────────────────────────────────────────────────
    redis_url: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587

    @field_validator("secret_key")
    @classmethod
    def secret_must_be_strong(cls, v: SecretStr) -> SecretStr:
        value = v.get_secret_value()
        if value.startswith("dev-") and os.environ.get("ENVIRONMENT") == "production":
            raise ValueError("Cannot use a dev secret key in production")
        return v

    @field_validator("workers")
    @classmethod
    def workers_range(cls, v: int) -> int:
        if not 1 <= v <= 32:
            raise ValueError("workers must be between 1 and 32")
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT


# Singleton — load once at startup
settings = Settings()


# =============================================================================
# 2. DOCKER CONFIGURATION TEMPLATES
# =============================================================================

DOCKERFILE = """\
# ── Stage 1: dependencies ────────────────────────────────────────────────────
FROM python:3.12-slim AS deps

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Create non-root user (security best practice)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from deps stage
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appgroup . .

USER appuser

# Health check (Docker will mark the container unhealthy if this fails)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# Production: gunicorn with uvicorn workers
CMD ["gunicorn", "main:app",
     "--worker-class", "uvicorn.workers.UvicornWorker",
     "--workers", "4",
     "--bind", "0.0.0.0:8000",
     "--timeout", "30",
     "--preload",
     "--log-level", "info"]
"""

DOCKER_COMPOSE = """\
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379/0
      - SECRET_KEY=${SECRET_KEY}          # from .env or CI secret
      - WORKERS=4
      - LOG_LEVEL=info
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    command: redis-server --save 60 1 --loglevel warning
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
"""

ENV_FILE_TEMPLATE = """\
# .env.production (do NOT commit — use secrets manager in CI/CD)
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info

DATABASE_URL=postgresql+asyncpg://user:strongpass@db:5432/mydb
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

SECRET_KEY=use-a-strong-random-key-here-min-32-chars
ALLOWED_HOSTS=["api.example.com"]
CORS_ORIGINS=["https://app.example.com"]

REDIS_URL=redis://cache:6379/0
"""


# =============================================================================
# 3. FASTAPI APP WITH LIFESPAN (startup/shutdown hooks)
# =============================================================================


@asynccontextmanager
async def lifespan(app):
    """
    Lifespan context manager replaces @on_event("startup") / @on_event("shutdown").

    Code BEFORE yield → runs at startup.
    Code AFTER yield  → runs at shutdown (after all requests complete).
    """
    # ── Startup ───────────────────────────────────────────────────────────────
    print(f"[startup] App: {settings.app_name} v{settings.app_version}")
    print(f"[startup] Environment: {settings.environment.value}")
    print(f"[startup] Database: {settings.database_url[:40]}...")
    print(f"[startup] Debug: {settings.debug}")

    # In production: initialize DB connection pool, Redis, etc.
    # await db.connect()
    # await cache.connect()

    yield  # ← Application is running here

    # ── Shutdown ──────────────────────────────────────────────────────────────
    print("[shutdown] Closing connections...")
    # await db.disconnect()
    # await cache.close()
    print("[shutdown] Graceful shutdown complete")


from fastapi import FastAPI

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.is_development,
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,  # hide docs in prod
    redoc_url="/redoc" if settings.is_development else None,
)


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
    }


@app.get("/health")
async def health():
    """Liveness probe — K8s/ECS check if the process is alive."""
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    """
    Readiness probe — K8s check if the pod should receive traffic.

    In production, check DB and cache connectivity here.
    """
    checks = {
        "database": "ok",  # replace with actual ping
        "cache": "ok" if settings.redis_url else "not configured",
    }
    all_ok = all(v == "ok" or v == "not configured" for v in checks.values())
    return {"status": "ready" if all_ok else "not_ready", "checks": checks}


@app.get("/config")
async def show_config():
    """Show non-sensitive config — never expose secrets."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment.value,
        "workers": settings.workers,
        "log_level": settings.log_level,
        "debug": settings.debug,
        "cors_origins": settings.cors_origins,
        # secret_key is NOT included
    }


# =============================================================================
# 4. MAIN
# =============================================================================


def main():
    """Entry point to demonstrate the implementation."""
    print("=" * 65)
    print("DEPLOYMENT — DEMO")
    print("=" * 65)
    print()
    print("Loaded settings:")
    print(f"  app_name:    {settings.app_name}")
    print(f"  version:     {settings.app_version}")
    print(f"  environment: {settings.environment.value}")
    print(f"  host:        {settings.host}:{settings.port}")
    print(f"  workers:     {settings.workers}")
    print(f"  debug:       {settings.debug}")
    print(f"  database:    {settings.database_url[:30]}...")
    print(f"  redis:       {settings.redis_url or 'not configured'}")
    print()
    print("─" * 65)
    print("Dockerfile (multi-stage, non-root user):")
    print("─" * 65)
    print(DOCKERFILE[:600], "  [... truncated]")
    print()
    print("─" * 65)
    print("docker-compose.yml key highlights:")
    print("─" * 65)
    print("  api: gunicorn, 4 workers, depends_on db+cache health checks")
    print("  db:  PostgreSQL 16, health check, named volume")
    print("  cache: Redis 7, health check")
    print()
    print("─" * 65)
    print(".env.production template (never commit):")
    print("─" * 65)
    print(ENV_FILE_TEMPLATE)
    print()
    print("─" * 65)
    print("Deployment checklist:")
    print("─" * 65)
    checklist = [
        "SECRET_KEY is strong and loaded from secrets manager",
        "DEBUG=false in production",
        "DOCS disabled in production (docs_url=None)",
        "HTTPS terminated at load balancer or nginx",
        "Database connection pooling configured",
        "Health + readiness probes configured",
        "Non-root Docker user",
        "Multi-stage Docker build (smaller image)",
        "Graceful shutdown with lifespan()",
        "Structured JSON logging",
        "Rate limiting enabled",
        "CORS restricted to known origins",
    ]
    for item in checklist:
        print(f"  [ ] {item}")
    print()
    print("Start (dev): uvicorn example_basic:app --reload")
    print("Start (prod): gunicorn example_basic:app -w 4 -k uvicorn.workers.UvicornWorker")
    print("=" * 65)


if __name__ == "__main__":
    main()
