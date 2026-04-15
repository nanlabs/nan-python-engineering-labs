"""Ruff performance: simulate timing comparison against legacy tools."""
import time


def fake_check(tool: str, files: int, ms_per_file: float) -> dict[str, object]:
    elapsed = files * ms_per_file / 1000
    return {"tool": tool, "files": files, "elapsed_s": round(elapsed, 3)}


def benchmark_tools(files: int = 1000) -> list[dict[str, object]]:
    return [
        fake_check("flake8",  files, 3.0),
        fake_check("pylint",  files, 12.0),
        fake_check("mypy",    files, 8.0),
        fake_check("ruff",    files, 0.03),
    ]


def speedup(baseline: dict, fast: dict) -> float:
    return round(baseline["elapsed_s"] / fast["elapsed_s"], 1)


def main() -> None:
    results = benchmark_tools(files=1000)
    ruff = results[-1]
    print(f"{'Tool':<10} {'Files':>6} {'Time (s)':>10}")
    for r in results:
        print(f"  {r['tool']:<10} {r['files']:>6} {r['elapsed_s']:>10.3f}")
    print(f"\nRuff is {speedup(results[0], ruff)}x faster than flake8")


if __name__ == "__main__":
    main()
