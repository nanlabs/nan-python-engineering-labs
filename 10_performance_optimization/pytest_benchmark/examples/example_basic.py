"""Micro benchmark helper similar to pytest-benchmark setup."""

from time import perf_counter


def operation() -> int:
    return sum(i * i for i in range(5000))


def benchmark(iterations: int = 300) -> tuple[float, int]:
    start = perf_counter()
    last = 0
    for _ in range(iterations):
        last = operation()
    elapsed = perf_counter() - start
    return elapsed / iterations, last


def main() -> None:
    avg, last = benchmark()
    print(f"Average time per call: {avg * 1e6:.2f} us")
    print(f"Last result: {last}")


if __name__ == '__main__':
    main()
