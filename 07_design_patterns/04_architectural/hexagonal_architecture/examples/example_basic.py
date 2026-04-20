"""Hexagonal Architecture example: domain logic isolated behind ports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class Order:
    order_id: str
    customer: str
    amount: float
    created_at: datetime


class OrderRepositoryPort(Protocol):
    def save(self, order: Order) -> None:
        ...

    def list_all(self) -> list[Order]:
        ...


class InMemoryOrderRepository(OrderRepositoryPort):
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def save(self, order: Order) -> None:
        self._orders.append(order)

    def list_all(self) -> list[Order]:
        return list(self._orders)


class OrderService:
    def __init__(self, repository: OrderRepositoryPort) -> None:
        self.repository = repository

    def create_order(self, order_id: str, customer: str, amount: float) -> Order:
        order = Order(order_id, customer, amount, datetime.utcnow())
        self.repository.save(order)
        return order

    def total_revenue(self) -> float:
        return sum(o.amount for o in self.repository.list_all())


def main() -> None:
    """Entry point to demonstrate the implementation."""
    repo = InMemoryOrderRepository()
    service = OrderService(repo)
    service.create_order("ORD-100", "Alice", 149.90)
    service.create_order("ORD-101", "Bob", 89.50)
    for order in repo.list_all():
        print(f"{order.order_id} | {order.customer} | ${order.amount:.2f}")
    print(f"Total revenue: ${service.total_revenue():.2f}")


if __name__ == "__main__":
    main()
