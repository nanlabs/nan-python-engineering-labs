"""Tests for the Test Organization exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "user_service.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/user_service.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("user_service", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_create_and_list_active_users() -> None:
    module = load_solution_module()
    service = module.UserService()
    service.create_user("bob@example.com")
    service.create_user("alice@example.com")
    assert service.active_emails() == ["alice@example.com", "bob@example.com"]


def test_deactivate_missing_user_fails() -> None:
    module = load_solution_module()
    service = module.UserService()
    with pytest.raises(LookupError):
        service.deactivate_user("missing@example.com")
