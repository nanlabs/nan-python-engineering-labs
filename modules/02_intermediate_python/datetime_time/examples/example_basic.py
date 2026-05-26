"""Working example of datetime and time."""

from datetime import datetime, timedelta


def schedule_next_review(start: datetime, days: int) -> datetime:
    """Return the next review date."""
    return start + timedelta(days=days)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    start = datetime(2026, 4, 13, 10, 30)
    next_review = schedule_next_review(start, 7)
    print(start.isoformat())
    print(next_review.isoformat())


if __name__ == "__main__":
    main()
