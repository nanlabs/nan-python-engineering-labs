"""Demonstrate how parametrization reduces repetition in tests."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailCase:
    raw: str
    normalized: str
    is_company_email: bool


CASES = [
    EmailCase(" Alice@Example.com ", "alice@example.com", False),
    EmailCase("bob@company.dev", "bob@company.dev", True),
    EmailCase("sue@company.dev ", "sue@company.dev", True),
]


def normalize_email(value: str) -> str:
    return value.strip().lower()


if __name__ == "__main__":
    print("parametrize example")
    for case in CASES:
        normalized = normalize_email(case.raw)
        print(f"{case.raw!r} -> {normalized!r} | company={case.is_company_email}")
