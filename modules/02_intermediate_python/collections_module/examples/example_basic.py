"""Working example of the collections module."""

from collections import Counter, defaultdict, deque


def main() -> None:
    """Entry point to demonstrate the implementation."""
    tickets = Counter(["open", "done", "open", "review"])
    grouped = defaultdict(list)
    grouped["backend"].append("FastAPI")
    grouped["data"].append("Polars")
    queue = deque(["first", "second"])
    queue.appendleft("zero")
    print(tickets)
    print(dict(grouped))
    print(list(queue))


if __name__ == "__main__":
    main()
