"""Tests for the TDD Basics exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "string_calculator.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/string_calculator.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("string_calculator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(("expression", "expected"), [("", 0), ("1", 1), ("1,2,3", 6)])
def test_add(expression: str, expected: int) -> None:
    module = load_solution_module()
    assert module.add(expression) == expected


def test_negative_numbers_fail() -> None:
    module = load_solution_module()
    with pytest.raises(ValueError):
        module.add("1,-2,3")
