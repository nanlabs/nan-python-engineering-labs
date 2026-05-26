from typing import NamedTuple, TypedDict


class User(TypedDict):
    name: str
    age: int


class Point(NamedTuple):
    x: int
    y: int


def main() -> None:
    """Entry point to demonstrate the implementation."""
    user: User = {"name": "Ada", "age": 32}
    point = Point(3, 5)
    print(user["name"], point.x + point.y)


if __name__ == "__main__":
    main()
