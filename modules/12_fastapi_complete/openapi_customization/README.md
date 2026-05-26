# OpenAPI Customization

Estimated time: 90 minutes

## 1. Definition

FastAPI auto-generates an OpenAPI 3.x schema from your code. You can enrich it at every level: application metadata, tag groups, per-route descriptions, request/response examples, and raw schema extensions — all without leaving Python.

### Key Characteristics

- **App metadata**: `title`, `version`, `description` (supports Markdown), `contact`, `license_info`.
- **Tag metadata**: `openapi_tags` list with `name`, `description`, and `externalDocs`.
- **`Field(examples=[...])`**: inline examples shown in Swagger UI's "Try it out" panel.
- **`model_config["json_schema_extra"]`**: model-level examples.
- **`deprecated=True`**: marks a route as deprecated in docs.
- **Custom `openapi()` hook**: override to add `x-*` extensions or restructure the schema.

## 2. Practical Application

### Use Cases

- Multi-team APIs where each team owns a tag group with its own description.
- Client SDK generators that rely on `operationId` and examples.
- Partner-facing APIs requiring contact info and license in the schema.
- Legacy endpoints that need deprecation markers before removal.

### Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., examples=["FastAPI Book"])
    price: float = Field(..., examples=[29.99])

app = FastAPI(
    title="My API",
    description="## My API\n\nA well-documented REST API.",
    contact={"name": "Team", "email": "api@example.com"},
)
```

## 3. Why Is It Important?

### Problem It Solves

Auto-generated schemas often lack human-readable descriptions, concrete examples, and organizational structure. Partners and frontend teams struggle to understand endpoints from field names alone.

### Solution and Benefits

Rich OpenAPI documentation reduces onboarding time, eliminates misunderstandings, and enables client SDK generation. Inline examples in Swagger UI let consumers test endpoints without writing any code.

## 4. References

- [FastAPI Metadata](https://fastapi.tiangolo.com/tutorial/metadata/)
- [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.0)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Add `title`, `description` (multi-line Markdown), `contact`, and `license_info` to your FastAPI app. View the result in `/docs`.

### Intermediate Level

Define `openapi_tags` with two tag groups (e.g. "Users" and "Products"). Add an `externalDocs` link to each. Verify grouping in Swagger UI.

### Advanced Level

Override `app.openapi()` to inject `x-logo` and `x-api-id` into the schema's `info` block. Add per-route `responses={404: {"model": ErrorDetail}}` documentation.

### Success Criteria

- `/docs` shows Markdown-formatted description.
- Tags appear as collapsible groups in Swagger UI.
- `GET /openapi.json` contains `x-logo` in the `info` block.
- A deprecated route is visually marked in `/docs`.

## 6. Summary

FastAPI's OpenAPI customization operates at three levels: application metadata, tag groups, and per-route annotations. Field-level `examples` drive Swagger UI's "Try it out" panel. The custom `openapi()` hook provides unlimited schema control for advanced integrations.

## 7. Reflection Prompt

OpenAPI schemas can be used to auto-generate client SDKs in TypeScript, Go, or Java. How does the quality of your schema documentation (descriptions, examples, `operationId`) affect the quality of the generated client code?
