"""Working example of basic iterators."""


class Countdown:
    """Simple iterator that counts down to zero."""

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(list(Countdown(5)))


if __name__ == "__main__":
    main()
