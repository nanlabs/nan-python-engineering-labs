# Request Body

Estimated time: 90 minutes

## 1. Definition

A **request body** carries structured data from the client to the server in the HTTP request payload. FastAPI reads it from the body of `POST`, `PUT`, and `PATCH` requests and validates it against a Pydantic model before passing it to your route handler.

### Key Characteristics

- **Pydantic model argument**: any function argument typed with a Pydantic `BaseModel` subclass is automatically read from the JSON body.
- **`Body()`**: metadata helper — marks a parameter as body, adds embedded examples, and controls whether it is required.
- **Nested models**: complex validation with nested objects, lists, and discriminated unions.
- **`model_validator`**: cross-field validation at the model level after all fields are parsed.
- **`exclude_unset=True`**: for PATCH semantics — distinguish `null` from "not provided".

## 2. Practical Application

### Use Cases

- Creating resources: `POST /orders` with a full order payload.
- Replacing resources: `PUT /orders/{id}` with a complete replacement body.
- Partial updates: `PATCH /orders/{id}` where only provided fields are updated.
- Complex nested payloads: orders with line items, addresses, and coupon codes.

### Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    customer_email: str
    items: list[str]
    total: float

app = FastAPI()

@app.post("/orders", status_code=201)
def create_order(order: CreateOrderRequest):
    return {"id": 1, **order.model_dump()}
```

## 3. Why Is It Important?

### Problem It Solves

Parsing, validating, and documenting JSON request bodies manually is verbose and fragile. Missing validation lets malformed or malicious payloads reach business logic.

### Solution and Benefits

FastAPI + Pydantic parses and validates the body in one step, returns a structured 422 on failure, documents the schema in Swagger UI, and provides Python type safety throughout the handler.

## 4. References

- [Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Nested Models](https://fastapi.tiangolo.com/tutorial/body-nested-models/)
- [Body with Multiple Parameters](https://fastapi.tiangolo.com/tutorial/body-multiple-params/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `POST /notes` with a `CreateNoteRequest` model (`title: str`, `content: str`, `pinned: bool = False`). Return the created note with an auto-assigned ID.

### Intermediate Level

Add `PATCH /notes/{id}` with all fields optional. Use `model_dump(exclude_unset=True)` to apply only the provided fields. Return 404 if the note doesn't exist.

### Advanced Level

Add a `model_validator` to ensure `content` is not empty when `pinned=True`. Add an `Annotated` field with a `Field(max_length=500)` constraint on `content`.

### Success Criteria

- `POST /notes` with a missing `title` returns 422.
- `PATCH /notes/1` with only `{"pinned": true}` updates only that field.
- Pinning a note with empty content returns 422 (model validator).

## 6. Summary

Request bodies are read from the JSON payload and validated against a Pydantic model. Nested models handle complex structures. PATCH endpoints use `exclude_unset=True` to implement partial-update semantics cleanly.

## 7. Reflection Prompt

What is the difference between a `field_validator` and a `model_validator`? In which scenarios does each one apply, and how do they interact when both are defined on the same model?
