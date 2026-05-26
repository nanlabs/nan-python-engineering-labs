"""Strategy pattern example: swap shipping algorithms at runtime."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ShippingStrategy(ABC):
    @abstractmethod
    def cost(self, weight_kg: float, distance_km: float) -> float:
        ...


class StandardShipping(ShippingStrategy):
    def cost(self, weight_kg: float, distance_km: float) -> float:
        return 5.0 + 0.6 * weight_kg + 0.02 * distance_km


class ExpressShipping(ShippingStrategy):
    def cost(self, weight_kg: float, distance_km: float) -> float:
        return 12.0 + 0.9 * weight_kg + 0.05 * distance_km


class InStorePickup(ShippingStrategy):
    def cost(self, weight_kg: float, distance_km: float) -> float:
        return 0.0


class ShippingCalculator:
    def __init__(self, strategy: ShippingStrategy) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy) -> None:
        self.strategy = strategy

    def quote(self, weight_kg: float, distance_km: float) -> float:
        return self.strategy.cost(weight_kg, distance_km)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    calculator = ShippingCalculator(StandardShipping())
    weight, distance = 8.5, 350
    print(f"Standard: ${calculator.quote(weight, distance):.2f}")
    calculator.set_strategy(ExpressShipping())
    print(f"Express : ${calculator.quote(weight, distance):.2f}")
    calculator.set_strategy(InStorePickup())
    print(f"Pickup  : ${calculator.quote(weight, distance):.2f}")


if __name__ == "__main__":
    main()
