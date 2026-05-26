"""
Basic example: Testing FastAPI
================================

FastAPI provides TestClient (powered by httpx) for synchronous testing
and an AsyncClient for async tests — both without running a real server.

This example demonstrates:
1. TestClient basics — GET, POST, assertions on status and body
2. Dependency overrides — replace real auth/DB with test fakes
3. Fixtures with pytest for app and client setup
4. Testing error cases (422, 404)
5. Async tests with httpx.AsyncClient

Run:
    pytest example_basic.py -v
    # or to see print output:
    pytest example_basic.py -v -s

Dependencies:
    pip install pytest httpx fastapi
"""


import pytest
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

# =============================================================================
# APP UNDER TEST
# =============================================================================
# In a real project, you'd import the app from your application module.
# Here we define a small app inline to keep the example self-contained.

app = FastAPI(title="TestClient Demo App")

# In-memory database
_db: dict[int, dict] = {
    1: {"id": 1, "name": "Widget A", "price": 9.99},
    2: {"id": 2, "name": "Widget B", "price": 19.99},
}
_next_id = 3


class ItemCreate(BaseModel):
    name: str
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float


# Dependency — replace in tests with an override
def get_current_user(token: str = ""):
    """Simulates token auth — returns a username or raises 401."""
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return "test-user"


@app.get("/items", response_model=list[ItemResponse])
def list_items():
    return list(_db.values())


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _db[item_id]


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, user: str = Depends(get_current_user)):
    global _next_id
    new = {"id": _next_id, **item.model_dump()}
    _db[_next_id] = new
    _next_id += 1
    return new


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, user: str = Depends(get_current_user)):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Not found")
    del _db[item_id]


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the in-memory database before each test."""
    global _db, _next_id
    _db.clear()
    _db.update(
        {
            1: {"id": 1, "name": "Widget A", "price": 9.99},
            2: {"id": 2, "name": "Widget B", "price": 19.99},
        }
    )
    _next_id = 3
    yield


@pytest.fixture
def client():
    """Unauthenticated TestClient."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client():
    """
    TestClient with dependency override that bypasses real authentication.

    This is the recommended pattern for testing protected endpoints:
    override the dependency with a fake that returns a fixed user.
    """

    def fake_auth():
        return "test-user"

    app.dependency_overrides[get_current_user] = fake_auth
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()  # always clean up


# =============================================================================
# TESTS — READ OPERATIONS
# =============================================================================


class TestListItems:
    def test_returns_all_items(self, client):
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Widget A"

    def test_response_schema(self, client):
        response = client.get("/items")
        for item in response.json():
            assert "id" in item
            assert "name" in item
            assert "price" in item


class TestGetItem:
    def test_existing_item(self, client):
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Widget A"

    def test_not_found(self, client):
        response = client.get("/items/999")
        assert response.status_code == 404
        assert "999" in response.json()["detail"]

    def test_invalid_id_type(self, client):
        """FastAPI returns 422 for path param type mismatches."""
        response = client.get("/items/not-an-int")
        assert response.status_code == 422


# =============================================================================
# TESTS — WRITE OPERATIONS (require auth override)
# =============================================================================


class TestCreateItem:
    def test_creates_item_successfully(self, auth_client):
        payload = {"name": "Widget C", "price": 29.99}
        response = auth_client.post("/items", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Widget C"
        assert data["price"] == 29.99
        assert "id" in data

    def test_created_item_appears_in_list(self, auth_client):
        auth_client.post("/items", json={"name": "Widget C", "price": 29.99})
        items = auth_client.get("/items").json()
        assert len(items) == 3

    def test_missing_name_returns_422(self, auth_client):
        response = auth_client.post("/items", json={"price": 10.0})
        assert response.status_code == 422

    def test_negative_price_passes_at_model_level(self, auth_client):
        """The model doesn't enforce price > 0 — add Field(gt=0) to fix."""
        response = auth_client.post("/items", json={"name": "X", "price": -1.0})
        assert response.status_code == 201

    def test_unauthorized_returns_401(self, client):
        """Without the auth override, real auth runs and rejects the request."""
        response = client.post(
            "/items",
            json={"name": "Widget", "price": 5.0},
            headers={"token": "wrong"},
        )
        assert response.status_code == 401


class TestDeleteItem:
    def test_deletes_existing_item(self, auth_client):
        response = auth_client.delete("/items/1")
        assert response.status_code == 204
        # Verify it's gone
        assert auth_client.get("/items/1").status_code == 404

    def test_delete_not_found(self, auth_client):
        assert auth_client.delete("/items/999").status_code == 404


# =============================================================================
# ASYNC TEST EXAMPLE
# =============================================================================


@pytest.mark.anyio
async def test_async_client():
    """
    Async tests use httpx.AsyncClient.

    Requires: pip install anyio pytest-anyio
    This test is skipped if anyio is not installed.
    """
    try:
        import httpx
        from httpx import AsyncClient

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/items")
        assert response.status_code == 200
    except ImportError:
        pytest.skip("httpx async not available")


# =============================================================================
# STANDALONE DEMO
# =============================================================================


def demo():
    print("=" * 65)
    print("TESTING FASTAPI — DEMO")
    print("=" * 65)
    print()
    print("Run tests:")
    print("  pytest example_basic.py -v")
    print()
    print("Key patterns shown:")
    print("  1. TestClient — no real server needed, synchronous")
    print("  2. app.dependency_overrides — replace auth, DB, etc.")
    print("  3. pytest fixtures — reset_db, client, auth_client")
    print("  4. Status code assertions: 200, 201, 204, 401, 404, 422")
    print("  5. AsyncClient — for testing async endpoints")
    print()
    print("Quick smoke test:")
    client = TestClient(app)
    r = client.get("/items")
    print(f"  GET /items → {r.status_code} | {len(r.json())} items")
    r = client.get("/items/1")
    print(f"  GET /items/1 → {r.status_code} | name={r.json()['name']!r}")
    r = client.get("/items/999")
    print(f"  GET /items/999 → {r.status_code} (expected 404)")
    print()
    print("=" * 65)


if __name__ == "__main__":
    demo()
