"""Tests for the Hypothesis Introduction exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "text_normalizer.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/text_normalizer.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("text_normalizer", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_collapse_whitespace() -> None:
    module = load_solution_module()
    assert module.collapse_whitespace("  hello   world  ") == "hello world"


def test_normalize_title() -> None:
    module = load_solution_module()
    assert module.normalize_title("  hello   world  ") == "Hello World"


def test_functions_are_idempotent() -> None:
    module = load_solution_module()
    normalized = module.normalize_title("multiple\nlines\tinside")
    assert module.normalize_title(normalized) == normalized
