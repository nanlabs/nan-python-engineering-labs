"""pytest-cov: coverage measurement concepts demo."""


def covered_branch(value: int) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "zero"


def compute_coverage(executed_branches: set[str], total_branches: set[str]) -> float:
    if not total_branches:
        return 0.0
    return len(executed_branches & total_branches) / len(total_branches) * 100


def main() -> None:
    """Entry point to demonstrate the implementation."""
    tests = [-5, 0, 10]
    results = [covered_branch(v) for v in tests]
    print(results)

    executed = set(results)
    total = {"positive", "negative", "zero"}
    coverage = compute_coverage(executed, total)
    print(f"Branch coverage: {coverage:.0f}%")


if __name__ == "__main__":
    main()
