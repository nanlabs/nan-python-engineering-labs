"""Working example of closures."""


def make_multiplier(factor: int):
    """Return a function that remembers the multiplication factor."""
    def multiply(value: int) -> int:
        return value * factor
    return multiply


def make_threshold_checker(limit: int):
    """Return a function that compares values against a saved limit."""
    def is_above(value: int) -> bool:
        return value > limit
    return is_above


def main() -> None:
    double = make_multiplier(2)
    is_priority = make_threshold_checker(10)
    print(double(8))
    print(is_priority(7))
    print(is_priority(14))


if __name__ == '__main__':
    main()
