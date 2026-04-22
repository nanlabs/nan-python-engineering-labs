"""
Comprehensive comparison: Threading (GIL) vs Multiprocessing.

Demonstrates when to use each approach and the tradeoffs involved.
"""

import multiprocessing as mp
import os
import sys
import threading
import time
from collections.abc import Callable


def fibonacci(n: int) -> int:
    """Recursive Fibonacci calculation (CPU-intensive)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def heavy_computation(numbers: list[int]) -> list[int]:
    """Simulate heavy CPU-bound computation."""
    return [fibonacci(n) for n in numbers]


def benchmark_sequential(func: Callable, data_chunks: list[list[int]]) -> float:
    """Run a function sequentially."""
    start = time.perf_counter()
    results = [func(chunk) for chunk in data_chunks]
    end = time.perf_counter()
    # Results are not used here, but could be printed or returned if needed
    print(f"   Results: {results}")
    return end - start


def benchmark_threading(func: Callable, data_chunks: list[list[int]]) -> float:
    """Run a function with threading (affected by the GIL)."""
    start = time.perf_counter()

    results = []
    threads = []

    def worker(chunk, index):
        result = func(chunk)
        results.append((index, result))

    for i, chunk in enumerate(data_chunks):
        t = threading.Thread(target=worker, args=(chunk, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()
    return end - start


def benchmark_multiprocessing(func: Callable, data_chunks: list[list[int]]) -> float:
    """Run a function with multiprocessing (without the GIL)."""
    start = time.perf_counter()

    with mp.Pool(processes=len(data_chunks)) as pool:
        pool.map(func, data_chunks)

    end = time.perf_counter()
    return end - start


def main():
    """
    Comprehensive comparison of threading vs multiprocessing
    for CPU-bound tasks.
    """
    print("=" * 70)
    print("THREADING (GIL) VS MULTIPROCESSING")
    print("=" * 70)
    print(f"Python: {sys.version}")
    print(f"CPU cores: {mp.cpu_count()}")
    print(f"PID: {os.getpid()}")
    print("=" * 70)

    # Test data: calculate Fibonacci for these numbers
    # Split into chunks for parallelization
    test_numbers = [30, 31, 32, 33]
    num_workers = 4
    data_chunks = [[n] for n in test_numbers]

    print(f"\nTask: Calculate fibonacci({test_numbers})")
    print(f"Workers: {num_workers}")
    print("\n" + "-" * 70)

    # Benchmark 1: Sequential (baseline)
    print("\n1️⃣  SEQUENTIAL EXECUTION (Baseline)")
    print("-" * 70)
    time_seq = benchmark_sequential(heavy_computation, data_chunks)
    print(f"   Time: {time_seq:.4f}s")
    print("   Speedup: 1.00x (baseline)")

    # Benchmark 2: Threading
    print("\n2️⃣  THREADING (Affected by GIL)")
    print("-" * 70)
    time_threading = benchmark_threading(heavy_computation, data_chunks)
    speedup_threading = time_seq / time_threading
    print(f"   Time: {time_threading:.4f}s")
    print(f"   Speedup: {speedup_threading:.2f}x")

    if speedup_threading < 1.2:
        print("   ❌ No significant improvement - the GIL serializes execution")
    else:
        print("   ⚠️  Unexpected improvement - this may be system variability")

    # Benchmark 3: Multiprocessing
    print("\n3️⃣  MULTIPROCESSING (Without GIL)")
    print("-" * 70)
    time_mp = benchmark_multiprocessing(heavy_computation, data_chunks)
    speedup_mp = time_seq / time_mp
    print(f"   Time: {time_mp:.4f}s")
    print(f"   Speedup: {speedup_mp:.2f}x")

    if speedup_mp > 2.0:
        print("   ✅ Effective real parallelism")
    else:
        print("   ⚠️  Serialization/communication overhead")

    # Comparative analysis
    print("\n" + "=" * 70)
    print("COMPARATIVE ANALYSIS")
    print("=" * 70)

    print(
        f"""
    Sequential:        {time_seq:.4f}s (1.00x)
    Threading:         {time_threading:.4f}s ({speedup_threading:.2f}x)
    Multiprocessing:   {time_mp:.4f}s ({speedup_mp:.2f}x)

    Threading Efficiency:        {speedup_threading / num_workers * 100:.1f}%
    Multiprocessing Efficiency:  {speedup_mp / num_workers * 100:.1f}%

    🎯 RECOMMENDATION:
    """
    )

    if speedup_mp > speedup_threading * 1.5:
        print(
            """
    ✅ For this CPU-bound task, MULTIPROCESSING is clearly superior.

    The GIL prevents threading from using multiple cores.
    Multiprocessing creates separate processes, each with its own GIL.

    Trade-offs:
    • Multiprocessing: Higher memory overhead (full processes)
    • Multiprocessing: Data serialization (pickle)
    • Threading: Lower overhead, but no real parallelism for CPU-bound work
        """
        )
    else:
        print(
            """
    ⚠️  Results are similar. Consider:

    • Multiprocessing overhead can dominate small tasks
    • For large CPU-bound tasks, multiprocessing should win
    • For I/O-bound tasks, threading is sufficient and more efficient
        """
        )

    # When to use each one
    print("\n" + "=" * 70)
    print("DECISION GUIDE")
    print("=" * 70)
    print(
        """
    📊 USE THREADING when:
    • I/O-bound operations (network, disk, database)
    • You need to share memory across workers easily
    • Process overhead is prohibitive
    • Example: Web scraping, API calls, file I/O

    🚀 USE MULTIPROCESSING when:
    • CPU-bound operations (calculations, data processing)
    • You need true parallelism across multiple cores
    • Data can be serialized efficiently
    • Example: Image processing, data analysis, simulations

    ⚡ USE ASYNCIO when:
    • Many concurrent I/O operations (1000s)
    • Event-driven architecture
    • Single-threaded but highly efficient for I/O
    • Example: Chat servers, real-time apps, microservices

    🔥 USE NATIVE EXTENSIONS when:
    • You need maximum performance
    • Libraries like NumPy and TensorFlow release the GIL internally
    • Example: Machine learning, scientific computing
    """
    )


if __name__ == "__main__":
    # Required for multiprocessing on Windows
    mp.freeze_support()
    main()
