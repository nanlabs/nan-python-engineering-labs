"""A tiny domain model that maps naturally to Given/When/Then scenarios."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ShoppingCart:
    items: list[tuple[str, float]] = field(default_factory=list)

    def add_item(self, name: str, price: float) -> None:
        self.items.append((name, price))

    def total(self) -> float:
        return round(sum(price for _, price in self.items), 2)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Book", 12.5)
    cart.add_item("Pen", 1.2)
    print("bdd behave example")
    print(f"cart total: {cart.total()}")
