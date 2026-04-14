"""Exercise: CI Testing.

Goal:
Create `my_solution/quality_gate.py`.

Requirements:
- `validate_test_report(report)` requires `passed`, `failed`, and `skipped` keys.
- It returns `True` only when at least one test passed and zero failed.
- `should_publish_artifacts(report, coverage)` returns `True` only when the report is valid and coverage is at least 85.

This is the kind of logic a CI pipeline could enforce before deployment.
"""
