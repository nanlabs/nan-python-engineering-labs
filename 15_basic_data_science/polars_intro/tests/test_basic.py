"""Basic tests for the Polars Intro exercise."""

from __future__ import annotations

import sys
from pathlib import Path

import polars as pl
import pytest

MY_SOLUTION_DIR = Path(__file__).parent.parent / 'my_solution'
sys.path.insert(0, str(MY_SOLUTION_DIR))
exercise = pytest.importorskip(
    'exercise_01',
    reason='Copy exercises/exercise_01.py into my_solution/ before running tests.',
)


def test_summarize_shipments_groups_and_sorts() -> None:
    frame = pl.DataFrame(
        {
            'warehouse': ['east', 'west', 'east'],
            'items': [120, 90, 80],
            'shipping_cost': [30.0, 22.0, 20.0],
        }
    )
    result = exercise.summarize_shipments(frame)
    assert result.to_dicts()[0]['warehouse'] == 'east'
    assert result.to_dicts()[0]['total_items'] == 200
