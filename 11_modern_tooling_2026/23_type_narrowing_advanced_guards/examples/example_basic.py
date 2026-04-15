"""Advanced type narrowing with TypeGuard and isinstance chains."""
from typing import TypeGuard, Union


def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in val)


def process_items(items: list[Union[int, str]]) -> tuple[list[int], list[str]]:
    ints: list[int] = []
    strs: list[str] = []
    for item in items:
        if isinstance(item, int):
            ints.append(item)
        else:
            strs.append(item)
    return ints, strs


def main() -> None:
    mixed: list[Union[int, str]] = [1, "a", 2, "b", 3]
    integers, strings = process_items(mixed)
    print(f"integers={integers}")
    print(f"strings={strings}")
    raw: list[object] = ["x", "y", "z"]
    print(f"is_string_list={is_string_list(raw)}")


if __name__ == "__main__":
    main()
