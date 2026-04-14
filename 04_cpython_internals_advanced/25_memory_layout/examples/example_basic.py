from dataclasses import dataclass
import sys


@dataclass
class Node:
    value: int


def main() -> None:
    data = [Node(i) for i in range(5)]
    sizes = [sys.getsizeof(item) for item in data]
    print(f"min={min(sizes)}, max={max(sizes)}")


if __name__ == "__main__":
    main()
