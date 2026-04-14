def chunked(values: list[int], size: int):
    for idx in range(0, len(values), size):
        yield values[idx: idx + size]


def main() -> None:
    print(list(chunked([1, 2, 3, 4, 5], 2)))


if __name__ == '__main__':
    main()
