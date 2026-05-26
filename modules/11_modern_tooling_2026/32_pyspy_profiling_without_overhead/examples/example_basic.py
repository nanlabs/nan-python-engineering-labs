"""py-spy: sampling profiler concepts demo."""

import time


def cpu_intensive(n: int) -> float:
    import math

    return sum(math.log(i + 1) for i in range(n))


def profile_function(fn, *args) -> dict[str, object]:
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return {"result": round(result, 4), "elapsed_ms": round(elapsed * 1000, 2)}


def main() -> None:
    """Entry point to demonstrate the implementation."""
    report = profile_function(cpu_intensive, 50_000)
    print(f"Result: {report['result']}")
    print(f"Elapsed: {report['elapsed_ms']} ms")
    print("In production: use `py-spy record -o profile.svg -- python script.py`")


if __name__ == "__main__":
    main()
