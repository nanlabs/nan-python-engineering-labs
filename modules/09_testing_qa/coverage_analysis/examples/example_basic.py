"""Highlight why coverage reports should drive better questions."""

from __future__ import annotations


def shipping_cost(subtotal: float, expedited: bool) -> float:
    if subtotal >= 100:
        return 0.0
    if expedited:
        return 12.0
    return 5.0


def final_amount(subtotal: float, loyalty_tier: str, expedited: bool) -> float:
    discount_rate = {"silver": 0.05, "gold": 0.10}.get(loyalty_tier, 0.0)
    discounted = subtotal * (1 - discount_rate)
    return round(discounted + shipping_cost(discounted, expedited), 2)


if __name__ == "__main__":
    print("coverage analysis example")
    for tier in ["standard", "silver", "gold"]:
        print(tier, final_amount(80, tier, expedited=False))
