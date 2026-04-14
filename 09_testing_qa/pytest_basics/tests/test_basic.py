"""Tests for the Pytest Basics exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "calculator.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/calculator.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("calculator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_basic_operations() -> None:
    module = load_solution_module()
    assert module.add(2, 3) == 5
    assert module.subtract(10, 4) == 6


def test_divide_rejects_zero() -> None:
    module = load_solution_module()
    with pytest.raises(ValueError):
        module.divide(3, 0)


def test_classify_number() -> None:
    module = load_solution_module()
    assert module.classify_number(4) == "positive"
    assert module.classify_number(-2) == "negative"
    assert module.classify_number(0) == "zero"
