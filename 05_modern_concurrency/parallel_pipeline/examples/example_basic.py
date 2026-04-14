def stage_one(values: list[int]) -> list[int]:
    return [value * 2 for value in values]


def stage_two(values: list[int]) -> list[int]:
    return [value + 1 for value in values]


def main() -> None:
    values = stage_one([1, 2, 3])
    print(stage_two(values))


if __name__ == '__main__':
    main()
