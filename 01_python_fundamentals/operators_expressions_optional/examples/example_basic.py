"""Working example of operators and expressions."""


def calculate_total(subtotal: float, tax_rate: float, discount: float) -> float:
    """Apply arithmetic operators to compute a final total."""
    taxed = subtotal * (1 + tax_rate)
    return round(taxed - discount, 2)


def shipping_label(total: float, is_member: bool) -> str:
    """Use boolean and conditional expressions to decide shipping."""
    free_shipping = total >= 50 or is_member
    return "free shipping" if free_shipping else "standard shipping"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    total = calculate_total(48.0, 0.21, 5.0)
    print(f"Final total: {total}")
    print(f"Label: {shipping_label(total, is_member=False)}")
    print(f"7 in [3, 5, 7]: {7 in [3, 5, 7]}")
    print(f"2 ** 5 = {2**5}")


if __name__ == "__main__":
    main()
