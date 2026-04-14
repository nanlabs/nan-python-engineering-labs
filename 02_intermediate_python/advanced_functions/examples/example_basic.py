"""Working example of advanced functions."""


def apply_operation(values: list[int], operation) -> list[int]:
    """Apply a callable to each value."""
    return [operation(value) for value in values]


def build_formatter(prefix: str):
    """Return a function that formats messages with a prefix."""
    def formatter(message: str) -> str:
        return f"{prefix}: {message}"
    return formatter


def combine_scores(*scores: int, bonus: int = 0) -> int:
    """Use *args and keyword-only arguments in a single function."""
    return sum(scores) + bonus


def main() -> None:
    """
    Show how to use the advanced function features in practice.
    """
    print(apply_operation([1, 2, 3], lambda value: value * 10))
    warning = build_formatter('warning')
    print(warning('disk usage is above 80%'))
    print(combine_scores(10, 20, 15, bonus=5))


if __name__ == '__main__':
    main()
