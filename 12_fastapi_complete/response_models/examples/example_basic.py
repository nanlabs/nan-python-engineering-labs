"""Show response-model style validation and serialization using dataclasses."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime


@dataclass
class ItemResponse:
    """Represents an API response model for an item."""

    item_id: int
    name: str
    price: float
    in_stock: bool
    created_at: str

    @classmethod
    def from_payload(cls, payload: dict) -> ItemResponse:
        if payload.get("price", 0) < 0:
            raise ValueError("price must be non-negative")
        if not payload.get("name"):
            raise ValueError("name is required")

        timestamp = datetime.now(tz=UTC).isoformat()
        return cls(
            item_id=int(payload["item_id"]),
            name=str(payload["name"]).strip(),
            price=float(payload["price"]),
            in_stock=bool(payload.get("in_stock", True)),
            created_at=timestamp,
        )


def main() -> None:
    """Entry point to demonstrate the implementation."""
    raw_payload = {
        "item_id": "101",
        "name": "Mechanical Keyboard",
        "price": 129.99,
        "in_stock": 1,
    }

    model = ItemResponse.from_payload(raw_payload)
    response_json = json.dumps(asdict(model), indent=2, sort_keys=True)

    print("Validated response model:")
    print(response_json)


if __name__ == "__main__":
    main()
