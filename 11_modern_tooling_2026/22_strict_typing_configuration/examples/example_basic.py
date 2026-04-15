"""Strict typing: demonstrate TypeVar, Protocol, and Literal usage."""
from typing import Literal, Protocol, TypeVar

T = TypeVar("T")
SortOrder = Literal["asc", "desc"]


class Sortable(Protocol):
    def __lt__(self, other: object) -> bool: ...


def sorted_typed(items: list[T], order: SortOrder = "asc") -> list[T]:
    result = sorted(items, key=lambda x: x)  # type: ignore[arg-type]
    return result if order == "asc" else list(reversed(result))


def main() -> None:
    nums: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]
    print(sorted_typed(nums, "asc"))
    print(sorted_typed(nums, "desc"))


if __name__ == "__main__":
    main()
