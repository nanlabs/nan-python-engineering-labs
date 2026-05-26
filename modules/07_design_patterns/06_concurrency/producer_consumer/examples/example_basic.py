from queue import Queue


def main() -> None:
    """Entry point to demonstrate the implementation."""
    q: Queue[int] = Queue()
    for item in [1, 2, 3]:
        q.put(item)
    out: list[int] = []
    while not q.empty():
        out.append(q.get() * 10)
    print(out)


if __name__ == "__main__":
    main()
