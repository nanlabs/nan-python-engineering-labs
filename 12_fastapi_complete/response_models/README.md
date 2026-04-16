# Response Models

Estimated time: 90 minutes

## 1. Definition

A **response model** tells FastAPI what shape to serialize before sending the HTTP response. It filters out fields not in the model (e.g. passwords), coerces types, and documents the response schema in the OpenAPI spec.

### Key Characteristics

- **`response_model=`**: kwarg on the route decorator — FastAPI serializes the return value through this model.
- **Filtering**: fields present in the return value but absent from the response model are stripped silently.
- **`response_model_exclude_unset`**: omits fields not explicitly set (reduces payload size).
- **`response_model_exclude`**: explicitly exclude named fields.
- **Generic response models**: `PaginatedResponse[T]` using `TypeVar` and `Generic`.
- **Multiple response schemas**: specify different models per HTTP status code via `responses={}`.

## 2. Practical Application

### Use Cases

- Hiding internal fields: `UserInDB` has `hashed_password`; `UserPublic` omits it.
- Paginated list endpoints that wrap data in metadata (`total`, `page`, `items`).
- Different response shapes per status: 200 returns `ItemResponse`, 404 returns `ErrorDetail`.
- Admin vs. public views: `UserAdmin` exposes email and role; `UserPublic` does not.

### Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str  # internal — must not be exposed

class UserPublic(BaseModel):
    id: int
    username: str

app = FastAPI()

@app.get("/users/me", response_model=UserPublic)
def get_me():
    return UserInDB(id=1, username="alice", hashed_password="secret")
    # hashed_password is stripped automatically
```

## 3. Why Is It Important?

### Problem It Solves

Without response models, any field on the returned object is included in the response. Sensitive fields (passwords, tokens, internal flags) leak to clients by default.

### Solution and Benefits

`response_model` enforces a contract at the framework level: no code path can accidentally expose a field not declared in the output model. It also documents the response schema in Swagger UI.

## 4. References

- [FastAPI Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Additional Responses](https://fastapi.tiangolo.com/advanced/additional-responses/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `UserInDB` (with `hashed_password`) and `UserResponse` (without it). Use `response_model=UserResponse` on `GET /users/me`. Verify `hashed_password` is absent from the response.

### Intermediate Level

Create a generic `PaginatedResponse[T]` with `total`, `page`, `per_page`, and `items: List[T]`. Use it as the response model for `GET /products`.

### Advanced Level

Add `responses={404: {"model": ErrorDetail}, 403: {"model": ErrorDetail}}` to a route. Write a test with `TestClient` that verifies the correct schema is returned for each status.

### Success Criteria

- `GET /users/me` JSON does not contain `hashed_password`.
- `GET /products` JSON contains `total`, `page`, and `items` array.
- `/docs` shows all declared response schemas.

## 6. Summary

`response_model` is a security and documentation primitive. It filters the return value to only the declared fields, documents the schema in OpenAPI, and prevents accidental data leakage. Generic response models eliminate repetition for paginated endpoints.

## 7. Reflection Prompt

If `response_model` filters fields at the framework level, why might you still want to avoid loading sensitive columns from the database in the first place? What does defence-in-depth mean in this context?
