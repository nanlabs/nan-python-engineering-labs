"""
Basic example: OpenAPI Customization
=======================================

FastAPI auto-generates an OpenAPI schema from your code. You can
deeply customize it: add metadata, tags, descriptions, examples,
deprecation markers, and even override the raw schema.

This example demonstrates:
1. App-level metadata (title, description, contact, license, version)
2. Tag groups with descriptions
3. Per-route documentation: summary, description, response examples
4. Request body examples via model_config and openapi_extra
5. Deprecated endpoint marking
6. Custom OpenAPI schema hook

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs   (Swagger UI)
    Visit http://localhost:8000/redoc  (ReDoc UI)
    Visit http://localhost:8000/openapi.json
"""


from fastapi import Body, FastAPI, HTTPException, Path
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field

# =============================================================================
# MODELS WITH EMBEDDED EXAMPLES
# =============================================================================


class ProductCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Product display name",
        examples=["FastAPI Handbook"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in USD (must be positive)",
        examples=[29.99],
    )
    category: str = Field(
        default="general",
        description="Product category slug",
        examples=["books"],
    )
    in_stock: bool = Field(default=True, description="Whether the product is available")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "FastAPI Handbook",
                    "price": 29.99,
                    "category": "books",
                    "in_stock": True,
                }
            ]
        }
    }


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None


# =============================================================================
# TAG DEFINITIONS
# =============================================================================

TAGS_METADATA = [
    {
        "name": "Products",
        "description": (
            "Operations on the product catalog. Products can be listed, created, and archived."
        ),
        "externalDocs": {
            "description": "Product schema documentation",
            "url": "https://example.com/docs/products",
        },
    },
    {
        "name": "Health",
        "description": "Service health and readiness probes.",
    },
    {
        "name": "Legacy",
        "description": "**Deprecated endpoints.** Will be removed in v3.0.",
    },
]


# =============================================================================
# APP
# =============================================================================

app = FastAPI(
    title="Product Catalog API",
    version="2.1.0",
    summary="Manages product listings with full CRUD support.",
    description="""
## Product Catalog API

A REST API for managing products in an e-commerce platform.

### Features
- **CRUD** operations on products
- **OpenAPI** schema with rich examples and descriptions
- **Deprecated** endpoints clearly marked

### Authentication
All write endpoints require `Authorization: Bearer <token>`.
Read endpoints are public.

### Rate Limits
- Read: 1000 req/min per IP
- Write: 100 req/min per authenticated user
""",
    contact={
        "name": "API Support Team",
        "url": "https://example.com/support",
        "email": "api@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
)


# In-memory store
products: dict[int, ProductResponse] = {
    1: ProductResponse(id=1, name="FastAPI Handbook", price=29.99, category="books", in_stock=True),
    2: ProductResponse(
        id=2, name="Python Pro Bundle", price=49.99, category="courses", in_stock=True
    ),
}
_next_id = 3


# =============================================================================
# ROUTES
# =============================================================================


@app.get(
    "/health",
    tags=["Health"],
    summary="Liveness probe",
    description="Returns 200 if the service is running. Used by load balancers.",
    response_description="Service is healthy",
)
async def health():
    return {"status": "healthy"}


@app.get(
    "/products",
    tags=["Products"],
    summary="List all products",
    description=("Returns all products in the catalog. Filter by `category` or `in_stock` status."),
    response_model=list[ProductResponse],
    response_description="A list of products matching the filter criteria",
)
async def list_products(
    category: str | None = None,
    in_stock: bool | None = None,
):
    results = list(products.values())
    if category:
        results = [p for p in results if p.category == category]
    if in_stock is not None:
        results = [p for p in results if p.in_stock == in_stock]
    return results


@app.get(
    "/products/{product_id}",
    tags=["Products"],
    summary="Get a product by ID",
    response_model=ProductResponse,
    responses={
        200: {"description": "Product found"},
        404: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {"code": "NOT_FOUND", "message": "Product 42 does not exist"}
                }
            },
        },
    },
)
async def get_product(
    product_id: int = Path(..., description="Unique product identifier", ge=1, examples=[1]),
):
    if product_id not in products:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return products[product_id]


@app.post(
    "/products",
    tags=["Products"],
    summary="Create a product",
    description=(
        "Create a new product in the catalog. "
        "The `id` is auto-assigned and returned in the response."
    ),
    response_model=ProductResponse,
    status_code=201,
    response_description="The newly created product",
    responses={
        201: {
            "description": "Product created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "name": "FastAPI Handbook",
                        "price": 29.99,
                        "category": "books",
                        "in_stock": True,
                    }
                }
            },
        },
        422: {"description": "Validation error — check the request body"},
    },
)
async def create_product(
    product: ProductCreate = Body(..., openapi_extra={"x-internal-note": "Price must be > 0"}),
):
    global _next_id
    new_product = ProductResponse(id=_next_id, **product.model_dump())
    products[_next_id] = new_product
    _next_id += 1
    return new_product


@app.delete(
    "/products/{product_id}",
    tags=["Products"],
    summary="Delete a product",
    status_code=204,
    response_description="Product deleted successfully",
)
async def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]


@app.get(
    "/legacy/catalog",
    tags=["Legacy"],
    summary="[DEPRECATED] List products",
    description=(
        "**This endpoint is deprecated.** Use `GET /products` instead. Will be removed in v3.0."
    ),
    deprecated=True,
    response_model=list[ProductResponse],
)
async def legacy_catalog():
    return list(products.values())


# =============================================================================
# CUSTOM OPENAPI SCHEMA (optional override)
# =============================================================================


def custom_openapi():
    """
    Override the auto-generated schema to add custom extensions.

    x-logo: shown in ReDoc
    x-api-id: machine-readable API identifier
    """
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=TAGS_METADATA,
    )

    # Add custom extensions
    schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
    schema["info"]["x-api-id"] = "product-catalog-v2"

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi  # type: ignore[method-assign]


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("OPENAPI CUSTOMIZATION — DEMO")
    print("=" * 65)
    print()
    print("App metadata:")
    print(f"  Title:   {app.title}")
    print(f"  Version: {app.version}")
    print()
    print("Documentation UIs:")
    print("  Swagger UI: http://localhost:8000/docs")
    print("  ReDoc:      http://localhost:8000/redoc")
    print("  Raw schema: http://localhost:8000/openapi.json")
    print()
    print("Customizations applied:")
    print("  - Rich markdown description with sections")
    print("  - Contact + license info in schema")
    print("  - Tag groups with descriptions and external docs links")
    print("  - Per-route: summary, description, response examples")
    print("  - Request body examples via model_config and Field(examples=…)")
    print("  - Deprecated endpoint marker (GET /legacy/catalog)")
    print("  - Custom x-logo and x-api-id extensions in info block")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
