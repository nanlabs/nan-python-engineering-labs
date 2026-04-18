"""Use polymorphism to calculate area for multiple shapes."""

from dataclasses import dataclass
from math import pi


@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass
class Circle:
    radius: float

    def area(self) -> float:
        return pi * self.radius ** 2


def main() -> None:
    shapes = [Rectangle(4, 5), Circle(2), Rectangle(3, 1.5)]
    print([round(s.area(), 2) for s in shapes])


if __name__ == "__main__":
    main()
