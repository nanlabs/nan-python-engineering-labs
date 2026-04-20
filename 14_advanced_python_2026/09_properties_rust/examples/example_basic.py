"""
Properties: Rust fields exposed as Python @property decorators.
"""


class Rectangle:
    """Rectangle with properties."""

    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def area(self) -> float:
        return self._width * self._height


if __name__ == "__main__":
    rect = Rectangle(5, 10)
    print(f"Area: {rect.area}")
    rect.width = 8
    print(f"New area: {rect.area}")
