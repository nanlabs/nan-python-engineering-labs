# Path & Query Parameters

Estimated time: 90 minutes

## 1. Definition

FastAPI extracts **path parameters** directly from the URL template (e.g. `/items/{item_id}`) and **query parameters** from the URL query string (e.g. `?skip=0&limit=10`). Both are declared as regular function arguments and are automatically validated and documented.

### Key Characteristics

- **Path parameters**: required by default; declared with `{name}` in the path template.
- **Query parameters**: optional when given a default value; validated by Pydantic under the hood.
- **`Path()`**: metadata helper for path params — adds constraints (`ge`, `le`), description, and examples.
- **`Query()`**: metadata helper for query params — adds constraints, regex patterns, aliases, and deprecation.
- **Type annotations** drive automatic coercion: `int`, `float`, `bool`, `Enum`, `datetime`, `UUID`.

## 2. Practical Application

### Use Cases

- Resource lookup by ID: `GET /products/{product_id}`.
- Paginated lists: `GET /products?skip=0&limit=20`.
- Filtering by category and availability: `GET /products?category=books&in_stock=true`.
- Enum-constrained parameters: `?sort=asc` validated against `SortOrder` enum.

### Code Example

```python
from fastapi import FastAPI, Path, Query
from typing import Optional

app = FastAPI()

@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(..., ge=1, description="Product ID"),
    include_details: bool = Query(False, description="Include extended details"),
):
    return {"id": product_id, "details": include_details}
```

## 3. Why Is It Important?

### Problem It Solves

Without validation, a route handler receives raw strings. Parsing and validating `int`, `bool`, and enum values manually is repetitive and error-prone, and missing checks let bad inputs reach your database.

### Solution and Benefits

FastAPI validates path and query parameters before calling your function, returns a structured 422 response on failure, and generates accurate OpenAPI schema — all from the type annotation alone.

## 4. References

- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [Path/Query Metadata](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `GET /users/{user_id}` where `user_id` must be an integer ≥ 1. Return a 404 if the ID is not found in a small in-memory dict.

### Intermediate Level

Add `GET /users` with optional `name` (string, max length 50), `active` (bool, default `True`), and pagination (`skip`, `limit` with sensible constraints). Filter the user list accordingly.

### Advanced Level

Add an `order_by` enum parameter (`name`, `created_at`, `email`) and a `sort` direction enum (`asc`, `desc`). Apply sorting to the result. Validate that `skip + limit ≤ 1000`.

### Success Criteria

- `GET /users/0` returns 422 (constraint violation).
- `GET /users?limit=abc` returns 422 (type coercion failure).
- Valid combinations return correctly filtered and sorted results.

## 6. Summary

Path parameters are required, positional URL segments. Query parameters are optional key-value pairs appended after `?`. FastAPI validates both automatically from type annotations, and `Path()` / `Query()` add richer constraints and documentation without extra code.

## 7. Reflection Prompt

When should you represent a filter as a query parameter versus as a path parameter? How does your choice affect URL readability, caching behaviour, and the OpenAPI schema?
