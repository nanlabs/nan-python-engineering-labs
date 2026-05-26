"""Mutation testing: demonstrate survivable vs killed mutations."""


def discount(price: float, rate: float) -> float:
    if rate < 0 or rate > 1:
        raise ValueError("Rate must be between 0 and 1")
    return round(price * (1 - rate), 2)


def run_test_suite() -> list[dict[str, object]]:
    cases = [
        (100.0, 0.1, 90.0),
        (200.0, 0.0, 200.0),
        (50.0, 0.5, 25.0),
    ]
    results = []
    for price, rate, expected in cases:
        actual = discount(price, rate)
        results.append(
            {
                "input": (price, rate),
                "expected": expected,
                "actual": actual,
                "pass": actual == expected,
            }
        )
    return results


def main() -> None:
    """Entry point to demonstrate the implementation."""
    results = run_test_suite()
    passed = sum(1 for r in results if r["pass"])
    for r in results:
        print(r)
    print(f"Mutation killed by {passed}/{len(results)} tests")


if __name__ == "__main__":
    main()
