"""Working example of basic context managers."""

from contextlib import contextmanager
from time import perf_counter


@contextmanager
def measure_block(label: str):
    """Measure how long a block takes to execute."""
    start = perf_counter()
    try:
        yield
    finally:
        duration = perf_counter() - start
        print(f"{label}: {duration:.6f}s")


def main() -> None:
    """Entry point to demonstrate the implementation."""
    with measure_block("sum block"):
        print(sum(range(1000)))


if __name__ == "__main__":
    main()
