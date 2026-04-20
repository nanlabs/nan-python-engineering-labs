from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Money(100, "USD") == Money(100, "USD"))


if __name__ == "__main__":
    main()
