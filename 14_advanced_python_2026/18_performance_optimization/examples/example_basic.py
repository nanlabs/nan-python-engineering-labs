"""
Performance optimization techniques in PyO3.
Benchmarking Rust vs Python implementations.
"""

def python_implementation(n: int) -> int:
    """Pure Python sum (for comparison)."""
    return sum(range(n))

def optimized_implementation(n: int) -> int:
    """Optimized version (simulates Rust efficiency)."""
    # This would be Rust in real scenario
    return n * (n - 1) // 2

def benchmark_comparison(n: int) -> dict:
    """Compare performance."""
    return {
        "python_result": python_implementation(n),
        "optimized_result": optimized_implementation(n),
        "input_size": n,
    }

if __name__ == "__main__":
    print(benchmark_comparison(1000000))
