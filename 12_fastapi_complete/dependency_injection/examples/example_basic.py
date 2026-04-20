"""
Basic example: Dependency Injection
=====================================

FastAPI's Depends() system lets you declare reusable, composable
dependencies that are resolved automatically per request.

This example demonstrates:
1. Simple function-based dependency (pagination)
2. Dependency with sub-dependencies (auth token → user)
3. Class-based dependency (query filter builder)
4. Dependency with cleanup (database session)
5. Overriding dependencies in tests

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel

# =============================================================================
# MODELS
# =============================================================================


class User(BaseModel):
    id: int
    username: str
    role: str


class Item(BaseModel):
    id: int
    name: str
    owner_id: int
    price: float


class PaginationParams(BaseModel):
    skip: int
    limit: int


# =============================================================================
# FAKE DATA
# =============================================================================

FAKE_TOKENS = {
    "token-alice": User(id=1, username="alice", role="admin"),
    "token-bob": User(id=2, username="bob", role="viewer"),
}

ITEMS_DB: list[Item] = [
    Item(id=i, name=f"Item {i}", owner_id=(i % 2) + 1, price=round(i * 9.99, 2))
    for i in range(1, 11)
]


# =============================================================================
# DEPENDENCIES
# =============================================================================


# ── 1. Simple function dependency ────────────────────────────────────────────


def get_pagination(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(5, ge=1, le=50, description="Max records to return"),
) -> PaginationParams:
    """
    Reusable pagination dependency.

    Any route that uses Depends(get_pagination) gets validated
    skip + limit query params automatically.
    """
    return PaginationParams(skip=skip, limit=limit)


# ── 2. Authentication dependency chain ──────────────────────────────────────


def get_token(authorization: Annotated[str, Header()] = ""):
    """
    Extract and validate the Bearer token from the Authorization header.

    Sub-dependency: used by get_current_user.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(token: str = Depends(get_token)) -> User:
    """
    Resolve a token to a User object.

    Depends on get_token — FastAPI builds the dependency chain automatically.
    """
    user = FAKE_TOKENS.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Admin-only guard. Wraps get_current_user."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# ── 3. Class-based dependency ────────────────────────────────────────────────


@dataclass
class ItemFilter:
    """
    Class-based dependency for filtering items.

    Using a class lets you store state and group related query params.
    FastAPI instantiates this per request.
    """

    min_price: float | None = Query(None, ge=0, description="Minimum price")
    max_price: float | None = Query(None, ge=0, description="Maximum price")
    owner_id: int | None = Query(None, ge=1, description="Filter by owner")

    def apply(self, items: list[Item]) -> list[Item]:
        result = items
        if self.min_price is not None:
            result = [i for i in result if i.price >= self.min_price]
        if self.max_price is not None:
            result = [i for i in result if i.price <= self.max_price]
        if self.owner_id is not None:
            result = [i for i in result if i.owner_id == self.owner_id]
        return result


# ── 4. Dependency with cleanup (simulated DB session) ────────────────────────


class FakeDbSession:
    """Simulates a database session with open/close lifecycle."""

    def __init__(self):
        self.active = True
        self._log: list[str] = []

    def query(self, table: str) -> str:
        if not self.active:
            raise RuntimeError("Session is closed")
        entry = f"SELECT * FROM {table}"
        self._log.append(entry)
        return entry

    def close(self):
        self.active = False


def get_db():
    """
    Dependency that yields a session and closes it after the request.

    The yield-based pattern (like a context manager) ensures cleanup
    runs even if the route raises an exception.
    """
    db = FakeDbSession()
    try:
        yield db
    finally:
        db.close()


# =============================================================================
# APP + ROUTES
# =============================================================================

app = FastAPI(title="Dependency Injection Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Dependency Injection Demo", "docs": "/docs"}


@app.get("/items", response_model=list[Item])
async def list_items(
    pagination: PaginationParams = Depends(get_pagination),
    item_filter: ItemFilter = Depends(ItemFilter),
):
    """
    List items with pagination and optional filtering.

    Uses two independent dependencies composed in one route.
    """
    filtered = item_filter.apply(ITEMS_DB)
    return filtered[pagination.skip : pagination.skip + pagination.limit]


@app.get("/items/mine", response_model=list[Item])
async def list_my_items(
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(get_pagination),
):
    """
    Return the authenticated user's own items.

    Requires a valid Bearer token in the Authorization header.
    Try: Authorization: Bearer token-alice
    """
    my_items = [i for i in ITEMS_DB if i.owner_id == current_user.id]
    return my_items[pagination.skip : pagination.skip + pagination.limit]


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    admin: User = Depends(require_admin),
):
    """
    Admin-only endpoint — delete an item.

    Uses a dependency chain: require_admin → get_current_user → get_token.
    Try with: Authorization: Bearer token-alice  (admin)
    Fails with: Authorization: Bearer token-bob   (viewer)
    """
    global ITEMS_DB
    original_count = len(ITEMS_DB)
    ITEMS_DB = [i for i in ITEMS_DB if i.id != item_id]
    if len(ITEMS_DB) == original_count:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/db-demo")
async def db_demo(db: FakeDbSession = Depends(get_db)):
    """
    Demonstrate yield-based dependency with cleanup.

    The session is created at request start and closed after response.
    """
    q1 = db.query("items")
    q2 = db.query("users")
    return {"queries_run": [q1, q2], "session_active": db.active}


@app.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("DEPENDENCY INJECTION — DEMO")
    print("=" * 65)
    print()
    print("Dependency graph:")
    print()
    print("  get_pagination  ─────────────────── simple, no sub-deps")
    print("  get_token       ─────────────────── reads Authorization header")
    print("  get_current_user ── Depends(get_token)")
    print("  require_admin   ──── Depends(get_current_user)")
    print("  ItemFilter      ─────────────────── class-based, query params")
    print("  get_db          ─────────────────── yield-based with cleanup")
    print()
    print("Routes:")
    print("  GET  /items        — pagination + filter (no auth)")
    print("  GET  /items/mine   — auth required (viewer or admin)")
    print("  DELETE /items/{id} — admin only")
    print("  GET  /me           — current user from token")
    print("  GET  /db-demo      — yield dependency lifecycle")
    print()
    print("Test tokens:")
    print("  Authorization: Bearer token-alice  (admin)")
    print("  Authorization: Bearer token-bob    (viewer)")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
