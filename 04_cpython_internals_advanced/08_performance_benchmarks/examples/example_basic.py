from statistics import mean
import time


def time_call(fn, *args) -> float:
    start = time.perf_counter()
    fn(*args)
    return time.perf_counter() - start


def compute(limit: int) -> int:
    return sum(i * i for i in range(limit))


def main() -> None:
    runs = [time_call(compute, 150_000) for _ in range(5)]
    print(f"avg={mean(runs):.6f}s")


if __name__ == "__main__":
    main()
