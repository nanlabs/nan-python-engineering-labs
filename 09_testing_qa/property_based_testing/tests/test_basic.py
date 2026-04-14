"""Tests for the Property-Based Testing exercise."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "list_tools.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/list_tools.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("list_tools", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_rotate_list_preserves_multiset() -> None:
    module = load_solution_module()
    original = [1, 2, 3, 4]
    rotated = module.rotate_list(original, 1)
    assert Counter(rotated) == Counter(original)


def test_deduplicate_preserve_order() -> None:
    module = load_solution_module()
    assert module.deduplicate_preserve_order([1, 2, 1, 3, 2]) == [1, 2, 3]


def test_rotate_empty_list() -> None:
    module = load_solution_module()
    assert module.rotate_list([], 3) == []
