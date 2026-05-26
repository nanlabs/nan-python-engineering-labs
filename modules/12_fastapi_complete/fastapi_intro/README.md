# FastAPI Intro

Estimated time: 2–3 hours

## 1. Definition

**FastAPI** is a modern, high-performance Python web framework for building APIs with Python 3.7+ based on standard type hints. It is built on top of Starlette for web handling and Pydantic for data validation.

### Key Characteristics

- **High performance**: on par with NodeJS and Go — thanks to Starlette and async support.
- **Automatic documentation**: generates Swagger UI (`/docs`) and ReDoc (`/redoc`) automatically.
- **Type safety**: uses Python type hints for request/response validation via Pydantic.
- **Standards-based**: fully compatible with OpenAPI and JSON Schema.
- **Easy to learn**: designed to be intuitive and reduce code duplication.

## 2. Practical Application

### Use Cases

1. **REST API backends**: build CRUD APIs for web and mobile applications.
1. **Microservices**: create lightweight, independent services with clear contracts.
1. **Data science APIs**: expose ML models or data processing pipelines as HTTP endpoints.

### Code Example

```python
# See examples/example_basic.py for a complete runnable FastAPI app
```

Run the server with:

```bash
uvicorn example_basic:app --reload
```

Then visit `http://localhost:8000/docs` for interactive documentation.

## 3. Why Is It Important?

### Problem It Solves

Traditional Python web frameworks (Flask, Django) require manual serialization/deserialization, lack built-in async support, and need third-party tools for API documentation. This leads to boilerplate, runtime errors from type mismatches, and outdated docs.

### Solution and Benefits

FastAPI eliminates boilerplate by deriving validation, serialization, and documentation directly from type hints. Async support enables high concurrency without threads. The result is less code, fewer bugs, and always-accurate documentation.

## 4. References

See [references/links.md](references/links.md) for official documentation and additional resources.

## 5. Practice Task

Use `exercises/exercise_01.py` as the starting point.

### Basic Level

- Create a FastAPI app with a `GET /` root endpoint returning a welcome message.
- Add a `GET /items/{item_id}` endpoint that returns an item by ID.

### Intermediate Level

- Add POST, PUT, and DELETE endpoints for a resource.
- Validate path and query parameters using FastAPI's built-in tools.

### Advanced Level

- Add Pydantic models for request and response bodies.
- Implement in-memory CRUD with proper HTTP status codes.
- Add a `/stats` endpoint summarizing the current state.

### Success Criteria

- All endpoints return correct HTTP status codes.
- Invalid inputs return 422 Unprocessable Entity automatically.
- Interactive docs at `/docs` accurately reflect all endpoints.

## 6. Summary

- FastAPI is the fastest way to build production-ready APIs in Python.
- Type hints drive automatic validation, serialization, and documentation.
- Async support enables high throughput without complex threading.

## 7. Reflection Prompt

After completing this topic, reflect on:

- How does FastAPI's type-hint-driven approach compare to Flask's decorator style?
- What would break if you removed Pydantic validation from your endpoints?
- How would you structure a real-world project using FastAPI?
