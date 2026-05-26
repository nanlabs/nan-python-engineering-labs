"""Pyright/BasedPyright: strict type narrowing example."""


def process(value: int | str | None) -> str:
    if value is None:
        return "empty"
    if isinstance(value, int):
        return f"integer: {value * 2}"
    return f"string: {value.upper()}"


def batch_process(items: list[int | str | None]) -> list[str]:
    return [process(item) for item in items]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    results = batch_process([1, "hello", None, 42, "world"])
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
