"""Demonstrate the essential pytest building blocks with plain Python code."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Calculator:
    """Small domain object used by the sample tests."""

    tax_rate: float = 0.21

    def total_with_tax(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        return round(amount * (1 + self.tax_rate), 2)


def should_raise_for_negative_amount() -> None:
    calculator = Calculator()
    try:
        calculator.total_with_tax(-1)
    except ValueError as error:
        print(f"expected failure: {error}")
    else:
        raise AssertionError("negative amount must fail")


def show_assert_style() -> None:
    calculator = Calculator(tax_rate=0.10)
    total = calculator.total_with_tax(100)
    assert total == 110.0
    print(f"assertion-ready value: {total}")


if __name__ == "__main__":
    print("pytest basics example")
    show_assert_style()
    should_raise_for_negative_amount()
