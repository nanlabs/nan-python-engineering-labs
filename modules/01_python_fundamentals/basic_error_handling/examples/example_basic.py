"""Working example of basic error handling."""


def safe_divide(dividend: float, divisor: float) -> float | None:
    """Return the result or None when the divisor is invalid."""
    try:
        return dividend / divisor
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None


def parse_port(raw_value: str) -> int:
    """Validate a numeric configuration value and raise useful errors."""
    port = int(raw_value)
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    return port


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    try:
        print(parse_port("8080"))
        print(parse_port("70000"))
    except ValueError as error:
        print(f"Handled error: {error}")


if __name__ == "__main__":
    main()
