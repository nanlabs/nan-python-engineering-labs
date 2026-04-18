"""Basic tests for the Pandas Operations exercise."""

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


def test_summarize_orders_groups_by_segment() -> None:
    orders = pd.DataFrame(
        [
            {'customer_id': 1, 'amount': 100.0},
            {'customer_id': 1, 'amount': 50.0},
            {'customer_id': 2, 'amount': 80.0},
        ]
    )
    customers = pd.DataFrame(
        [
            {'customer_id': 1, 'segment': 'enterprise'},
            {'customer_id': 2, 'segment': 'startup'},
        ]
    )
    result = exercise.summarize_orders(orders, customers)
    rows = {row['segment']: row for row in result.to_dict(orient='records')}
    assert rows['enterprise']['total_revenue'] == 150.0
    assert rows['startup']['average_order_value'] == 80.0
