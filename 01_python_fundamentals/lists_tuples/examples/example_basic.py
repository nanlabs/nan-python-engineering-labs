"""Working example of lists and tuples."""


def rotate_tasks(tasks: list[str]) -> list[str]:
    """Move the first task to the end using slicing."""
    return tasks[1:] + tasks[:1]


def format_point(point: tuple[int, int]) -> str:
    """Unpack a tuple and convert it into readable text."""
    x, y = point
    return f"Point(x={x}, y={y})"


def main() -> None:
    tasks = ["read", "practice", "review"]
    print(rotate_tasks(tasks))
    print(format_point((3, 7)))


if __name__ == "__main__":
    main()
