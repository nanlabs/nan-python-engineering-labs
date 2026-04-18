"""Basic tests for the NumPy Basics exercise."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

MY_SOLUTION_DIR = Path(__file__).parent.parent / 'my_solution'
sys.path.insert(0, str(MY_SOLUTION_DIR))
exercise = pytest.importorskip(
    'exercise_01',
    reason='Copy exercises/exercise_01.py into my_solution/ before running tests.',
)


def test_normalize_scores_returns_zero_mean() -> None:
    values = np.array([10.0, 12.0, 14.0, 16.0])
    normalized = exercise.normalize_scores(values)
    assert np.isclose(normalized.mean(), 0.0)
    assert np.isclose(normalized.std(), 1.0)


def test_moving_average_uses_window_size() -> None:
    values = np.array([2.0, 4.0, 6.0, 8.0])
    result = exercise.moving_average(values, window=2)
    assert np.allclose(result, np.array([3.0, 5.0, 7.0]))
