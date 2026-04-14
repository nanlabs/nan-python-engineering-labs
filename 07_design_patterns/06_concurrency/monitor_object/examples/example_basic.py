import threading


class CounterMonitor:
    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1

    def value(self) -> int:
        with self._lock:
            return self._value


def main() -> None:
    monitor = CounterMonitor()
    monitor.increment(); monitor.increment()
    print(monitor.value())


if __name__ == '__main__':
    main()
