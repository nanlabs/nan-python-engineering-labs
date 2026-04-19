"""Basic tests for exercise_01 validation behavior."""

from exercises.exercise_01 import validate_input


def test_rejects_empty_input() -> None:
    result = validate_input("   ")
    assert result.accepted is False


def test_accepts_reasonable_input() -> None:
    result = validate_input("security-baseline")
    assert result.accepted is True
