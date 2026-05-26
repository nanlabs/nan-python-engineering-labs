class Vector2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    a = Vector2D(1, 2)
    b = Vector2D(3, 4)
    print(a + b)


if __name__ == "__main__":
    main()
