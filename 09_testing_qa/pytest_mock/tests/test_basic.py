"""Tests for the pytest-mock exercise."""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "report_service.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/report_service.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("report_service", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generate_daily_summary_uses_current_day() -> None:
    module = load_solution_module()

    class FakeClock:
        def today(self):
            return date(2026, 4, 1)

    class FakeRepository:
        def fetch_day(self, day: date):
            assert day == date(2026, 4, 1)
            return {"orders": 5, "revenue": 300.0}

    service = module.ReportService(FakeRepository(), FakeClock())
    report = service.generate_daily_summary()
    assert report.total_orders == 5
    assert report.total_revenue == 300.0


def test_generate_daily_summary_requires_data() -> None:
    module = load_solution_module()

    class FakeClock:
        def today(self):
            return date(2026, 4, 1)

    class EmptyRepository:
        def fetch_day(self, day: date):
            return None

    service = module.ReportService(EmptyRepository(), FakeClock())
    with pytest.raises(LookupError):
        service.generate_daily_summary()
