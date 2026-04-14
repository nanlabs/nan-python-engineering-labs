"""Mutation testing rewards precise assertions."""

from __future__ import annotations


def apply_tax(amount: float, tax_rate: float) -> float:
    return round(amount * (1 + tax_rate), 2)


def apply_discount(amount: float, discount_rate: float) -> float:
    return round(amount * (1 - discount_rate), 2)


def final_price(amount: float, tax_rate: float, discount_rate: float) -> float:
    discounted = apply_discount(amount, discount_rate)
    return apply_tax(discounted, tax_rate)


if __name__ == "__main__":
    print("mutation testing example")
    print(final_price(100, tax_rate=0.21, discount_rate=0.10))
