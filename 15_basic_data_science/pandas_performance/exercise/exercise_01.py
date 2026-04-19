"""Exercise: Pandas Performance.

Goal: Implement a vectorized discount strategy for a revenue column.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Keep the vectorized solution column-oriented.
3. Run tests with: pytest tests/
4. Return a Pandas Series aligned with the original DataFrame index.
"""

from __future__ import annotations

import pandas as pd


def apply_discount_vectorized(df: pd.DataFrame, threshold: float, rate: float) -> pd.Series:
    """Return discounted revenue values using a vectorized strategy."""
    raise NotImplementedError('Implement apply_discount_vectorized in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to compare approaches in your own copy."""
    print('Copy this file into my_solution/ and compare vectorized vs. row-wise strategies.')


if __name__ == '__main__':
    main()
