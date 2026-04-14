import time


def timed_run(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def compute(limit: int) -> int:
    return sum(range(limit))


def main() -> None:
    result, elapsed = timed_run(compute, 100_000)
    print(result)
    print(f'{elapsed:.6f}s')


if __name__ == '__main__':
    main()
