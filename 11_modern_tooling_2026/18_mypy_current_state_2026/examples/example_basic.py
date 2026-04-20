"""mypy 2026: strict mode and incremental checking demo."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict[str, object]:
        ...


class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "age": self.age}


def serialize(obj: Serializable) -> dict[str, object]:
    return obj.to_dict()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    user = User("Alice", 30)
    print(isinstance(user, Serializable))
    print(serialize(user))


if __name__ == "__main__":
    main()
