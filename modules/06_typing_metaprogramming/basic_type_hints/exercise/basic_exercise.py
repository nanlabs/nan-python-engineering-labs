"""
Basic Exercise: Type Hints - Product Discounts

OBJECTIVE:
Create a function that calculates the final price of a product
after applying a percentage discount.

REQUIREMENTS:
1. Function calculate_discount must accept:
   - price: float (original price)
   - discount_percent: float (discount percentage 0-100)
2. Return the final price as a float
3. Validate that discount_percent is between 0 and 100
4. If the discount is invalid, return the original price
5. ALL parameters and the return value must have type hints

USAGE EXAMPLE:
>>> calculate_discount(100.0, 20.0)
80.0
>>> calculate_discount(50.0, 150.0)  # Invalid discount
50.0
"""


def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate the final price after applying a discount.

    Args:
        price: Original product price (must be positive)
        discount_percent: Discount percentage to apply (0-100)

    Returns:
        The final price after the discount.
        If the discount is invalid (<0 or >100), return the original price.

    Examples:
        >>> calculate_discount(100.0, 20.0)
        80.0
        >>> calculate_discount(150.0, 10.0)
        135.0
        >>> calculate_discount(50.0, -5.0)
        50.0
    """
    # TODO: Implement validation and calculation logic
    # 1. Validate that discount_percent is between 0 and 100
    # 2. If valid, calculate: price - (price * discount_percent / 100)
    # 3. If invalid, return price unchanged
    pass


if __name__ == "__main__":
    # Manual tests - uncomment to test your implementation
    # print(calculate_discount(100.0, 20.0))  # Expected: 80.0
    # print(calculate_discount(50.0, 50.0))   # Expected: 25.0
    # print(calculate_discount(200.0, 15.0))  # Expected: 170.0
    # print(calculate_discount(100.0, 110.0)) # Expected: 100.0 (invalid)
    # print(calculate_discount(100.0, -10.0)) # Expected: 100.0 (invalid)
    pass
