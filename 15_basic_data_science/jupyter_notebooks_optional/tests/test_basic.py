"""Basic tests for the Jupyter Notebooks exercise."""

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


def test_build_notebook_outline_creates_title_and_sections() -> None:
    notebook = exercise.build_notebook_outline('Weekly analysis', ['Load data', 'Explore'])
    assert notebook['cells'][0]['source'][0].startswith('# Weekly analysis')
    assert exercise.count_code_cells(notebook) == 2
