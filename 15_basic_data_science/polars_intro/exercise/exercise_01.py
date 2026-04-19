"""Exercise: Polars Intro.

Goal: Summarize shipment metrics by warehouse using Polars expressions.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Keep the output sorted by total items descending.
3. Run tests with: pytest tests/
4. Use Polars expressions instead of manual loops.
"""

from __future__ import annotations

import polars as pl


def summarize_shipments(frame: pl.DataFrame) -> pl.DataFrame:
    """Return total items and average shipping cost per warehouse."""
    raise NotImplementedError('Implement summarize_shipments in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to prototype a Polars aggregation locally."""
    print('Copy this file into my_solution/ and summarize shipments per warehouse.')


if __name__ == '__main__':
    main()
