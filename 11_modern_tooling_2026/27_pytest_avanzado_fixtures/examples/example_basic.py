"""Advanced pytest: fixture factory and parametrize demo."""
from typing import Callable


def make_adder(base: int) -> Callable[[int], int]:
    def adder(x: int) -> int:
        return base + x
    return adder


def parametrize_cases() -> list[tuple[int, int, int]]:
    return [
        (0,  5,  5),
        (10, 3,  13),
        (-1, 1,  0),
        (100, 0, 100),
    ]


def run_parametrized_test(base: int, x: int, expected: int) -> bool:
    adder = make_adder(base)
    result = adder(x)
    return result == expected


def main() -> None:
    cases = parametrize_cases()
    passed = [c for c in cases if run_parametrized_test(*c)]
    print(f"Passed {len(passed)}/{len(cases)} parametrized cases")
    for c in cases:
        status = "PASS" if run_parametrized_test(*c) else "FAIL"
        print(f"  [{status}] make_adder({c[0]})({c[1]}) == {c[2]}")


if __name__ == "__main__":
    main()
