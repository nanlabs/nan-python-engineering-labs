"""CI quality gates turn test outcomes into merge decisions."""

from __future__ import annotations


def validate_test_report(report: dict[str, int]) -> bool:
    required = {"passed", "failed", "skipped"}
    if required - report.keys():
        raise ValueError("report is missing required counters")
    if report["failed"] > 0:
        return False
    return report["passed"] > 0


def should_publish_artifacts(report: dict[str, int], coverage: float) -> bool:
    return validate_test_report(report) and coverage >= 85.0


if __name__ == "__main__":
    report = {"passed": 24, "failed": 0, "skipped": 2}
    print("ci testing example")
    print(f"ready to publish: {should_publish_artifacts(report, coverage=91.4)}")
