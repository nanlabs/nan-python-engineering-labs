"""Basic tests for the Matplotlib Basics exercise."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

MY_SOLUTION_DIR = Path(__file__).parent.parent / 'my_solution'
sys.path.insert(0, str(MY_SOLUTION_DIR))
exercise = pytest.importorskip(
    'exercise_01',
    reason='Copy exercises/exercise_01.py into my_solution/ before running tests.',
)


def test_build_sales_figure_returns_single_axes() -> None:
    fig = exercise.build_sales_figure(['Jan', 'Feb', 'Mar'], [10.0, 12.0, 14.0])
    assert len(fig.axes) == 1
    assert len(fig.axes[0].lines) == 1
