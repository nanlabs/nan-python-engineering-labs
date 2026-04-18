"""Basic tests for the Pandas Performance exercise."""

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


def test_apply_discount_vectorized_preserves_index() -> None:
    df = pd.DataFrame({'revenue': [100.0, 200.0, 80.0]}, index=['a', 'b', 'c'])
    result = exercise.apply_discount_vectorized(df, threshold=120.0, rate=0.1)
    assert list(result.index) == ['a', 'b', 'c']
    assert result.tolist() == [100.0, 180.0, 80.0]
