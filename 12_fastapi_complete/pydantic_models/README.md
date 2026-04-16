# Pydantic Models

Estimated time: 2 hours

## 1. Definition

**Pydantic** is a data validation library that uses Python type annotations to parse, validate, coerce, and serialize data. FastAPI relies on Pydantic v2 for request body parsing, response serialization, and settings management.

### Key Characteristics

- **`BaseModel`**: base class for all models; provides parsing, validation, and serialization.
- **`field_validator`**: validator for a single field, runs after coercion.
- **`model_validator`**: cross-field validator for the whole model.
- **`computed_field`**: derived, read-only property included in serialization.
- **`model_config`**: class-level settings (e.g. `from_attributes`, `populate_by_name`).
- **Inheritance**: models can extend other models and override or add fields.

## 2. Practical Application

### Use Cases

- Validating and coercing API request bodies.
- Serializing database ORM objects to JSON responses (`from_attributes=True`).
- Creating typed settings objects from environment variables (`pydantic-settings`).
- Ensuring data integrity in internal service layers.

### Code Example

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    email: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
```

## 3. Why Is It Important?

### Problem It Solves

Without Pydantic, validation requires manual `if`/`raise` blocks repeated across every handler. Type coercion (e.g. string `"123"` → `int 123`) must be done explicitly. Serialization needs custom `__dict__` or `json.dumps` logic.

### Solution and Benefits

Pydantic provides a single source of truth: the model definition simultaneously drives validation, coercion, documentation, and serialization. Errors are collected and returned as structured 422 responses.

## 4. References

- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic Field Types](https://docs.pydantic.dev/latest/concepts/types/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `Product` model with `name: str`, `price: float`, and `in_stock: bool`. Add a `field_validator` that ensures `price > 0`.

### Intermediate Level

Add a `computed_field` called `price_with_tax` that returns `price * 1.21`. Add a `model_validator` that sets `in_stock = False` if `price == 0`.

### Advanced Level

Create a `ProductCreate` (input) and `ProductResponse` (output) pair. `ProductResponse` adds an `id: int` and inherits from `ProductCreate`. Demonstrate serialization with `by_alias=True` and `exclude_none=True`.

### Success Criteria

- `Product(name="A", price=-1.0)` raises a `ValidationError`.
- `computed_field` `price_with_tax` appears in `model_dump()`.
- `ProductResponse` serializes to JSON correctly.

## 6. Summary

Pydantic models are the data backbone of FastAPI. They handle validation, coercion, computed fields, and serialization from a single class definition. Understanding `field_validator`, `model_validator`, and `computed_field` is essential for building robust APIs.

## 7. Reflection Prompt

When should you use separate input and output models (e.g. `UserCreate` vs `UserResponse`) instead of a single model? What security risk does using a single model expose?
