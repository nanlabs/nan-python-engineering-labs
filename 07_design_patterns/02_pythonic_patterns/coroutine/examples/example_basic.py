def accumulator():
    total = 0
    while True:
        value = yield total
        total += value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    coro = accumulator()
    next(coro)
    print(coro.send(3))
    print(coro.send(4))


if __name__ == "__main__":
    main()
