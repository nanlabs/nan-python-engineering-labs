"""
Basic example: Uvicorn & Gunicorn
=====================================

Uvicorn is the ASGI server that runs FastAPI. Gunicorn manages
multiple Uvicorn worker processes for production deployments.

Standalone runnable — demonstrates configuration and startup patterns.
No HTTP server is started; the script explains and demonstrates config.

Run:
    python example_basic.py

Production commands shown in output:
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
"""

import os
import multiprocessing
from fastapi import FastAPI


# =============================================================================
# THE APP (imported by uvicorn/gunicorn)
# =============================================================================

app = FastAPI(
    title="Uvicorn & Gunicorn Production App",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "worker_pid": os.getpid(),
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# =============================================================================
# UVICORN CONFIGURATION REFERENCE
# =============================================================================

UVICORN_CONFIG = {
    # ── Binding ──────────────────────────────────────────────────────────────
    "host": "0.0.0.0",           # Listen on all interfaces (0.0.0.0 for Docker)
    "port": 8000,                 # Default port
    "unix_socket": None,          # Or: "/tmp/app.sock" for nginx proxy

    # ── Workers ──────────────────────────────────────────────────────────────
    "workers": 1,                 # Use gunicorn for multi-worker instead
    "loop": "auto",               # asyncio (default) or uvloop (faster, install separately)
    "http": "auto",               # h11 (default) or httptools (slightly faster)

    # ── TLS (terminate at nginx in prod, or use here) ─────────────────────
    "ssl_keyfile": None,          # Path to key file
    "ssl_certfile": None,         # Path to cert file

    # ── Timeouts ─────────────────────────────────────────────────────────────
    "timeout_keep_alive": 5,      # Seconds to keep idle connections open
    "timeout_notify": 30,         # Time to wait for app startup

    # ── Logging ──────────────────────────────────────────────────────────────
    "log_level": "info",          # debug / info / warning / error / critical
    "access_log": True,           # Log every request
    "use_colors": True,           # Colorize console output

    # ── Reload (development only) ────────────────────────────────────────────
    "reload": False,              # Auto-reload on file change (dev only)
    "reload_dirs": None,          # Which dirs to watch
}


GUNICORN_CONFIG = {
    # ── Workers ──────────────────────────────────────────────────────────────
    "workers": 4,                 # Rule: (2 × CPU cores) + 1
    "worker_class": "uvicorn.workers.UvicornWorker",  # ASGI worker
    "threads": 1,                 # Threads per worker (UvicornWorker ignores this)

    # ── Binding ──────────────────────────────────────────────────────────────
    "bind": "0.0.0.0:8000",
    "backlog": 2048,              # Max pending connections in queue

    # ── Timeouts ─────────────────────────────────────────────────────────────
    "timeout": 30,                # Worker silent timeout (seconds)
    "graceful_timeout": 30,       # Time to finish in-flight requests on reload
    "keepalive": 2,               # Keep-alive connection timeout

    # ── Logging ──────────────────────────────────────────────────────────────
    "loglevel": "info",
    "accesslog": "-",             # "-" = stdout
    "errorlog": "-",              # "-" = stderr

    # ── Process management ──────────────────────────────────────────────────
    "preload_app": True,          # Load app before forking workers (saves RAM)
    "daemon": False,              # Never daemonize in Docker/Kubernetes
}


# =============================================================================
# RECOMMENDED COMMANDS
# =============================================================================

COMMANDS = {
    "development": (
        "uvicorn example_basic:app --reload --host 127.0.0.1 --port 8000"
    ),
    "production_uvicorn_only": (
        "uvicorn example_basic:app "
        "--host 0.0.0.0 --port 8000 "
        "--workers 4 "
        "--loop uvloop "
        "--log-level info"
    ),
    "production_gunicorn": (
        "gunicorn example_basic:app "
        "-w 4 "
        "-k uvicorn.workers.UvicornWorker "
        "--bind 0.0.0.0:8000 "
        "--timeout 30 "
        "--preload "
        "--log-level info"
    ),
    "gunicorn_config_file": (
        "gunicorn example_basic:app -c gunicorn.conf.py"
    ),
}


GUNICORN_CONF_PY = """\
# gunicorn.conf.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
timeout = 30
graceful_timeout = 30
keepalive = 2
preload_app = True
loglevel = "info"
accesslog = "-"
errorlog = "-"
"""


DOCKERFILE_SNIPPET = """\
# Dockerfile (production)
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run with gunicorn (multi-worker) + uvicorn workers
CMD ["gunicorn", "main:app",
     "-w", "4",
     "-k", "uvicorn.workers.UvicornWorker",
     "--bind", "0.0.0.0:8000",
     "--timeout", "30",
     "--preload"]
"""


# =============================================================================
# PROGRAMMATIC UVICORN STARTUP (alternative to CLI)
# =============================================================================


def programmatic_start():
    """
    Start uvicorn from Python code — useful for testing or custom launchers.

    uvicorn.run() is equivalent to the CLI command.
    """
    import uvicorn  # type: ignore
    uvicorn.run(
        "example_basic:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )


# =============================================================================
# MAIN
# =============================================================================


def main():
    cpu_count = multiprocessing.cpu_count()
    recommended_workers = cpu_count * 2 + 1

    print("=" * 65)
    print("UVICORN & GUNICORN — DEMO")
    print("=" * 65)
    print()
    print(f"System CPU count:        {cpu_count}")
    print(f"Recommended workers:     {recommended_workers}  (2×CPUs + 1)")
    print()

    print("─" * 65)
    print("UVICORN CONFIGURATION (key options)")
    print("─" * 65)
    for k, v in UVICORN_CONFIG.items():
        print(f"  {k:<30} = {v!r}")

    print()
    print("─" * 65)
    print("GUNICORN CONFIGURATION (key options)")
    print("─" * 65)
    for k, v in GUNICORN_CONFIG.items():
        print(f"  {k:<30} = {v!r}")

    print()
    print("─" * 65)
    print("RECOMMENDED COMMANDS")
    print("─" * 65)
    for env, cmd in COMMANDS.items():
        print(f"\n  [{env}]")
        print(f"  {cmd}")

    print()
    print("─" * 65)
    print("gunicorn.conf.py")
    print("─" * 65)
    print(GUNICORN_CONF_PY)

    print("─" * 65)
    print("Dockerfile (production snippet)")
    print("─" * 65)
    print(DOCKERFILE_SNIPPET)

    print("─" * 65)
    print("When to use what:")
    print("─" * 65)
    choices = [
        ("Development",   "uvicorn --reload"),
        ("Single server", "uvicorn --workers N"),
        ("Production",    "gunicorn -k UvicornWorker (process supervisor)"),
        ("Kubernetes",    "Single uvicorn process per pod (HPA handles scaling)"),
        ("Docker Compose","gunicorn with 2-4 workers per container"),
    ]
    for scenario, choice in choices:
        print(f"  {scenario:<18} → {choice}")
    print()


if __name__ == "__main__":
    main()
