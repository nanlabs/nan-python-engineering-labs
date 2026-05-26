class Backlog:
    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __iter__(self):
        for item in self.items:
            yield item


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for task in Backlog(["design", "build", "test"]):
        print(task)


if __name__ == "__main__":
    main()
