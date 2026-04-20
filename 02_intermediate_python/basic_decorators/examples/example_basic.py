"""Working example of basic decorators."""

from functools import wraps


def log_calls(function):
    """Print function name and arguments before execution."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__} args={args} kwargs={kwargs}")
        return function(*args, **kwargs)

    return wrapper


@log_calls
def calculate_area(width: float, height: float) -> float:
    """Return a rectangle area."""
    return width * height


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(calculate_area(4, 2.5))


if __name__ == "__main__":
    main()
