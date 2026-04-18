"""Basic tests for the Seaborn Visualization exercise."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

MY_SOLUTION_DIR = Path(__file__).parent.parent / 'my_solution'
sys.path.insert(0, str(MY_SOLUTION_DIR))
exercise = pytest.importorskip(
    'exercise_01',
    reason='Copy exercises/exercise_01.py into my_solution/ before running tests.',
)


def test_build_segment_chart_returns_figure() -> None:
    df = pd.DataFrame(
        [
            {'segment': 'enterprise', 'avg_revenue': 220.0},
            {'segment': 'startup', 'avg_revenue': 150.0},
        ]
    )
    fig = exercise.build_segment_chart(df)
    assert len(fig.axes) == 1
    assert fig.axes[0].get_title()
