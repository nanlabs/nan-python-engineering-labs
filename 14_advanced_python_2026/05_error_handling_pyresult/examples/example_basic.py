"""
Error handling in PyO3 using PyResult.
Demonstrates try-catch patterns and Rust error propagation.
"""

def divide(a: float, b: float) -> float:
    """Divide with error handling."""
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def parse_integer(s: str) -> int:
    """Parse string to integer with error handling."""
    try:
        return int(s)
    except ValueError as e:
        raise ValueError(f"Could not parse '{s}' as integer: {e}")

if __name__ == "__main__":
    print("Divide:", divide(10, 2))
    try:
        print("Divide by zero:", divide(10, 0))
    except ValueError as e:
        print(f"Error caught: {e}")
