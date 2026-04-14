"""Working example of basic functions."""


def greet(name: str, role: str = "Developer") -> str:
    """Return a greeting with positional and optional parameters."""
    return f"Hello, {name}. Your current role is {role}."


def calculate_price(base: float, discount: float = 0.0, tax: float = 0.21) -> float:
    """Calculate a final price by encapsulating reusable logic."""
    return round(base * (1 - discount) * (1 + tax), 2)


def main() -> None:
    print(greet("Lin"))
    print(calculate_price(100.0, discount=0.1))


if __name__ == "__main__":
    main()
