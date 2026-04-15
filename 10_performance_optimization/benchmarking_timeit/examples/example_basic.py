"""Benchmark list comprehension vs loop with timeit."""

import timeit


def with_comprehension() -> list[int]:
    return [x * x for x in range(1000)]


def with_loop() -> list[int]:
    result: list[int] = []
    for x in range(1000):
        result.append(x * x)
    return result


def main() -> None:
    comp = timeit.timeit('with_comprehension()', globals=globals(), number=5000)
    loop = timeit.timeit('with_loop()', globals=globals(), number=5000)

    print(f"Comprehension: {comp:.4f}s")
    print(f"Loop:          {loop:.4f}s")


if __name__ == '__main__':
    main()
