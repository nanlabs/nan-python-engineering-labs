from typing import Callable, Iterable


def apply_all(values: Iterable[int], fn: Callable[[int], int]) -> list[int]:
    return [fn(value) for value in values]


def main() -> None:
    print(apply_all([1, 2, 3], lambda x: x * 10))


if __name__ == '__main__':
    main()
