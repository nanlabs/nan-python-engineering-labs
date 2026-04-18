"""Exercise: Exploratory Analysis.

Goal: Produce a compact EDA report with key numeric and categorical signals.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Return plain Python objects where requested.
3. Run tests with: pytest tests/
4. Keep the report small but interpretable.
"""

from __future__ import annotations

import pandas as pd


def compute_eda_report(df: pd.DataFrame) -> dict[str, object]:
    """Return a compact exploratory analysis report for the dataset."""
    raise NotImplementedError('Implement compute_eda_report in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to inspect a small report locally."""
    print('Copy this file into my_solution/ and produce a compact EDA report.')


if __name__ == '__main__':
    main()
