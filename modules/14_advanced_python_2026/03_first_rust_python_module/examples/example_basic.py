"""
First complete Rust-Python module integration.
Demonstrates creating a module with Rust function exported to Python.
"""


def fibonacci(n: int) -> int:
    """Fibonacci sequence (simulating Rust computation)."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def create_module_info() -> dict:
    """Module metadata."""
    return {
        "name": "first_rust_python_module",
        "version": "0.1.0",
        "functions": ["fibonacci", "prime_check"],
    }


if __name__ == "__main__":
    print(f"Fibonacci(10) = {fibonacci(10)}")
    print("Module Info:", create_module_info())
