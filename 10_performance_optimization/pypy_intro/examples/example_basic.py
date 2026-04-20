"""Object allocation workload commonly improved in PyPy."""


class Event:
    def __init__(self, user_id: int, value: int) -> None:
        self.user_id = user_id
        self.value = value


def aggregate_events(count: int) -> dict[int, int]:
    totals: dict[int, int] = {}
    for i in range(count):
        event = Event(i % 200, i)
        totals[event.user_id] = totals.get(event.user_id, 0) + event.value
    return totals


def main() -> None:
    """Entry point to demonstrate the implementation."""
    totals = aggregate_events(50000)
    print(f"Users aggregated: {len(totals)}")
    print(f"Sample user 10 total: {totals.get(10, 0)}")


if __name__ == "__main__":
    main()
