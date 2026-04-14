class Timer:
    def __enter__(self):
        import time
        self._time = time.perf_counter
        self._start = self._time()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = self._time() - self._start


def main() -> None:
    with Timer() as timer:
        sum(range(10000))
    print(round(timer.elapsed, 6))


if __name__ == '__main__':
    main()
