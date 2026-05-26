"""
Basic example: Pydantic Models
================================

Pydantic v2 is FastAPI's validation engine. It converts raw data into typed
Python objects and raises clear errors when input doesn't match the schema.

This example runs STANDALONE — no HTTP server needed.
Execute: python example_basic.py

Demonstrates:
1. Basic model with field constraints
2. Optional and default values
3. Custom validators (field_validator, model_validator)
4. Computed fields
5. Model inheritance
6. Nested models
7. Serialization options (exclude_unset, by_alias)
8. From ORM objects (model_validate)
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

# =============================================================================
# 1. BASIC MODEL WITH FIELD CONSTRAINTS
# =============================================================================


class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class User(BaseModel):
    """Basic user model with type coercion and validation."""

    id: int = Field(..., ge=1, description="Positive integer user ID")
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(..., description="Must contain @")
    role: UserRole = Field(UserRole.VIEWER, description="User permission level")
    age: int | None = Field(None, ge=0, le=150)
    tags: list[str] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email: must contain @")
        return v.lower().strip()

    @field_validator("tags", mode="before")
    @classmethod
    def deduplicate_tags(cls, v: list) -> list:
        """Remove duplicate tags while preserving order."""
        seen = set()
        return [tag for tag in v if not (tag in seen or seen.add(tag))]


# =============================================================================
# 2. CROSS-FIELD VALIDATION WITH model_validator
# =============================================================================


class DateRange(BaseModel):
    """Date range with cross-field validation."""

    start: date
    end: date
    label: str | None = None

    @model_validator(mode="after")
    def check_dates(self) -> "DateRange":
        if self.end < self.start:
            raise ValueError(f"'end' ({self.end}) must be >= 'start' ({self.start})")
        return self


# =============================================================================
# 3. COMPUTED FIELDS
# =============================================================================


class Product(BaseModel):
    """Product with a computed price-after-discount field."""

    name: str
    unit_price: Decimal = Field(..., decimal_places=2, gt=0)
    quantity: int = Field(..., ge=0)
    discount_percent: float = Field(0.0, ge=0.0, le=100.0)

    @computed_field
    @property
    def total_price(self) -> Decimal:
        discount_factor = Decimal(str(1 - self.discount_percent / 100))
        return (self.unit_price * self.quantity * discount_factor).quantize(Decimal("0.01"))

    @computed_field
    @property
    def in_stock(self) -> bool:
        return self.quantity > 0


# =============================================================================
# 4. MODEL INHERITANCE
# =============================================================================


class BaseItem(BaseModel):
    """Shared fields for all item types."""

    name: str = Field(..., min_length=1)
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class PhysicalItem(BaseItem):
    """Extends BaseItem with physical properties."""

    weight_kg: float = Field(..., gt=0)
    dimensions_cm: tuple[float, float, float]  # (L, W, H)

    @computed_field
    @property
    def volume_cm3(self) -> float:
        l, w, h = self.dimensions_cm
        return round(l * w * h, 2)


class DigitalItem(BaseItem):
    """Extends BaseItem with digital properties."""

    file_size_mb: float = Field(..., gt=0)
    download_url: str
    license_type: str = "single-use"


# =============================================================================
# 5. NESTED MODELS + SERIALIZATION
# =============================================================================


class Address(BaseModel):
    street: str
    city: str
    country: str = Field(..., min_length=2, max_length=2)


class Customer(BaseModel):
    """Nested model example."""

    model_config = ConfigDict(populate_by_name=True)

    customer_id: int = Field(..., alias="id")
    full_name: str = Field(..., alias="name")
    address: Address
    email: str
    tags: list[str] = Field(default_factory=list)


# =============================================================================
# DEMO RUNNER
# =============================================================================


def demo():
    separator = "─" * 60

    print("=" * 60)
    print("PYDANTIC MODELS — STANDALONE DEMO")
    print("=" * 60)

    # ── 1. Basic model ──────────────────────────────────────────
    print(f"\n{separator}")
    print("1. BASIC MODEL — User")
    print(separator)

    user = User(
        id=1,
        username="alice_99",
        email="  Alice@Example.COM  ",
        role="admin",
        tags=["python", "fastapi", "python"],
    )
    print(f"  Parsed user : {user.model_dump()}")
    print(f"  Email normalized : {user.email}")
    print(f"  Tags deduplicated: {user.tags}")

    try:
        User(id=0, username="ab", email="not-an-email", role="unknown")
    except Exception as e:
        print(f"  Validation error (expected): {type(e).__name__}")

    # ── 2. Cross-field validation ───────────────────────────────
    print(f"\n{separator}")
    print("2. CROSS-FIELD VALIDATION — DateRange")
    print(separator)

    dr = DateRange(start=date(2025, 1, 1), end=date(2025, 12, 31), label="Full year")
    print(f"  Valid range  : {dr.start} → {dr.end}")

    try:
        DateRange(start=date(2025, 12, 31), end=date(2025, 1, 1))
    except Exception as e:
        print(f"  Invalid range (expected): {e}")

    # ── 3. Computed fields ──────────────────────────────────────
    print(f"\n{separator}")
    print("3. COMPUTED FIELDS — Product")
    print(separator)

    p = Product(name="Widget", unit_price="9.99", quantity=5, discount_percent=10)
    print(f"  Unit price   : ${p.unit_price}")
    print(f"  Quantity     : {p.quantity}")
    print(f"  Discount     : {p.discount_percent}%")
    print(f"  Total price  : ${p.total_price}  (computed)")
    print(f"  In stock     : {p.in_stock}  (computed)")

    # ── 4. Inheritance ──────────────────────────────────────────
    print(f"\n{separator}")
    print("4. MODEL INHERITANCE — PhysicalItem / DigitalItem")
    print(separator)

    book = PhysicalItem(name="Clean Code", weight_kg=0.45, dimensions_cm=(22.0, 15.0, 2.5))
    print(f"  Physical  : {book.name}  volume={book.volume_cm3} cm³  (computed)")

    ebook = DigitalItem(
        name="Clean Code PDF", file_size_mb=12.5, download_url="https://example.com/dl/1"
    )
    print(f"  Digital   : {ebook.name}  {ebook.file_size_mb} MB  license={ebook.license_type}")

    # ── 5. Nested models + serialization ────────────────────────
    print(f"\n{separator}")
    print("5. NESTED MODELS + SERIALIZATION")
    print(separator)

    raw = {
        "id": 42,
        "name": "Bob Builder",
        "email": "bob@example.com",
        "address": {"street": "7 Oak Ave", "city": "Portland", "country": "US"},
        "tags": ["vip"],
    }
    customer = Customer.model_validate(raw)
    print(f"  Customer     : {customer.full_name}  (id={customer.customer_id})")
    print(f"  City         : {customer.address.city}, {customer.address.country}")

    # Serialize with alias
    as_alias = customer.model_dump(by_alias=True)
    print(f"  Alias keys   : {list(as_alias.keys())}")

    # Partial serialization — only set fields
    partial_user = User(id=5, username="charlie", email="c@x.com")
    print(f"  exclude_unset: {partial_user.model_dump(exclude_unset=True)}")

    print(f"\n{'=' * 60}")
    print("All demos completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
