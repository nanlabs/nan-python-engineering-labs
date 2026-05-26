import inspect


def compute(a: int, b: int) -> int:
    return a + b


def main() -> None:
    """Entry point to demonstrate the implementation."""
    signature = inspect.signature(compute)
    print(signature)
    print(inspect.getdoc(compute))


if __name__ == "__main__":
    main()
