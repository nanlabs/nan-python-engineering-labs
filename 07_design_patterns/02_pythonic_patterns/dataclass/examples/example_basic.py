from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    active: bool = True


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(User(1, "Ada"))


if __name__ == "__main__":
    main()
