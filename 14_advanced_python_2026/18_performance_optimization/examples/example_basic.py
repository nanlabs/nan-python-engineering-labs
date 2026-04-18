"""Compare baseline and optimized implementations with simple timing measurements."""

from __future__ import annotations

from functools import lru_cache
import time


def fibonacci_plain(n: int) -> int:
    if n < 2:
        return n
    return fibonacci_plain(n - 1) + fibonacci_plain(n - 2)


@lru_cache(maxsize=None)
def fibonacci_cached(n: int) -> int:
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def timed_call(func, n: int) -> tuple[int, float]:
    start = time.perf_counter()
    result = func(n)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


def main() -> None:
    n = 32
    plain_result, plain_ms = timed_call(fibonacci_plain, n)
    cached_result, cached_ms = timed_call(fibonacci_cached, n)

    print(f"fibonacci_plain({n})={plain_result} in {plain_ms:.2f} ms")
    print(f"fibonacci_cached({n})={cached_result} in {cached_ms:.2f} ms")
    if cached_ms > 0:
        print(f"speedup ≈ {plain_ms / cached_ms:.1f}x")


if __name__ == "__main__":
    main()
