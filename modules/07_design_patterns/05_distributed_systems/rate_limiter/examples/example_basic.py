import time


class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: float) -> None:
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls: list[float] = []

    def allow(self) -> bool:
        now = time.time()
        self.calls = [t for t in self.calls if now - t <= self.window]
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True


def main() -> None:
    """Entry point to demonstrate the implementation."""
    limiter = RateLimiter(2, 1.0)
    print(limiter.allow(), limiter.allow(), limiter.allow())


if __name__ == "__main__":
    main()
