"""Tests for the Integration Testing exercise."""

from __future__ import annotations

import importlib.util
import sqlite3
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "sqlite_user_repository.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/sqlite_user_repository.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("sqlite_user_repository", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_repository_round_trip() -> None:
    module = load_solution_module()
    connection = sqlite3.connect(":memory:")
    module.create_schema(connection)
    module.insert_user(connection, "alice@example.com")
    module.insert_user(connection, "bob@example.com")
    assert module.list_users(connection) == ["alice@example.com", "bob@example.com"]


def test_duplicate_email_fails() -> None:
    module = load_solution_module()
    connection = sqlite3.connect(":memory:")
    module.create_schema(connection)
    module.insert_user(connection, "alice@example.com")
    with pytest.raises(Exception):
        module.insert_user(connection, "alice@example.com")
