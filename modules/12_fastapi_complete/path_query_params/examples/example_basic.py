"""
Basic example: Path and Query Parameters
=========================================

FastAPI provides rich, validated path and query parameter handling
directly from function signatures using Python type hints.

This example demonstrates:
1. Path parameters with type coercion and constraints
2. Query parameters with defaults and validation
3. Optional query parameters
4. Enum-based path/query parameters
5. Multiple parameter types in one endpoint

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

import math
from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query

# =============================================================================
# ENUMS
# =============================================================================


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    FOOD = "food"


# =============================================================================
# SAMPLE DATA
# =============================================================================

PRODUCTS = [
    {
        "id": i,
        "name": f"Product {i}",
        "price": round(10 + i * 7.5, 2),
        "category": list(ProductCategory)[i % 4].value,
        "rating": round(3 + (i % 3) * 0.5, 1),
    }
    for i in range(1, 21)
]


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Path and Query Params Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Path & Query Params Demo", "docs": "/docs"}


# ── Path parameters ──────────────────────────────────────────────────────────


@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(
        ...,
        ge=1,
        le=1000,
        title="Product ID",
        description="Unique identifier for the product",
    ),
):
    """
    Fetch a product by its ID.

    - Path parameter `product_id` must be an integer between 1 and 1000.
    - FastAPI validates and converts the string from the URL automatically.
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.get("/categories/{category}/products")
async def get_products_by_category(
    category: ProductCategory = Path(..., description="Product category"),
    min_rating: float = Query(0.0, ge=0.0, le=5.0, description="Minimum rating filter"),
):
    """
    Fetch products by category with an optional minimum rating filter.

    - `category` is validated against the ProductCategory enum.
    - `min_rating` is a query parameter with a default of 0.0.
    """
    results = [p for p in PRODUCTS if p["category"] == category.value and p["rating"] >= min_rating]
    return {
        "category": category.value,
        "min_rating": min_rating,
        "count": len(results),
        "products": results,
    }


# ── Query parameters ─────────────────────────────────────────────────────────


@app.get("/products")
async def list_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(5, ge=1, le=20, description="Max number of products to return"),
    sort_by: str = Query("id", pattern="^(id|price|rating)$", description="Sort field"),
    order: SortOrder = Query(SortOrder.ASC, description="Sort direction"),
    min_price: float | None = Query(None, ge=0, description="Minimum price filter"),
    max_price: float | None = Query(None, ge=0, description="Maximum price filter"),
    q: str | None = Query(None, min_length=1, max_length=50, description="Search query"),
):
    """
    List products with full pagination, sorting, and filtering.

    All parameters are query params — they come after `?` in the URL.
    FastAPI validates types and constraints automatically.

    Example: /products?skip=0&limit=5&sort_by=price&order=desc&min_price=20
    """
    results = list(PRODUCTS)

    # Search filter
    if q:
        results = [p for p in results if q.lower() in p["name"].lower()]

    # Price range filters
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

    # Sort
    reverse = order == SortOrder.DESC
    results.sort(key=lambda p: p[sort_by], reverse=reverse)

    # Pagination
    total = len(results)
    page_results = results[skip : skip + limit]
    total_pages = math.ceil(total / limit) if limit else 1

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "page": (skip // limit) + 1,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "order": order.value,
        "results": page_results,
    }


@app.get("/products/{product_id}/related")
async def get_related_products(
    product_id: int = Path(..., ge=1),
    max_results: int = Query(3, ge=1, le=10, description="Number of related products"),
    same_category: bool = Query(True, description="Only return same-category products"),
):
    """
    Find products related to a given product.

    Combines a path param (product_id) with query params (max_results, same_category).
    """
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    candidates = [p for p in PRODUCTS if p["id"] != product_id]
    if same_category:
        candidates = [p for p in candidates if p["category"] == product["category"]]

    # Sort by price proximity
    candidates.sort(key=lambda p: abs(p["price"] - product["price"]))
    return {
        "product_id": product_id,
        "related": candidates[:max_results],
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 60)
    print("PATH & QUERY PARAMS — DEMO")
    print("=" * 60)
    print()
    print("Path parameter examples:")
    print("  GET /products/5              — fetch product ID 5")
    print("  GET /categories/books/products — all books")
    print("  GET /categories/electronics/products?min_rating=4.0")
    print()
    print("Query parameter examples:")
    print("  GET /products                — first 5 products")
    print("  GET /products?skip=10&limit=5&sort_by=price&order=desc")
    print("  GET /products?min_price=50&max_price=100&q=product")
    print()
    print("Combined path + query:")
    print("  GET /products/3/related?max_results=5&same_category=false")
    print()
    print("Start server: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    demo()
