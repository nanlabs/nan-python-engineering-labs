"""Working example of imports from the standard library."""

from math import ceil
from pathlib import Path
from statistics import mean


def build_report_path(base_dir: str, module_name: str) -> Path:
    """Build a path using pathlib."""
    return Path(base_dir) / module_name / "report.txt"


def estimate_iterations(values: list[int], chunk_size: int) -> int:
    """Combine statistics and math for a simple calculation."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if not values:
        return 0
    return ceil(mean(values) / chunk_size)


def main() -> None:
    """
    Main function to demonstrate the usage of pathlib, math, and statistics modules.
    """
    print(build_report_path("nan-python-engineering-labs", "01_python_fundamentals"))
    print(f"Estimated iterations: {estimate_iterations([10, 14, 12], 4)}")


if __name__ == "__main__":
    main()
