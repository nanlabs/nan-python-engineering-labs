"""Exercise: Data Cleaning.

Goal: Clean a customer dataset by standardizing columns, filling gaps, and removing duplicates.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Keep the original business meaning of each row.
3. Run tests with: pytest tests/
4. Return a cleaned DataFrame with deterministic ordering.
"""

from __future__ import annotations

import pandas as pd


def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned customer dataset ready for downstream analysis."""
    raise NotImplementedError('Implement clean_customer_data in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to try your cleaning rules on sample data."""
    print('Copy this file into my_solution/ and clean a messy customer dataset.')


if __name__ == '__main__':
    main()
