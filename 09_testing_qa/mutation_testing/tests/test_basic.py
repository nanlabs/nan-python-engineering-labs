"""Tests for the Mutation Testing exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "pricing.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/pricing.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("pricing", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_apply_tax() -> None:
    module = load_solution_module()
    assert module.apply_tax(100, 0.21) == 121.0


def test_apply_discount() -> None:
    module = load_solution_module()
    assert module.apply_discount(100, 0.10) == 90.0


def test_final_price_discount_then_tax() -> None:
    module = load_solution_module()
    assert module.final_price(100, tax_rate=0.21, discount_rate=0.10) == 108.9
