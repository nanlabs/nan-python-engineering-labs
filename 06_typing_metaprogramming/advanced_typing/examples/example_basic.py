from typing import Callable, Iterable, TypeVar


T = TypeVar("T")


def apply_all(values: Iterable[T], fn: Callable[[T], T]) -> list[T]:
    return [fn(value) for value in values]


def main() -> None:
    doubled = apply_all([1, 2, 3], lambda x: x * 2)
    upper = apply_all(["a", "b"], lambda s: s.upper())
    print(doubled)
    print(upper)


if __name__ == "__main__":
    main()
