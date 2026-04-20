"""Working example of exception handling."""


class InvalidGradeError(ValueError):
    """Raised when a grade is outside the accepted range."""


def normalize_grade(raw_value: str) -> int:
    """Convert and validate a grade."""
    try:
        grade = int(raw_value)
    except ValueError as error:
        raise InvalidGradeError("grade must be numeric") from error

    if not 0 <= grade <= 100:
        raise InvalidGradeError("grade must be between 0 and 100")
    return grade


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for raw_value in ["85", "101", "oops"]:
        try:
            print(normalize_grade(raw_value))
        except InvalidGradeError as error:
            print(f"handled error: {error}")


if __name__ == "__main__":
    main()
