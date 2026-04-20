import threading


class Counter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        return self._value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    counter = Counter()
    for _ in range(1000):
        counter.increment()
    print(counter.value)


if __name__ == "__main__":
    main()
