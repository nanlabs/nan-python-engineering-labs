"""viztracer: function call tracing demo."""

import time


def outer_task(n: int) -> int:
    return sum(inner_compute(i) for i in range(n))


def inner_compute(x: int) -> int:
    return x * x


def trace_calls(fn, *args) -> dict[str, object]:
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return {
        "function": fn.__name__,
        "args": args,
        "result": result,
        "ms": round(elapsed * 1_000, 3),
    }


def main() -> None:
    """Entry point to demonstrate the implementation."""
    report = trace_calls(outer_task, 100)
    print(report)
    print("In production: use `viztracer python script.py` then open result.json")


if __name__ == "__main__":
    main()
