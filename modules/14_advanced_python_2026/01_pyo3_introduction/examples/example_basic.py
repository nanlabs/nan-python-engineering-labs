"""
Basic PyO3 module that creates a simple Python-callable Rust function.
Demonstrates the minimal setup for Rust-Python interop.
"""


def greet_from_rust(name: str) -> str:
    """Mock function simulating Rust integration."""
    return f"Hello, {name}! This is from Rust via PyO3."


def calculate_sum(values: list) -> int:
    """Sum a list of integers (simulates Rust computation)."""
    return sum(values)


if __name__ == "__main__":
    result = greet_from_rust("Python")
    print(result)
    print(f"Sum: {calculate_sum([1, 2, 3, 4, 5])}")
