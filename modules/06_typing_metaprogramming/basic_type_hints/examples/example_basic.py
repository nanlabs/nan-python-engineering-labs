def add(a: int, b: int) -> int:
    return a + b


def describe_total(a: int, b: int) -> str:
    total = add(a, b)
    return f"Total for {a} + {b} is {total}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(describe_total(2, 3))


if __name__ == "__main__":
    main()
