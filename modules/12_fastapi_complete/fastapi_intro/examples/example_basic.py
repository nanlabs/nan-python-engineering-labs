"""
Basic example: Introduction to FastAPI
=======================================

FastAPI is a modern, high-performance web framework for building APIs
with Python 3.7+ based on standard type hints.

This example demonstrates:
1. Creating a FastAPI application
2. Defining routes with different HTTP methods
3. Path parameters and query parameters
4. Request body with Pydantic models
5. Responses with status codes
6. Automatic documentation

Installation:
    pip install fastapi uvicorn[standard] pydantic[email]

Run the server:
    uvicorn example_basic:app --reload

Then visit:
    - http://localhost:8000/docs   (Swagger UI)
    - http://localhost:8000/redoc  (ReDoc)
"""

from datetime import datetime
from enum import Enum

from fastapi import Body, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

# =============================================================================
# CREATE FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title="My First FastAPI",
    description="Example API for learning FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# =============================================================================
# PYDANTIC MODELS (Request / Response)
# =============================================================================


class ItemCategory(str, Enum):
    """Item categories (Enum)."""

    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"


class Item(BaseModel):
    """Model for an item."""

    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be > 0)")
    category: ItemCategory = Field(..., description="Item category")
    in_stock: bool = Field(True, description="Whether the item is in stock")
    tags: list[str] = Field(default_factory=list, description="Item tags")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "HP Laptop",
                "description": "15-inch laptop with 16 GB RAM",
                "price": 799.99,
                "category": "electronics",
                "in_stock": True,
                "tags": ["computer", "technology"],
            }
        }
    }


class ItemResponse(BaseModel):
    """Response schema for creating/fetching an item."""

    id: int
    item: Item
    created_at: datetime


# =============================================================================
# IN-MEMORY DATABASE
# =============================================================================

items_db: dict[int, ItemResponse] = {}
next_item_id = 1


# =============================================================================
# ROUTES — GET
# =============================================================================


@app.get("/")
async def root():
    """Root endpoint — welcome message."""
    return {
        "message": "Welcome to FastAPI!",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/items", response_model=list[ItemResponse])
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    category: ItemCategory | None = Query(None, description="Filter by category"),
    in_stock: bool | None = Query(None, description="Filter by availability"),
):
    """Return a paginated, optionally filtered list of items."""
    items = list(items_db.values())
    if category is not None:
        items = [i for i in items if i.item.category == category]
    if in_stock is not None:
        items = [i for i in items if i.item.in_stock == in_stock]
    return items[skip : skip + limit]


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int = Path(..., ge=1, description="ID of the item to fetch"),
):
    """Fetch a single item by ID."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return items_db[item_id]


# =============================================================================
# ROUTES — POST
# =============================================================================


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """Create a new item."""
    global next_item_id
    item_response = ItemResponse(
        id=next_item_id,
        item=item,
        created_at=datetime.now(),
    )
    items_db[next_item_id] = item_response
    next_item_id += 1
    return item_response


# =============================================================================
# ROUTES — PUT / PATCH
# =============================================================================


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int = Path(..., ge=1),
    item: Item = Body(...),
):
    """Fully replace an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    items_db[item_id].item = item
    return items_db[item_id]


@app.patch("/items/{item_id}/stock", response_model=ItemResponse)
async def update_item_stock(
    item_id: int = Path(..., ge=1),
    in_stock: bool = Body(..., embed=True),
):
    """Update only the stock availability of an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    items_db[item_id].item.in_stock = in_stock
    return items_db[item_id]


# =============================================================================
# ROUTES — DELETE
# =============================================================================


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int = Path(..., ge=1)):
    """Delete an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del items_db[item_id]


# =============================================================================
# STATS
# =============================================================================


@app.get("/stats")
async def get_stats():
    """Return a summary of current inventory data."""
    return {
        "total_items": len(items_db),
        "items_by_category": {
            category.value: sum(1 for i in items_db.values() if i.item.category == category)
            for category in ItemCategory
        },
        "in_stock": sum(1 for i in items_db.values() if i.item.in_stock),
        "out_of_stock": sum(1 for i in items_db.values() if not i.item.in_stock),
    }


# =============================================================================
# MAIN — run as script to see setup instructions
# =============================================================================


def print_instructions() -> None:
    print("=" * 70)
    print("FASTAPI — BASIC EXAMPLE")
    print("=" * 70)
    print("\nInstall dependencies:")
    print("    pip install fastapi uvicorn[standard] pydantic[email]")
    print("\nStart the server:")
    print("    uvicorn example_basic:app --reload")
    print("\nKey URLs:")
    print("    API root : http://localhost:8000")
    print("    Swagger  : http://localhost:8000/docs")
    print("    ReDoc    : http://localhost:8000/redoc")
    print("\nAvailable endpoints:")
    print("    GET    /                  — welcome message")
    print("    GET    /health            — health check")
    print("    GET    /items             — list items (paginated, filterable)")
    print("    GET    /items/{id}        — fetch single item")
    print("    POST   /items             — create item")
    print("    PUT    /items/{id}        — replace item")
    print("    PATCH  /items/{id}/stock  — update stock flag")
    print("    DELETE /items/{id}        — delete item")
    print("    GET    /stats             — inventory summary")
    print("\nExample curl request:")
    print(
        """
    curl -X POST "http://localhost:8000/items" \\
         -H "Content-Type: application/json" \\
         -d '{
             "name": "HP Laptop",
             "description": "15-inch laptop",
             "price": 799.99,
             "category": "electronics",
             "in_stock": true,
             "tags": ["computer"]
         }'
    """
    )
    print("=" * 70)


if __name__ == "__main__":
    print_instructions()
