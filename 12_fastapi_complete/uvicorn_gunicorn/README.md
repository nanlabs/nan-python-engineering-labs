# Uvicorn & Gunicorn

Estimated time: 90 minutes

## 1. Definition

**Uvicorn** is the ASGI server that runs FastAPI. **Gunicorn** is a production-grade process manager that spawns and supervises multiple Uvicorn worker processes, enabling multi-core utilisation.

### Key Characteristics

- **ASGI**: the async interface that Uvicorn implements; FastAPI speaks ASGI.
- **Uvicorn workers**: each is a single-threaded async event loop; one per process.
- **Gunicorn + UvicornWorker**: Gunicorn manages N Uvicorn processes, providing restarts, graceful shutdown, and worker recycling.
- **Worker count formula**: `(2 × CPU cores) + 1` for I/O-bound apps.
- **`--reload`**: development-only; never use in production.

## 2. Practical Application

### Use Cases

- Development: `uvicorn main:app --reload --host 127.0.0.1 --port 8000`.
- Production single server: `uvicorn main:app --workers 4`.
- Production with Gunicorn: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`.
- Docker/Kubernetes: single Uvicorn process per container, horizontal scaling via replicas.

### Code Example

```bash
# Development
uvicorn main:app --reload

# Production (Gunicorn + UvicornWorker)
gunicorn main:app   --workers 4   --worker-class uvicorn.workers.UvicornWorker   --bind 0.0.0.0:8000   --timeout 30   --preload
```

## 3. Why Is It Important?

### Problem It Solves

A single Uvicorn process uses one CPU core. On a 4-core server, 75% of CPU capacity is idle. Gunicorn distributes requests across multiple worker processes, utilising all cores.

### Solution and Benefits

Gunicorn adds process supervision: crashed workers are restarted automatically. `--preload` shares loaded application memory across workers via copy-on-write, reducing RAM. `graceful_timeout` drains in-flight requests before reload.

## 4. References

- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/server-workers/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Start your app with `uvicorn main:app --reload`. Access `/docs`. Stop it and restart with `--port 9000`. Verify the port change.

### Intermediate Level

Write a `gunicorn.conf.py` that sets workers to `cpu_count * 2 + 1`, binds to `0.0.0.0:8000`, sets `timeout=30`, and uses `UvicornWorker`.

### Advanced Level

Write a `Dockerfile` that runs Gunicorn with 4 workers and a health check. Use a multi-stage build to keep the image small.

### Success Criteria

- `gunicorn.conf.py` sets workers dynamically from `multiprocessing.cpu_count()`.
- Docker health check passes with `curl http://localhost:8000/health`.
- Image size is under 200 MB.

## 6. Summary

Uvicorn is the ASGI runtime; Gunicorn is the process supervisor. Together they enable multi-core production deployments. In containerised environments (Docker, Kubernetes), a single Uvicorn process per container is preferred — scaling is handled at the orchestration layer.

## 7. Reflection Prompt

When running in Kubernetes, should you use Gunicorn with multiple workers per pod, or a single Uvicorn process per pod scaled via HPA? What are the trade-offs for rolling updates, resource limits, and pod startup time?
