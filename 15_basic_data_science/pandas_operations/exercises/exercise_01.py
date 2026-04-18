"""Exercise: Pandas Operations.

Goal: Join order and customer tables, then compute segment-level metrics.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Preserve the requested output column names.
3. Run tests with: pytest tests/
4. Prefer clear Pandas operations over nested loops.
"""

from __future__ import annotations

import pandas as pd


def summarize_orders(orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
    """Return revenue and average order value per customer segment."""
    raise NotImplementedError('Implement summarize_orders in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to prototype your transformation pipeline."""
    print('Copy this file into my_solution/ and join a small orders/customers dataset.')


if __name__ == '__main__':
    main()
