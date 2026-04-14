"""Working example of basic debugging."""


def average_positive(values: list[int]) -> float:
    """Show a simple debugging flow with prints and assertions."""
    print(f"[debug] received values={values}")
    positives = [value for value in values if value >= 0]
    print(f"[debug] positive values={positives}")
    if not positives:
        raise ValueError("At least one positive value is required.")

    result = sum(positives) / len(positives)
    print(f"[debug] computed average={result}")
    assert result >= 0
    return result


def main() -> None:
    print(average_positive([10, -5, 20, 15]))


if __name__ == "__main__":
    main()
