"""Factory Method example: create transport objects through creators."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def deliver(self, cargo: str) -> str:
        ...


class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Delivering {cargo} by road with a truck"


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Delivering {cargo} by sea with a ship"


class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        ...

    def plan_delivery(self, cargo: str) -> str:
        return self.create_transport().deliver(cargo)


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(RoadLogistics().plan_delivery("electronics"))
    print(SeaLogistics().plan_delivery("containers"))


if __name__ == "__main__":
    main()
