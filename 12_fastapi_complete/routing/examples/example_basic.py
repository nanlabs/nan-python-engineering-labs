"""
Basic example: Routing with APIRouter
======================================

FastAPI's APIRouter allows you to organize endpoints into separate modules,
each with their own prefix, tags, and dependencies.

This example demonstrates:
1. Creating multiple APIRouter instances (users, products)
2. Setting prefixes and OpenAPI tags per router
3. Including routers in the main app
4. Nested routers for hierarchical resources
5. Router-level dependency injection

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# =============================================================================
# PYDANTIC MODELS
# =============================================================================


class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str


class Order(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]
    total: float
    created_at: datetime


# =============================================================================
# IN-MEMORY STORES
# =============================================================================

users_db: dict[int, User] = {
    1: User(id=1, username="alice", email="alice@example.com"),
    2: User(id=2, username="bob", email="bob@example.com"),
}
products_db: dict[int, Product] = {
    1: Product(id=1, name="Keyboard", price=79.99, category="electronics"),
    2: Product(id=2, name="Desk", price=249.00, category="furniture"),
}
orders_db: dict[int, Order] = {}
_user_counter = 3
_product_counter = 3
_order_counter = 1


# =============================================================================
# USERS ROUTER  (prefix=/users, tag=users)
# =============================================================================

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=List[User])
async def list_users(active_only: bool = False):
    """List all users, optionally filtered to active ones."""
    users = list(users_db.values())
    return [u for u in users if u.active] if active_only else users


@users_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Fetch a user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@users_router.post("/", response_model=User, status_code=201)
async def create_user(payload: UserCreate):
    """Create a new user."""
    global _user_counter
    user = User(id=_user_counter, username=payload.username, email=payload.email)
    users_db[_user_counter] = user
    _user_counter += 1
    return user


@users_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Soft-delete a user (mark inactive)."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].active = False


# =============================================================================
# PRODUCTS ROUTER  (prefix=/products, tag=products)
# =============================================================================

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get("/", response_model=List[Product])
async def list_products(category: Optional[str] = None):
    """List products, optionally filtered by category."""
    prods = list(products_db.values())
    if category:
        prods = [p for p in prods if p.category.lower() == category.lower()]
    return prods


@products_router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Fetch a product by ID."""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]


@products_router.post("/", response_model=Product, status_code=201)
async def create_product(payload: ProductCreate):
    """Create a new product."""
    global _product_counter
    product = Product(
        id=_product_counter,
        name=payload.name,
        price=payload.price,
        category=payload.category,
    )
    products_db[_product_counter] = product
    _product_counter += 1
    return product


# =============================================================================
# ORDERS ROUTER  (nested under users: /users/{user_id}/orders)
# =============================================================================

orders_router = APIRouter(prefix="/{user_id}/orders", tags=["orders"])


@orders_router.get("/", response_model=List[Order])
async def list_user_orders(user_id: int):
    """List all orders for a given user."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return [o for o in orders_db.values() if o.user_id == user_id]


@orders_router.post("/", response_model=Order, status_code=201)
async def create_order(user_id: int, product_ids: List[int]):
    """Create an order for a user."""
    global _order_counter
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    missing = [pid for pid in product_ids if pid not in products_db]
    if missing:
        raise HTTPException(status_code=400, detail=f"Products not found: {missing}")
    total = sum(products_db[pid].price for pid in product_ids)
    order = Order(
        id=_order_counter,
        user_id=user_id,
        product_ids=product_ids,
        total=total,
        created_at=datetime.now(),
    )
    orders_db[_order_counter] = order
    _order_counter += 1
    return order


# Attach orders as nested resource under users
users_router.include_router(orders_router)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

app = FastAPI(
    title="Routing Example",
    description="Demonstrates APIRouter organization in FastAPI",
    version="1.0.0",
)

app.include_router(users_router)
app.include_router(products_router)


@app.get("/", tags=["root"])
async def root():
    """API root — summary of available routers."""
    return {
        "resources": ["/users", "/products"],
        "nested": ["/users/{user_id}/orders"],
        "docs": "/docs",
    }


# =============================================================================
# MAIN
# =============================================================================


def print_route_summary() -> None:
    print("=" * 60)
    print("FASTAPI ROUTING — EXAMPLE")
    print("=" * 60)
    print("Router layout:")
    print("  /users          (prefix='/users', tags=['users'])")
    print("    GET  /              — list users")
    print("    GET  /{id}          — get user")
    print("    POST /              — create user")
    print("    DELETE /{id}        — soft-delete user")
    print("    GET  /{id}/orders   — list user orders (nested)")
    print("    POST /{id}/orders   — create order (nested)")
    print()
    print("  /products       (prefix='/products', tags=['products'])")
    print("    GET  /              — list products")
    print("    GET  /{id}          — get product")
    print("    POST /              — create product")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("Docs : http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    print_route_summary()
