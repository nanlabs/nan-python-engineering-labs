"""Tests for the Contract Testing exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "payment_contract.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/payment_contract.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("payment_contract", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_validate_payment_response_normalizes_status() -> None:
    module = load_solution_module()
    payload = {
        "payment_id": "pay_123",
        "status": "APPROVED",
        "amount": 150.0,
        "currency": "USD",
    }
    validated = module.validate_payment_response(payload)
    assert validated["status"] == "approved"


def test_validate_payment_response_requires_all_keys() -> None:
    module = load_solution_module()
    with pytest.raises(ValueError):
        module.validate_payment_response({"payment_id": "pay_123"})
