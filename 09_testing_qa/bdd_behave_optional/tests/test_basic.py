"""Tests for the BDD with behave exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "shopping_cart.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/shopping_cart.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("shopping_cart", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_add_item_and_total() -> None:
    module = load_solution_module()
    cart = module.ShoppingCart()
    cart.add_item("Book", 12.5)
    cart.add_item("Pen", 1.2)
    assert cart.total() == 13.7


def test_clear_removes_all_items() -> None:
    module = load_solution_module()
    cart = module.ShoppingCart()
    cart.add_item("Book", 12.5)
    cart.clear()
    assert cart.total() == 0.0
