"""Line-level timing approximation using perf_counter."""

from time import perf_counter


def expensive_step(data: list[int]) -> int:
    return sum(x * x for x in data if x % 3 == 0)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    data = list(range(20000))

    t0 = perf_counter()
    filtered = [x for x in data if x % 2 == 0]
    t1 = perf_counter()

    result = expensive_step(filtered)
    t2 = perf_counter()

    print(f"Filter stage: {(t1 - t0) * 1000:.2f} ms")
    print(f"Compute stage: {(t2 - t1) * 1000:.2f} ms")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
