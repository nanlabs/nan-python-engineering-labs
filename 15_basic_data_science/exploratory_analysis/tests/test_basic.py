"""Basic tests for the Exploratory Analysis exercise."""

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


def test_compute_eda_report_includes_core_keys() -> None:
    df = pd.DataFrame(
        [
            {'region': 'north', 'revenue': 1200.0, 'units': 12},
            {'region': 'south', 'revenue': 950.0, 'units': 10},
            {'region': 'north', 'revenue': 1400.0, 'units': 14},
        ]
    )
    report = exercise.compute_eda_report(df)
    assert report['rows'] == 3
    assert report['top_region'] == 'north'
    assert 'numeric_summary' in report
