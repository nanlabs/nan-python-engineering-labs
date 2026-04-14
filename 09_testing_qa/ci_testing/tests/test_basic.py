"""Tests for the CI Testing exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "quality_gate.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/quality_gate.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("quality_gate", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_validate_test_report() -> None:
    module = load_solution_module()
    report = {"passed": 12, "failed": 0, "skipped": 1}
    assert module.validate_test_report(report) is True


def test_should_publish_artifacts_requires_coverage_threshold() -> None:
    module = load_solution_module()
    report = {"passed": 12, "failed": 0, "skipped": 1}
    assert module.should_publish_artifacts(report, 90.0) is True
    assert module.should_publish_artifacts(report, 70.0) is False


def test_validate_test_report_rejects_missing_keys() -> None:
    module = load_solution_module()
    with pytest.raises(ValueError):
        module.validate_test_report({"passed": 1, "failed": 0})
