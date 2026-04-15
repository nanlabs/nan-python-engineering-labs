"""Pylyzer: type-level reasoning demo (pure Python equivalent)."""


def annotated_pipeline(
    items: list[int],
    multiplier: float,
) -> list[float]:
    return [item * multiplier for item in items]


def safe_divide(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def main() -> None:
    result = annotated_pipeline([1, 2, 3, 4], 1.5)
    print(result)
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))


if __name__ == "__main__":
    main()
