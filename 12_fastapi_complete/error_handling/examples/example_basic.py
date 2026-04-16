"""
Basic example: Error Handling
==================================

FastAPI has a layered error handling system:
1. Pydantic validation errors → automatic 422 responses
2. HTTPException → automatic JSON error responses
3. Custom exception handlers → override default behavior
4. Global error handlers → catch-all for unexpected exceptions

This example demonstrates all four layers.

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

Test errors:
    curl http://localhost:8000/items/999          → 404 with custom format
    curl http://localhost:8000/items/abc          → 422 with field details
    curl -X POST http://localhost:8000/items      → 422 missing body
    curl http://localhost:8000/trigger-500        → 500 (safely handled)
"""

import traceback
import logging
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# =============================================================================
# 1. CUSTOM EXCEPTION TYPES
# =============================================================================


class AppError(Exception):
    """Base class for all application-level errors."""

    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class ResourceNotFoundError(AppError):
    def __init__(self, resource: str, resource_id):
        super().__init__(
            message=f"{resource} with id={resource_id!r} does not exist",
            code="RESOURCE_NOT_FOUND",
            status_code=404,
        )


class BusinessRuleError(AppError):
    def __init__(self, message: str, rule: str):
        super().__init__(message=message, code=f"BUSINESS_RULE_{rule.upper()}", status_code=422)


class AuthorizationError(AppError):
    def __init__(self, action: str):
        super().__init__(
            message=f"You are not authorized to perform: {action}",
            code="UNAUTHORIZED_ACTION",
            status_code=403,
        )


# =============================================================================
# 2. STANDARD ERROR RESPONSE SCHEMA
# =============================================================================


class ErrorResponse(BaseModel):
    """Consistent error format for all API errors."""

    error_id: str
    code: str
    message: str
    timestamp: datetime
    details: Optional[List[dict]] = None

    @classmethod
    def from_app_error(cls, exc: AppError) -> "ErrorResponse":
        return cls(
            error_id=str(uuid4())[:8],
            code=exc.code,
            message=exc.message,
            timestamp=datetime.now(),
        )

    @classmethod
    def from_http_exception(cls, exc: HTTPException) -> "ErrorResponse":
        return cls(
            error_id=str(uuid4())[:8],
            code=f"HTTP_{exc.status_code}",
            message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
            timestamp=datetime.now(),
        )


# =============================================================================
# 3. MODELS
# =============================================================================


class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: int = 0

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or whitespace")
        return v

    @field_validator("price")
    @classmethod
    def price_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v


class Item(BaseModel):
    id: int
    name: str
    price: float
    quantity: int


# =============================================================================
# 4. APP
# =============================================================================

app = FastAPI(title="Error Handling Example", version="1.0.0")
_db: dict[int, Item] = {
    1: Item(id=1, name="Widget A", price=9.99, quantity=50),
    2: Item(id=2, name="Widget B", price=19.99, quantity=0),
}
_next_id = 3


# ── Exception Handlers ────────────────────────────────────────────────────────


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    Handle all AppError subclasses (ResourceNotFoundError, BusinessRuleError, etc.).

    Returns a consistent ErrorResponse schema with the appropriate status code.
    """
    logger.warning("AppError: code=%s message=%s", exc.code, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.from_app_error(exc).model_dump(mode="json"),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Override the default FastAPI HTTPException handler.

    Wraps standard 401/403/404/405 etc. in the same ErrorResponse format.
    """
    logger.info("HTTPException: status=%s detail=%s", exc.status_code, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.from_http_exception(exc).model_dump(mode="json"),
        headers=exc.headers or {},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Override the default 422 Unprocessable Entity handler.

    Enriches the error with field-level detail so clients know exactly
    which field failed and why.
    """
    details = []
    for error in exc.errors():
        details.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    response = ErrorResponse(
        error_id=str(uuid4())[:8],
        code="VALIDATION_ERROR",
        message=f"{len(details)} validation error(s) in request",
        timestamp=datetime.now(),
        details=details,
    )
    logger.warning("Validation error: %s fields failed", len(details))
    return JSONResponse(status_code=422, content=response.model_dump(mode="json"))


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions.

    Logs the full traceback but returns a safe, generic error to the client
    — never expose internal stack traces to API consumers.
    """
    tb = traceback.format_exc()
    logger.error(
        "Unhandled exception on %s %s\n%s",
        request.method,
        request.url.path,
        tb,
    )
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_id=str(uuid4())[:8],
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            timestamp=datetime.now(),
        ).model_dump(mode="json"),
    )


# ── Routes ────────────────────────────────────────────────────────────────────


@app.get("/")
async def root():
    return {"message": "Error Handling Demo", "docs": "/docs"}


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Returns 404 via ResourceNotFoundError when item doesn't exist."""
    if item_id not in _db:
        raise ResourceNotFoundError("Item", item_id)
    return _db[item_id]


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item_in: ItemCreate):
    """
    Validates input with Pydantic.

    Missing/invalid fields trigger the custom validation_error_handler.
    """
    global _next_id
    item = Item(id=_next_id, **item_in.model_dump())
    _db[_next_id] = item
    _next_id += 1
    return item


@app.post("/items/{item_id}/purchase")
async def purchase_item(item_id: int, quantity: int = 1):
    """Demonstrates BusinessRuleError for domain-level validation."""
    if item_id not in _db:
        raise ResourceNotFoundError("Item", item_id)
    item = _db[item_id]
    if item.quantity < quantity:
        raise BusinessRuleError(
            f"Cannot purchase {quantity} units — only {item.quantity} in stock",
            rule="INSUFFICIENT_STOCK",
        )
    _db[item_id] = item.model_copy(update={"quantity": item.quantity - quantity})
    return {"purchased": quantity, "remaining": _db[item_id].quantity}


@app.get("/admin/secret")
async def admin_secret():
    """Raises AuthorizationError (403 in consistent format)."""
    raise AuthorizationError("view admin secrets")


@app.get("/trigger-500")
async def trigger_error():
    """
    Simulates an unhandled exception.

    The catch-all handler returns a safe 500 response without leaking details.
    """
    raise RuntimeError("Simulated internal error — this is safe in response")


@app.get("/trigger-http-404")
async def trigger_http():
    """Standard HTTPException — converted to consistent format."""
    raise HTTPException(status_code=404, detail="This resource was manually not found")


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("ERROR HANDLING — DEMO")
    print("=" * 65)
    print()
    print("Custom exception hierarchy:")
    print("  AppError")
    print("  ├─ ResourceNotFoundError  → 404")
    print("  ├─ BusinessRuleError      → 422")
    print("  └─ AuthorizationError     → 403")
    print()
    print("Handler chain:")
    print("  AppError           → @exception_handler(AppError)")
    print("  HTTPException      → @exception_handler(HTTPException)")
    print("  RequestValidation  → @exception_handler(RequestValidationError)")
    print("  anything else      → @exception_handler(Exception)  [catch-all]")
    print()
    print("Every error returns ErrorResponse:")
    print('  {"error_id": "abc12345", "code": "RESOURCE_NOT_FOUND",')
    print('   "message": "Item with id=999 does not exist",')
    print('   "timestamp": "2024-01-15T10:30:00", "details": null}')
    print()
    print("Test endpoints:")
    print("  GET  /items/999           → 404 ResourceNotFoundError")
    print("  GET  /items/abc           → 422 RequestValidationError")
    print("  POST /items (no body)     → 422 RequestValidationError")
    print("  POST /items/2/purchase?quantity=100 → 422 BusinessRuleError")
    print("  GET  /admin/secret        → 403 AuthorizationError")
    print("  GET  /trigger-500         → 500 (safely handled)")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
