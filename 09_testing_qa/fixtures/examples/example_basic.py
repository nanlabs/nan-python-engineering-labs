"""Show how fixtures centralize setup for stateful collaborators."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class InventoryService:
    stock: dict[str, int] = field(default_factory=dict)

    def reserve(self, sku: str, quantity: int) -> int:
        available = self.stock.get(sku, 0)
        if quantity > available:
            raise ValueError("not enough stock")
        self.stock[sku] = available - quantity
        return self.stock[sku]


def inventory_fixture() -> InventoryService:
    return InventoryService(stock={"keyboard": 4, "mouse": 10})


if __name__ == "__main__":
    service = inventory_fixture()
    print("fixtures example")
    print(f"initial stock: {service.stock}")
    remaining = service.reserve("keyboard", 1)
    print(f"remaining keyboards after reservation: {remaining}")
