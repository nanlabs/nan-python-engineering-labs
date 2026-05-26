# Dependency Injection

Estimated time: 2 hours

## 1. Definition

FastAPI's **dependency injection** (DI) system lets you declare shared logic — authentication, database sessions, pagination, configuration — as functions or classes, then inject them into route handlers using `Depends()`. Dependencies can themselves depend on other dependencies (chaining).

### Key Characteristics

- **`Depends(fn)`**: declares that a route requires the return value of `fn`.
- **Chaining**: a dependency can call `Depends()` on another dependency.
- **Class-based**: a class with `__call__` works as a dependency — useful for stateful helpers.
- **`yield`-based**: use `yield` for resources that need cleanup (DB sessions, locks).
- **Router-level**: apply a dependency to every route on a router without repeating it.

## 2. Practical Application

### Use Cases

- Validating and decoding JWT tokens before each protected route.
- Injecting a database session that is committed or rolled back after the request.
- Reusable pagination parameters (`skip`, `limit`) shared across all list endpoints.
- Role-based access control via chained dependencies.

### Code Example

```python
from fastapi import FastAPI, Depends

def get_pagination(skip: int = 0, limit: int = 20):
    return {"skip": skip, "limit": limit}

app = FastAPI()

@app.get("/items")
def list_items(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination, "items": []}
```

## 3. Why Is It Important?

### Problem It Solves

Without DI, authentication logic, session setup, and pagination parsing are copy-pasted into every route. Changing the auth scheme requires editing every handler.

### Solution and Benefits

DI centralizes cross-cutting concerns. Changing `get_current_user` automatically updates every route that depends on it. Testing becomes trivial with `app.dependency_overrides`.

## 4. References

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Yield Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `get_pagination(skip: int = 0, limit: int = 20)` dependency and inject it into `GET /items` and `GET /users`.

### Intermediate Level

Create `get_token(token: str = Header(None))` → `get_current_user(token_data=Depends(get_token))`. Protect `GET /profile` with `Depends(get_current_user)`.

### Advanced Level

Create a `require_admin` dependency that chains `get_current_user` and checks for an admin role. Apply it at the router level to protect all admin routes.

### Success Criteria

- `GET /items?limit=abc` returns 422 (DI validates types).
- `GET /profile` without token returns 401.
- `GET /admin/users` without admin role returns 403.

## 6. Summary

`Depends()` is FastAPI's composable dependency injection mechanism. It supports function dependencies, class-based dependencies, `yield`-based cleanup, chaining, and router-level application. It is the primary tool for sharing and testing cross-cutting concerns.

## 7. Reflection Prompt

How does FastAPI's dependency injection differ from traditional Python argument passing? When would you choose a class-based dependency over a plain function, and what does the `yield` keyword enable that a regular `return` cannot?
