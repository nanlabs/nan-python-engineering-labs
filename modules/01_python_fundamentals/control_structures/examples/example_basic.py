"""Working example of control structures."""


def classify_temperature(value: int) -> str:
    """Classify a temperature using if/elif/else."""
    if value < 10:
        return "cold"
    if value < 24:
        return "mild"
    return "hot"


def average_valid_scores(scores: list[int | None]) -> float:
    """Use a loop with continue to skip missing values."""
    total = 0
    count = 0
    for score in scores:
        if score is None:
            continue
        total += score
        count += 1
    return total / count if count else 0.0


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(f"18C -> {classify_temperature(18)}")
    print(f"Valid average: {average_valid_scores([10, None, 8, 9])}")


if __name__ == "__main__":
    main()
