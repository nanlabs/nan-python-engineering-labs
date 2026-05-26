# Routing

Estimated time: 2 hours

## 1. Definition

FastAPI's **router** system lets you split route definitions across multiple files and then mount them into a single application. A `APIRouter` instance works like a mini-app: it collects route handlers, prefixes, tags, and dependencies, then `include_router()` merges it into the main `FastAPI` app at a chosen URL prefix.

### Key Characteristics

- **`APIRouter`**: a lightweight container for related routes — identical interface to `FastAPI` for decorating endpoints.
- **`prefix`**: prepended to every path registered on the router (e.g. `prefix="/users"` turns `/` into `/users/`).
- **`tags`**: grouped label that appears in the Swagger UI; all routes on the router inherit it.
- **`dependencies`**: router-level dependencies (e.g. auth) applied to every route without repeating `Depends()`.
- **`include_router()`**: merges the router into the app; can be called multiple times or nested.

## 2. Practical Application

### Use Cases

- Splitting a growing API into domain modules: `users.py`, `products.py`, `orders.py`.
- Versioning endpoints under `/v1/` and `/v2/` using separate routers.
- Applying authentication to a whole group of routes via router-level dependencies.
- Nested routers for hierarchical resources (e.g. `/users/{user_id}/orders`).

### Code Example

```python
from fastapi import FastAPI, APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])
products_router = APIRouter(prefix="/products", tags=["Products"])

@users_router.get("/")
def list_users():
    return [{"id": 1, "name": "Alice"}]

@products_router.get("/")
def list_products():
    return [{"id": 1, "name": "Widget"}]

app = FastAPI()
app.include_router(users_router)
app.include_router(products_router)
```

## 3. Why Is It Important?

### Problem It Solves

Without routers, every endpoint lives in one file. As an API grows, a single `main.py` with 50+ routes becomes impossible to maintain, review, or test in isolation.

### Solution and Benefits

Routers enforce a module boundary: each domain owns its own router, its own models, and its own tests. The main app file becomes a thin orchestrator. Teams can work on separate routers without merge conflicts.

## 4. References

- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [APIRouter reference](https://fastapi.tiangolo.com/reference/apirouter/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `FastAPI` app with two routers: one for `/items` (CRUD) and one for `/categories`. Each router should live in a separate variable. Register them with `include_router()`.

### Intermediate Level

Add a `/v1/` prefix to both routers and apply a `get_api_key` dependency at the router level so all routes require a valid API key.

### Advanced Level

Create a nested router for `/users/{user_id}/addresses`. The parent router handles `/users` and the child router handles addresses, mounted under the parent via `include_router(addresses_router, prefix="/{user_id}/addresses")`.

### Success Criteria

- `GET /items` and `GET /categories` return 200.
- Unauthorized requests return 401 when the key dependency is added.
- Nested `/users/1/addresses` resolves the `user_id` path parameter correctly.

## 6. Summary

`APIRouter` is FastAPI's modular routing primitive. Routers carry prefixes, tags, and dependencies, and are merged into the app with `include_router()`. They are the primary tool for keeping large APIs organized and testable.

## 7. Reflection Prompt

When would you choose to version your API by creating `/v1` and `/v2` routers versus using a query parameter like `?version=2`? What are the trade-offs for clients, for documentation, and for your team's workflow?
