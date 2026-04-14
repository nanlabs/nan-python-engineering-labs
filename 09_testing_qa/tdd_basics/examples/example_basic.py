"""TDD thrives on tiny steps and explicit expectations."""

from __future__ import annotations


def add(expression: str) -> int:
    if not expression:
        return 0
    parts = [int(part) for part in expression.split(",")]
    negatives = [value for value in parts if value < 0]
    if negatives:
        raise ValueError(f"negative numbers not allowed: {negatives}")
    return sum(parts)


if __name__ == "__main__":
    print("tdd basics example")
    for expression in ["", "1", "1,2,3"]:
        print(f"{expression!r} -> {add(expression)}")
