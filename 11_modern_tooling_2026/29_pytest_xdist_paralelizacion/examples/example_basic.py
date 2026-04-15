"""pytest-xdist: parallelization concepts demo."""
from concurrent.futures import ThreadPoolExecutor


def slow_test(test_id: int) -> tuple[int, str]:
    import math
    _ = sum(math.sqrt(i) for i in range(10_000))
    return test_id, "PASS"


def run_parallel(test_ids: list[int], workers: int = 4) -> list[tuple[int, str]]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(slow_test, test_ids))


def main() -> None:
    results = run_parallel(list(range(8)))
    passed = sum(1 for _, s in results if s == "PASS")
    print(f"Ran {len(results)} tests in parallel → {passed} PASS")


if __name__ == "__main__":
    main()
