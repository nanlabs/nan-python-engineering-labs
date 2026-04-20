import sys
from dataclasses import dataclass


@dataclass
class Node:
    value: int


def main() -> None:
    """Entry point to demonstrate the implementation."""
    data = [Node(i) for i in range(5)]
    sizes = [sys.getsizeof(item) for item in data]
    print(f"min={min(sizes)}, max={max(sizes)}")


if __name__ == "__main__":
    main()
