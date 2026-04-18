"""Exercise: Seaborn Visualization.

Goal: Build a Seaborn bar chart that compares average revenue by segment.

Instructions:
1. Copy this file into my_solution/ before editing it.
2. Return the Figure object so tests can inspect the result.
3. Run tests with: pytest tests/
4. Keep labels and chart titles explicit.
"""

from __future__ import annotations

import matplotlib

matplotlib.use('Agg')

from matplotlib.figure import Figure
import pandas as pd


def build_segment_chart(df: pd.DataFrame) -> Figure:
    """Return a Figure that compares average revenue by segment."""
    raise NotImplementedError('Implement build_segment_chart in my_solution/exercise_01.py')


def main() -> None:
    """Use this entry point to experiment with your chart design."""
    print('Copy this file into my_solution/ and build a Seaborn bar chart.')


if __name__ == '__main__':
    main()
