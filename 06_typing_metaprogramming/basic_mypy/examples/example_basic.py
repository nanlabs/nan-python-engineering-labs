"""Model typed data structures in a mypy-friendly style."""

from typing import TypedDict


class User(TypedDict):
    username: str
    age: int
    active: bool


def can_access_dashboard(user: User) -> bool:
    return user["active"] and user["age"] >= 18


def main() -> None:
    user: User = {"username": "ana", "age": 28, "active": True}
    print(can_access_dashboard(user))


if __name__ == "__main__":
    main()
