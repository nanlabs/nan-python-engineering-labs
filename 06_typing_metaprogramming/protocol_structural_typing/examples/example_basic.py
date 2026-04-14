from typing import Protocol


class SupportsLen(Protocol):
    def __len__(self) -> int: ...


def size_of(value: SupportsLen) -> int:
    return len(value)


def main() -> None:
    print(size_of('hello'))


if __name__ == '__main__':
    main()
