"""
Basic example: CORS (Cross-Origin Resource Sharing)
=====================================================

CORS is a browser security mechanism that controls which origins (domains)
can make requests to your API from JavaScript running in a browser.

This example demonstrates:
1. Permissive CORS (allow all origins — dev/public APIs)
2. Strict CORS (explicit allow list — production)
3. Credentials CORS (cookies + auth headers)
4. Preflight (OPTIONS) request handling
5. Per-route CORS override pattern

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

Test with curl:
    curl -H "Origin: http://example.com" \
         -H "Access-Control-Request-Method: POST" \
         -H "Access-Control-Request-Headers: Content-Type" \
         -X OPTIONS http://localhost:8000/api/strict/data -v
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =============================================================================
# CORS CONFIGURATION PROFILES
# =============================================================================

# Profile 1 — Public API (allow all origins, no credentials)
PUBLIC_CORS = dict(
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Profile 2 — Production (strict allow list)
PRODUCTION_CORS = dict(
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
        "http://localhost:3000",  # local dev frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
    expose_headers=["X-Process-Time-Ms", "X-Correlation-ID"],
    max_age=600,  # preflight cache seconds
)


# =============================================================================
# MODELS
# =============================================================================


class DataItem(BaseModel):
    id: int
    value: str
    public: bool = True


# =============================================================================
# APPS
# =============================================================================

# We create one FastAPI app and show both configurations via different routers.
# In a real project you would pick ONE CORSMiddleware configuration.

app = FastAPI(
    title="CORS Example",
    version="1.0.0",
    description=(
        "Demonstrates CORSMiddleware configuration. "
        "In production, use the strict allow list — never allow_origins=['*'] "
        "together with allow_credentials=True."
    ),
)

# Apply the PRODUCTION_CORS profile for the whole app.
# Swap with PUBLIC_CORS to allow all origins.
app.add_middleware(CORSMiddleware, **PRODUCTION_CORS)


# =============================================================================
# ROUTES
# =============================================================================


@app.get("/")
async def root():
    return {"message": "CORS Demo", "docs": "/docs"}


@app.get("/api/public/data")
async def get_public_data():
    """
    Public endpoint — safe to call from any browser.

    CORSMiddleware adds `Access-Control-Allow-Origin: *` automatically
    when the request Origin is not in the strict allow list (in this example,
    only allowed origins get the header — others are rejected by the browser).
    """
    return {
        "items": [
            DataItem(id=1, value="apple", public=True),
            DataItem(id=2, value="banana", public=True),
        ]
    }


@app.get("/api/strict/data")
async def get_strict_data(request: Request):
    """
    Production endpoint — only pre-approved origins may access.

    The browser checks that `Access-Control-Allow-Origin` matches the
    requesting page's origin. If not, the browser blocks the response.
    """
    origin = request.headers.get("origin", "no-origin")
    return {
        "data": [{"id": 1, "secret": "top-secret-value"}],
        "request_origin": origin,
    }


@app.post("/api/strict/data")
async def post_strict_data(item: DataItem):
    """
    POST endpoint — demonstrates that browsers send a preflight OPTIONS
    request before any cross-origin POST with a body.

    CORSMiddleware handles OPTIONS automatically.
    """
    return {"created": item, "status": "accepted"}


@app.get("/cors/config")
async def show_cors_config():
    """Return the active CORS configuration (for debugging)."""
    return {
        "active_profile": "PRODUCTION_CORS",
        "config": {
            "allow_origins": PRODUCTION_CORS["allow_origins"],
            "allow_credentials": PRODUCTION_CORS["allow_credentials"],
            "allow_methods": PRODUCTION_CORS["allow_methods"],
            "allow_headers": PRODUCTION_CORS["allow_headers"],
            "expose_headers": PRODUCTION_CORS["expose_headers"],
            "max_age_seconds": PRODUCTION_CORS["max_age"],
        },
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("CORS — DEMO")
    print("=" * 65)
    print()
    print("Active profile: PRODUCTION_CORS")
    print()
    print("Allowed origins:")
    for origin in PRODUCTION_CORS["allow_origins"]:
        print(f"  {origin}")
    print()
    print("Key rules:")
    print("  ✓ allow_origins=['*'] + allow_credentials=True is FORBIDDEN")
    print("    → browsers will reject this combination")
    print("  ✓ max_age caches preflight results (reduces OPTIONS requests)")
    print("  ✓ expose_headers makes custom response headers readable from JS")
    print()
    print("Test preflight request:")
    print('  curl -H "Origin: http://localhost:3000" \\')
    print('       -H "Access-Control-Request-Method: POST" \\')
    print("       -X OPTIONS http://localhost:8000/api/strict/data -v")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
