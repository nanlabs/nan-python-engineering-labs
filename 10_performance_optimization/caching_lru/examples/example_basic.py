"""Simple memoization example similar to LRU behavior."""

from functools import lru_cache


@lru_cache(maxsize=256)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main() -> None:
    print(f"fib(35) = {fibonacci(35)}")
    print(f"Cache stats: {fibonacci.cache_info()}")


if __name__ == '__main__':
    main()
