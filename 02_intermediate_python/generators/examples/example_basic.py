"""Working example of generators."""


def rolling_average(values: list[int]):
    """Yield a rolling average after each new value."""
    total = 0
    for index, value in enumerate(values, start=1):
        total += value
        yield round(total / index, 2)


def main() -> None:
    print(list(rolling_average([10, 20, 15, 25])))


if __name__ == '__main__':
    main()
