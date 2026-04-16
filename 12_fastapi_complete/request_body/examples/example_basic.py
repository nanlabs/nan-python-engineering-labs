"""
Basic example: Request Body Handling
======================================

FastAPI uses Pydantic models declared as function parameters to parse,
validate, and document JSON request bodies automatically.

This example demonstrates:
1. Single JSON body
2. Nested models in the body
3. Multiple body parameters
4. Body with extra metadata (examples, field aliases)
5. Partial updates with Optional fields (PATCH pattern)

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime


# =============================================================================
# MODELS
# =============================================================================


class Address(BaseModel):
    """Nested model for a shipping address."""

    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2 code")
    postal_code: str = Field(..., pattern=r"^\d{4,10}$")


class OrderItem(BaseModel):
    """A single line item in an order."""

    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1, le=100)
    unit_price: float = Field(..., gt=0)

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)


class CreateOrderRequest(BaseModel):
    """
    Full request body for creating an order.

    Demonstrates nested models, list fields, and cross-field validation.
    """

    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    shipping_address: Address
    items: List[OrderItem] = Field(..., min_length=1)
    coupon_code: Optional[str] = Field(None, pattern=r"^[A-Z0-9]{6,12}$")
    notes: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def check_items_not_duplicate(self) -> "CreateOrderRequest":
        product_ids = [item.product_id for item in self.items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate product IDs are not allowed in a single order")
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_name": "Alice Smith",
                "customer_email": "alice@example.com",
                "shipping_address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "country": "US",
                    "postal_code": "62701",
                },
                "items": [
                    {"product_id": 1, "quantity": 2, "unit_price": 29.99},
                    {"product_id": 3, "quantity": 1, "unit_price": 199.00},
                ],
                "coupon_code": "SAVE10",
                "notes": "Please leave at the door.",
            }
        }
    }


class OrderResponse(BaseModel):
    """Response after creating an order."""

    order_id: int
    customer_name: str
    total: float
    discount: float
    final_total: float
    status: str
    created_at: datetime


class PatchOrderRequest(BaseModel):
    """Partial update model — all fields are optional."""

    shipping_address: Optional[Address] = None
    notes: Optional[str] = Field(None, max_length=500)
    coupon_code: Optional[str] = Field(None, pattern=r"^[A-Z0-9]{6,12}$")


# =============================================================================
# IN-MEMORY STORE
# =============================================================================

COUPONS = {"SAVE10": 0.10, "SAVE20": 0.20, "HALFOFF": 0.50}
orders_db: dict[int, dict] = {}
_order_counter = 1


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Request Body Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Request Body Demo", "docs": "/docs"}


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderRequest):
    """
    Create a new order.

    The entire request body is a single Pydantic model with nested models.
    FastAPI validates everything automatically — types, constraints, and
    the custom cross-field validator (no duplicate product IDs).
    """
    global _order_counter

    total = round(sum(item.subtotal for item in order.items), 2)
    discount = round(total * COUPONS.get(order.coupon_code or "", 0), 2)
    final_total = round(total - discount, 2)

    order_record = {
        "order_id": _order_counter,
        "data": order.model_dump(),
        "total": total,
        "discount": discount,
        "final_total": final_total,
        "status": "pending",
        "created_at": datetime.now(),
    }
    orders_db[_order_counter] = order_record
    _order_counter += 1

    return OrderResponse(
        order_id=order_record["order_id"],
        customer_name=order.customer_name,
        total=total,
        discount=discount,
        final_total=final_total,
        status="pending",
        created_at=order_record["created_at"],
    )


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    """Fetch an order by ID."""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


@app.patch("/orders/{order_id}")
async def patch_order(order_id: int, patch: PatchOrderRequest):
    """
    Partially update an order.

    Only the fields provided in the body are updated.
    Uses model_dump(exclude_unset=True) to ignore fields not sent by the client.
    """
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    updates = patch.model_dump(exclude_unset=True)
    orders_db[order_id]["data"].update(updates)
    return {"order_id": order_id, "updated_fields": list(updates.keys()), "status": "updated"}


@app.post("/orders/validate")
async def validate_order_only(order: CreateOrderRequest):
    """
    Validate an order body without persisting it.

    Useful for client-side pre-validation.
    """
    total = round(sum(item.subtotal for item in order.items), 2)
    discount = round(total * COUPONS.get(order.coupon_code or "", 0), 2)
    return {
        "valid": True,
        "item_count": len(order.items),
        "subtotal": total,
        "discount": discount,
        "estimated_total": round(total - discount, 2),
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 60)
    print("REQUEST BODY — DEMO")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  POST /orders          — create order (full body)")
    print("  GET  /orders/{id}     — fetch order")
    print("  PATCH /orders/{id}    — partial update (address, notes)")
    print("  POST /orders/validate — validate without saving")
    print()
    print("Key features demonstrated:")
    print("  • Nested Pydantic models (Address inside CreateOrderRequest)")
    print("  • List fields with min_length constraint")
    print("  • Cross-field validator (no duplicate product IDs)")
    print("  • PATCH with Optional fields and exclude_unset=True")
    print("  • Coupon discount calculation from body field")
    print()
    print("Start server: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    demo()
