"""Tests for the Mocking with unittest.mock exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import Mock

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "notifier.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/notifier.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("notifier", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_send_welcome_email_calls_gateway() -> None:
    module = load_solution_module()
    gateway = Mock()
    gateway.deliver.return_value = True
    notifier = module.Notifier(gateway)

    assert notifier.send_welcome_email("alice@example.com") is True
    gateway.deliver.assert_called_once()


def test_send_welcome_email_handles_gateway_failures() -> None:
    module = load_solution_module()
    gateway = Mock()
    gateway.deliver.side_effect = RuntimeError("mail server unavailable")
    notifier = module.Notifier(gateway)

    assert notifier.send_welcome_email("alice@example.com") is False
