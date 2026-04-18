"""Mimic a Python class that could be backed by Rust for fast numeric operations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Vector2D:
    """Small vector type with methods often delegated to native extensions."""

    x: float
    y: float

    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def dot(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y

    def normalized(self) -> "Vector2D":
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return Vector2D(self.x / mag, self.y / mag)


def main() -> None:
    a = Vector2D(3.0, 4.0)
    b = Vector2D(1.5, -2.0)

    print(f"a={a}, magnitude={a.magnitude():.2f}")
    print(f"b={b}, magnitude={b.magnitude():.2f}")
    print(f"dot(a, b)={a.dot(b):.2f}")
    print(f"normalized(a)={a.normalized()}")


if __name__ == "__main__":
    main()
