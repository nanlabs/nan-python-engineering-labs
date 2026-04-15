"""Lazy data pipeline using generators."""


def source(limit: int):
    for i in range(limit):
        yield i


def even_squares(values):
    for v in values:
        if v % 2 == 0:
            yield v * v


def main() -> None:
    pipeline = even_squares(source(20))
    first_five = [next(pipeline) for _ in range(5)]
    print(f"First lazy results: {first_five}")


if __name__ == '__main__':
    main()
