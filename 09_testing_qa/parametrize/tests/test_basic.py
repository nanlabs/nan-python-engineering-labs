"""Tests for the Parametrize exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "email_tools.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/email_tools.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("email_tools", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (" Alice@Example.com ", "alice@example.com"),
        ("bob@company.dev", "bob@company.dev"),
        ("Carol@Sub.Domain", "carol@sub.domain"),
    ],
)
def test_normalize_email(raw: str, expected: str) -> None:
    module = load_solution_module()
    assert module.normalize_email(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("alice@example.com", "example.com"),
        ("bob@company.dev", "company.dev"),
    ],
)
def test_extract_domain(raw: str, expected: str) -> None:
    module = load_solution_module()
    assert module.extract_domain(raw) == expected


def test_extract_domain_rejects_invalid_values() -> None:
    module = load_solution_module()
    with pytest.raises(ValueError):
        module.extract_domain("missing-at-sign")
