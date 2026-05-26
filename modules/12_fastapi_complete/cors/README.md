# CORS (Cross-Origin Resource Sharing)

Estimated time: 60 minutes

## 1. Definition

**CORS** is a browser security policy that blocks JavaScript running on one origin (domain + port + protocol) from making requests to a different origin, unless the server explicitly allows it via CORS headers. FastAPI uses Starlette's `CORSMiddleware` to configure these permissions.

### Key Characteristics

- **Same-origin policy**: browsers block cross-origin requests by default.
- **Preflight**: browsers send an `OPTIONS` request before any cross-origin `POST`/`PUT`/`DELETE` to check permissions.
- **`allow_origins`**: list of allowed origins, or `["*"]` for all.
- **`allow_credentials`**: permits cookies and `Authorization` headers — cannot be combined with `allow_origins=["*"]`.
- **`max_age`**: how long browsers cache preflight results (reduces `OPTIONS` traffic).

## 2. Practical Application

### Use Cases

- React/Vue/Angular frontend on `localhost:3000` talking to an API on `localhost:8000`.
- Production frontend on `https://app.example.com` calling `https://api.example.com`.
- Public read-only API that needs to work from any browser origin.
- Authenticated API that needs cookies or Authorization headers from specific origins.

### Code Example

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "http://localhost:3000"\],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## 3. Why Is It Important?

### Problem It Solves

Without CORS configuration, your browser-based frontend cannot call your API on a different port or domain. The browser silently blocks the request before it even reaches the server.

### Solution and Benefits

`CORSMiddleware` handles the `OPTIONS` preflight and adds the correct `Access-Control-*` headers automatically. A strict origin allowlist ensures that only your frontend (not arbitrary third-party sites) can make credentialed requests.

## 4. References

- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Add `CORSMiddleware` to allow `http://localhost:3000`. Test with curl: `curl -H "Origin: http://localhost:3000" http://localhost:8000/` and verify `Access-Control-Allow-Origin` is in the response.

### Intermediate Level

Switch to `allow_credentials=True` with an explicit origin list. Verify that a request from a non-listed origin does not get the CORS header.

### Advanced Level

Set `max_age=600` and `expose_headers=["X-Request-ID"]`. Test preflight caching: send two consecutive `OPTIONS` requests and observe browser behaviour.

### Success Criteria

- Allowed origins receive `Access-Control-Allow-Origin` in the response.
- Disallowed origins do not receive the header.
- `allow_origins=["*"]` + `allow_credentials=True` raises a runtime error.

## 6. Summary

`CORSMiddleware` manages browser cross-origin permissions. The key constraint is that `allow_origins=["*"]` and `allow_credentials=True` cannot be combined — always use an explicit origin list in production. `max_age` reduces preflight overhead.

## 7. Reflection Prompt

CORS is enforced by the browser, not the server. A curl request or a server-to-server call ignores CORS headers entirely. What does this mean for API security? Is CORS a sufficient defence against unauthorized access?
