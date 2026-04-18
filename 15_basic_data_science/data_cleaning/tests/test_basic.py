"""Basic tests for the Data Cleaning exercise."""

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


def test_clean_customer_data_standardizes_columns_and_deduplicates() -> None:
    raw = pd.DataFrame(
        [
            {'Customer ID': 2, 'Customer Name': '  ana ', 'Revenue': 1200.0},
            {'Customer ID': 1, 'Customer Name': 'luis', 'Revenue': None},
            {'Customer ID': 2, 'Customer Name': 'ANA', 'Revenue': 1200.0},
        ]
    )
    cleaned = exercise.clean_customer_data(raw)
    assert list(cleaned.columns) == ['customer_id', 'customer_name', 'revenue']
    assert cleaned['customer_name'].tolist() == ['Luis', 'Ana']
    assert cleaned['revenue'].isna().sum() == 0
