from typing import overload


@overload
def stringify(value: int) -> str: ...


@overload
def stringify(value: list[int]) -> str: ...


def stringify(value):
    if isinstance(value, list):
        return ','.join(str(x) for x in value)
    return str(value)


def main() -> None:
    print(stringify(10))
    print(stringify([1, 2, 3]))


if __name__ == '__main__':
    main()
