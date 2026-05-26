# Testing FastAPI

Estimated time: 2 hours

## 1. Definition

FastAPI provides **`TestClient`** (synchronous, powered by httpx) for testing endpoints without running a real server. Dependency overrides let you replace real implementations (auth, DB) with test fakes, enabling true unit testing of route logic.

### Key Characteristics

- **`TestClient(app)`**: creates a test client; `with` statement handles lifespan events.
- **No server required**: tests run in-process, making them fast and predictable.
- **`app.dependency_overrides`**: dict mapping real dependencies to fake replacements.
- **Always clean up**: `app.dependency_overrides.clear()` after each test.
- **Async tests**: use `httpx.AsyncClient(app=app)` with `pytest-anyio`.

## 2. Practical Application

### Use Cases

- Integration testing: call real route handlers against an in-memory SQLite database.
- Unit testing with dependency overrides: test route logic without real auth or DB.
- Contract testing: assert response schema matches the declared `response_model`.
- Error case testing: verify 422 on invalid input, 404 on missing resource.

### Code Example

```python
from fastapi.testclient import TestClient
from myapp import app

def fake_auth():
    return "test-user"

app.dependency_overrides[get_current_user] = fake_auth

client = TestClient(app)

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
```

## 3. Why Is It Important?

### Problem It Solves

Testing against a real running server is slow, requires network setup, and introduces flakiness from external dependencies (databases, auth services). It also makes CI/CD pipelines fragile.

### Solution and Benefits

`TestClient` is deterministic, fast, and isolated. Dependency overrides eliminate external dependencies entirely. A full test suite running in-process completes in seconds.

## 4. References

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Dependency Override](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Write tests for `GET /items` (200, correct count) and `GET /items/{id}` (200 for existing, 404 for missing).

### Intermediate Level

Add a protected `POST /items` that requires auth. Write a test using `app.dependency_overrides` to bypass auth. Verify the item is created.

### Advanced Level

Create a `reset_db` pytest fixture that clears the in-memory database before each test. Write a full test class with `test_basic_functionality`, `test_edge_cases`, and `test_error_handling`.

### Success Criteria

- All tests pass without starting a server.
- Protected route tests work with dependency override.
- `reset_db` fixture ensures test isolation.
- `pytest -v` shows all tests with descriptive names.

## 6. Summary

FastAPI testing with `TestClient` is fast, deterministic, and isolated. `app.dependency_overrides` is the standard mechanism for replacing auth, DB, and external service dependencies in tests. Always clean up overrides after each test to prevent interference.

## 7. Reflection Prompt

What is the difference between an integration test and a unit test in the context of FastAPI? When does dependency override testing become insufficient, and what additional test layer would you add?
