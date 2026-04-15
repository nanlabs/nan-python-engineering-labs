"""Compare memory usage with and without __slots__."""

import sys


class RegularPoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def main() -> None:
    regular = RegularPoint(1, 2)
    slotted = SlottedPoint(1, 2)
    print(f"Regular object size: {sys.getsizeof(regular)}")
    print(f"Slotted object size: {sys.getsizeof(slotted)}")


if __name__ == '__main__':
    main()
