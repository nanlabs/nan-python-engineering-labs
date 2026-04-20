from collections import deque


def main() -> None:
    """Entry point to demonstrate the implementation."""
    tasks = deque(["a", "b", "c"])
    leaders = ["l1", "l2"]
    assignments: list[str] = []
    while tasks:
        for leader in leaders:
            if not tasks:
                break
            assignments.append(f"{leader}->{tasks.popleft()}")
    print(assignments)


if __name__ == "__main__":
    main()
