"""
Basic example: Response Models
================================

FastAPI's `response_model` parameter controls what is serialized and returned
to the client — regardless of what the route function actually returns.

This example demonstrates:
1. response_model filters sensitive fields (e.g., password hashes)
2. response_model_exclude_unset — only return fields that were explicitly set
3. Different response models per HTTP status code
4. Union response models
5. Generic response wrappers

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Generic, TypeVar
from datetime import datetime


# =============================================================================
# MODELS
# =============================================================================

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic wrapper for paginated list responses."""

    total: int
    page: int
    per_page: int
    items: List[T]


# ── User models — demonstrating field filtering ──────────────────────────────


class UserInDB(BaseModel):
    """Internal model — contains all fields including sensitive ones."""

    id: int
    username: str
    email: str
    hashed_password: str  # NEVER returned to clients
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class UserPublic(BaseModel):
    """Public response model — no sensitive data."""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


class UserAdmin(UserPublic):
    """Extended response for admin consumers — adds is_admin flag."""

    is_admin: bool


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=8)


# ── Item models ──────────────────────────────────────────────────────────────


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    in_stock: bool = True


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    @computed_field
    @property
    def price_with_tax(self) -> float:
        return round(self.price * 1.21, 2)


# ── Error models ─────────────────────────────────────────────────────────────


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.now)


class SuccessMessage(BaseModel):
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


# =============================================================================
# IN-MEMORY STORES
# =============================================================================

users_db: dict[int, UserInDB] = {}
items_db: dict[int, ItemResponse] = {}
_user_counter = 1
_item_counter = 1


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Response Models Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Response Models Demo", "docs": "/docs"}


# ── User endpoints with field filtering ───────────────────────────────────────


@app.post(
    "/users",
    response_model=UserPublic,           # hashed_password is NOT in UserPublic → filtered out
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Username already exists"},
    },
)
async def create_user(payload: UserCreateRequest):
    """
    Create a user.

    The function stores `hashed_password` internally, but the response
    only contains the fields defined in `UserPublic` (no password).
    """
    global _user_counter
    if any(u.username == payload.username for u in users_db.values()):
        raise HTTPException(
            status_code=400,
            detail={"code": "DUPLICATE_USERNAME", "message": "Username already exists"},
        )
    user = UserInDB(
        id=_user_counter,
        username=payload.username,
        email=payload.email,
        hashed_password=f"hashed:{payload.password}",  # simplified hash
    )
    users_db[_user_counter] = user
    _user_counter += 1
    return user  # FastAPI filters this through UserPublic automatically


@app.get("/users", response_model=PaginatedResponse[UserPublic])
async def list_users(skip: int = 0, limit: int = 10):
    """Return a paginated list of users (no passwords in response)."""
    all_users = list(users_db.values())
    page_users = all_users[skip : skip + limit]
    return PaginatedResponse(
        total=len(all_users),
        page=(skip // limit) + 1 if limit else 1,
        per_page=limit,
        items=page_users,
    )


@app.get(
    "/users/{user_id}",
    response_model=UserPublic,
    responses={404: {"model": ErrorResponse}},
)
async def get_user(user_id: int):
    """Fetch a user. Returns UserPublic (no password) or 404 ErrorResponse."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.get("/admin/users/{user_id}", response_model=UserAdmin)
async def get_user_admin(user_id: int):
    """Admin view — same user but includes the is_admin flag (UserAdmin model)."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


# ── Item endpoints ────────────────────────────────────────────────────────────


@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(payload: ItemCreate):
    """Create an item. Response includes computed `price_with_tax`."""
    global _item_counter
    item = ItemResponse(id=_item_counter, created_at=datetime.now(), **payload.model_dump())
    items_db[_item_counter] = item
    _item_counter += 1
    return item


@app.get("/items", response_model=List[ItemResponse])
async def list_items():
    """List all items — each includes the computed tax field."""
    return list(items_db.values())


@app.delete(
    "/users/{user_id}",
    response_model=SuccessMessage,
    responses={404: {"model": ErrorResponse}},
)
async def delete_user(user_id: int):
    """Delete a user — returns a SuccessMessage on success, ErrorResponse on 404."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return SuccessMessage(message=f"User {user_id} deleted successfully")


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("RESPONSE MODELS — DEMO")
    print("=" * 65)
    print()
    print("Key concepts demonstrated:")
    print()
    print("  1. Field filtering via response_model")
    print("     UserInDB has hashed_password")
    print("     UserPublic does NOT — FastAPI strips it automatically")
    print()
    print("  2. Different models per status code")
    print("     POST /users  → 201 UserPublic | 400 ErrorResponse")
    print("     GET /users/{id} → 200 UserPublic | 404 ErrorResponse")
    print()
    print("  3. Computed fields in response")
    print("     ItemResponse.price_with_tax adds 21% VAT automatically")
    print()
    print("  4. Generic paginated wrapper")
    print("     GET /users → PaginatedResponse[UserPublic]")
    print()
    print("  5. Extended model for admin view")
    print("     GET /admin/users/{id} → UserAdmin (adds is_admin field)")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("Docs : http://localhost:8000/docs")
    print("=" * 65)


if __name__ == "__main__":
    demo()
