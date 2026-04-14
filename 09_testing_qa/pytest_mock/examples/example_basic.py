"""Show the style encouraged by the pytest-mock plugin."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Report:
    day: date
    total_orders: int
    total_revenue: float


class ReportService:
    def __init__(self, repository, clock) -> None:
        self.repository = repository
        self.clock = clock

    def generate_daily_summary(self) -> Report:
        current_day = self.clock.today()
        data = self.repository.fetch_day(current_day)
        return Report(day=current_day, total_orders=data["orders"], total_revenue=data["revenue"])


if __name__ == "__main__":
    class FakeClock:
        def today(self):
            return date(2026, 4, 1)

    class FakeRepository:
        def fetch_day(self, day: date):
            return {"orders": 12, "revenue": 1450.0}

    service = ReportService(FakeRepository(), FakeClock())
    report = service.generate_daily_summary()
    print("pytest-mock example")
    print(report)
