"""Exercise: pytest-mock.

Goal:
Create `my_solution/report_service.py`.

Requirements:
- Create a `Report` dataclass with `day`, `total_orders`, and `total_revenue`.
- Create `ReportService(repository, clock)`.
- `generate_daily_summary()` must query the repository for `clock.today()`.
- Raise `LookupError` when no data is available.

The tests are written so they can be solved either with plain dependency injection or with the `pytest-mock` plugin.
"""
