# Error Handling

Estimated time: 90 minutes

## 1. Definition

FastAPI has a layered error handling system. Pydantic validation errors produce automatic 422 responses; `HTTPException` produces JSON error responses; custom exception handlers intercept specific exception types; and a global catch-all handler prevents unhandled exceptions from leaking stack traces to clients.

### Key Characteristics

- **`HTTPException`**: standard FastAPI exception with `status_code` and `detail`.
- **`@app.exception_handler(ExcType)`**: registers a custom handler for a specific exception class.
- **`RequestValidationError`**: raised by Pydantic on body/query/path validation failure; caught to customise 422 format.
- **Custom exception hierarchy**: `AppError` → `ResourceNotFoundError`, `BusinessRuleError` — typed, consistent errors.
- **Catch-all handler**: `exception_handler(Exception)` logs the traceback but returns a safe 500 to the client.

## 2. Practical Application

### Use Cases

- Returning consistent `{"error_id": ..., "code": ..., "message": ...}` format for all errors.
- 404 with meaningful context: `"Item with id=42 does not exist"` rather than `"Not found"`.
- Business rule violations as 422: `"Cannot purchase 10 units — only 3 in stock"`.
- Catching unhandled exceptions to log the traceback and return a safe 500.

### Code Example

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ItemNotFound(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

app = FastAPI()

@app.exception_handler(ItemNotFound)
async def item_not_found(request: Request, exc: ItemNotFound):
    return JSONResponse(status_code=404, content={"error": f"Item {exc.item_id} not found"})
```

## 3. Why Is It Important?

### Problem It Solves

Without custom handlers, FastAPI returns different error formats for different error types (Pydantic 422, HTTP exceptions, unhandled 500). Clients must handle multiple schemas. Unhandled exceptions leak stack traces.

### Solution and Benefits

Custom handlers normalise all errors to a single `ErrorResponse` schema. Clients parse one format. Stack traces are logged server-side and never exposed. A typed exception hierarchy makes error handling code explicit and testable.

## 4. References

- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Custom Exception Handlers](https://fastapi.tiangolo.com/advanced/custom-response/#errors)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `ResourceNotFoundError` exception and a `@exception_handler` that returns a 404 with `{"code": "NOT_FOUND", "message": "..."}`.

### Intermediate Level

Override the default `RequestValidationError` handler to return the same `ErrorResponse` format with a `details` array listing each failing field.

### Advanced Level

Create a catch-all `exception_handler(Exception)` that logs the full traceback and returns a generic 500 response. Test that raising an unhandled `RuntimeError` in a route returns 500 (not a stack trace).

### Success Criteria

- All error responses share the same JSON schema.
- `GET /items/999` returns 404 with `code: "RESOURCE_NOT_FOUND"`.
- Invalid body returns 422 with a `details` array.
- Unhandled exception returns 500 without exposing the traceback.

## 6. Summary

Custom exception handlers normalise error formats across all error types. A domain-specific exception hierarchy (`ResourceNotFoundError`, `BusinessRuleError`) makes error handling explicit and testable. A catch-all handler prevents stack trace exposure. The key constraint: never return internal error details to API consumers.

## 7. Reflection Prompt

Should `HTTPException` and your custom `AppError` hierarchy be separate, or should `AppError` subclass `HTTPException`? What are the trade-offs for code organisation, framework coupling, and testability?
