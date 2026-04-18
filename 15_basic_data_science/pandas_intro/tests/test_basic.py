"""Basic tests for the Pandas Intro exercise."""

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


def test_build_sales_dataframe_adds_revenue() -> None:
    records = [
        {'month': '2026-01', 'units': 10, 'unit_price': 5.0},
        {'month': '2026-02', 'units': 20, 'unit_price': 4.0},
    ]
    df = exercise.build_sales_dataframe(records)
    assert list(df['revenue']) == [50.0, 80.0]


def test_monthly_revenue_groups_by_month() -> None:
    df = pd.DataFrame(
        [
            {'month': '2026-01', 'revenue': 50.0},
            {'month': '2026-01', 'revenue': 25.0},
            {'month': '2026-02', 'revenue': 80.0},
        ]
    )
    result = exercise.monthly_revenue(df)
    assert result.to_dict() == {'2026-01': 75.0, '2026-02': 80.0}
