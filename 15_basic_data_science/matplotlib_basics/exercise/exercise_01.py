"""Exercise: Matplotlib Basics.

Goal: Build a clean line chart that can be reused in reports.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Return the Figure object so tests can inspect it.
3. Run tests with: pytest tests/
4. Use a non-interactive backend when experimenting locally.
"""

from __future__ import annotations

import matplotlib

matplotlib.use('Agg')

from matplotlib.figure import Figure


def build_sales_figure(months: list[str], sales: list[float]) -> Figure:
    """Return a Figure with a single monthly sales line."""
    raise NotImplementedError('Implement build_sales_figure in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to prototype your chart design."""
    print('Copy this file into my_solution/ and build a figure for a monthly sales trend.')


if __name__ == '__main__':
    main()
