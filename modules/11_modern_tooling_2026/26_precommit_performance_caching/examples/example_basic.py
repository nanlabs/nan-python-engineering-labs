"""pre-commit caching: show how hook caching reduces runtime."""


def simulate_runs(
    hook: str,
    first_run_ms: float,
    cached_run_ms: float,
    changed_files: int,
) -> list[dict[str, object]]:
    return [
        {"run": "first", "hook": hook, "ms": first_run_ms, "files_checked": changed_files},
        {"run": "cached", "hook": hook, "ms": cached_run_ms, "files_checked": changed_files},
    ]


def speedup_factor(baseline_ms: float, cached_ms: float) -> float:
    return round(baseline_ms / cached_ms, 1)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    runs = simulate_runs("ruff", first_run_ms=800, cached_run_ms=45, changed_files=3)
    for r in runs:
        print(r)
    print(f"Speedup: {speedup_factor(800, 45)}x with caching enabled")


if __name__ == "__main__":
    main()
