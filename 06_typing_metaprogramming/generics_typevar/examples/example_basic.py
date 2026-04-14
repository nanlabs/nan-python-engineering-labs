from typing import TypeVar


T = TypeVar('T')


def first(items: list[T]) -> T:
    if not items:
        raise ValueError('items cannot be empty')
    return items[0]


def main() -> None:
    print(first(['a', 'b']))


if __name__ == '__main__':
    main()
