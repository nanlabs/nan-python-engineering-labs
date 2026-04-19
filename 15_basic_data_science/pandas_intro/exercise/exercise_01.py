"""Exercise: Pandas Intro.

Goal: Build a tidy sales DataFrame and aggregate monthly revenue.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Keep the implementation readable and column-oriented.
3. Run tests with: pytest tests/
4. Return Pandas objects instead of raw dicts where requested.
"""

from __future__ import annotations

import pandas as pd


def build_sales_dataframe(records: list[dict[str, object]]) -> pd.DataFrame:
    """Create a DataFrame with a derived revenue column."""
    raise NotImplementedError('Implement build_sales_dataframe in my_solution/exercise_01.py')


def monthly_revenue(df: pd.DataFrame) -> pd.Series:
    """Return total revenue indexed by month."""
    raise NotImplementedError('Implement monthly_revenue in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to explore the expected inputs."""
    print('Copy this file into my_solution/ and experiment with a few sales records.')


if __name__ == '__main__':
    main()
