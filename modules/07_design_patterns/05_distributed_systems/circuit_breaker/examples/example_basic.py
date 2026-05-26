class CircuitBreaker:
    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        self.failures = 0
        self.open = False

    def call(self, fn, *args):
        if self.open:
            return "fallback"
        try:
            return fn(*args)
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.open = True
            return "error"


def unstable(flag: bool) -> str:
    if flag:
        raise RuntimeError("boom")
    return "ok"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    cb = CircuitBreaker(2)
    print(cb.call(unstable, True))
    print(cb.call(unstable, True))
    print(cb.call(unstable, False))


if __name__ == "__main__":
    main()
