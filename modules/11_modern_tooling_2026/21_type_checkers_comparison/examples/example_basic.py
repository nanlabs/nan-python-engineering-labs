"""Type checkers comparison: mypy vs pyright vs pylyzer feature matrix."""


def feature_matrix() -> list[dict[str, object]]:
    return [
        {"tool": "mypy", "language": "Python", "speed": "medium", "strict": True, "plugins": True},
        {
            "tool": "pyright",
            "language": "Python",
            "speed": "fast",
            "strict": True,
            "plugins": False,
        },
        {
            "tool": "basedpyright",
            "language": "Python",
            "speed": "fast",
            "strict": True,
            "plugins": False,
        },
        {
            "tool": "pylyzer",
            "language": "Rust",
            "speed": "fastest",
            "strict": True,
            "plugins": False,
        },
    ]


def rank_by_speed(matrix: list[dict[str, object]]) -> list[str]:
    order = {"fastest": 0, "fast": 1, "medium": 2}
    sorted_tools = sorted(matrix, key=lambda t: order.get(str(t["speed"]), 10))
    return [str(t["tool"]) for t in sorted_tools]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    matrix = feature_matrix()
    print(f"{'Tool':<15} {'Speed':<10} {'Strict':>8}")
    for row in matrix:
        print(f"  {row['tool']:<15} {row['speed']:<10} {row['strict']!s:>8}")
    print(f"\nFastest to slowest: {rank_by_speed(matrix)}")


if __name__ == "__main__":
    main()
