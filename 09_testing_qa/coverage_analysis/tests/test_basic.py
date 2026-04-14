"""Tests for the Coverage Analysis exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "discount_rules.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/discount_rules.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("discount_rules", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_gold_customers_receive_discount() -> None:
    module = load_solution_module()
    assert module.loyalty_discount(100, "gold") == 90.0


def test_standard_shipping_is_free_after_threshold() -> None:
    module = load_solution_module()
    assert module.shipping_cost(120, expedited=False) == 0.0


def test_final_amount_includes_expedited_shipping() -> None:
    module = load_solution_module()
    assert module.final_amount(80, "silver", expedited=True) == pytest.approx(88.0)
