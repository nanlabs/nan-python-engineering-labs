"""Illustrate a few invariants for list transformations."""

from __future__ import annotations

from collections import Counter


def rotate_list(values: list[int], steps: int) -> list[int]:
    if not values:
        return []
    shift = steps % len(values)
    return values[-shift:] + values[:-shift]


if __name__ == "__main__":
    values = [1, 2, 3, 4]
    rotated = rotate_list(values, 1)
    print("property based testing example")
    print(f"rotated: {rotated}")
    print(f"same multiset: {Counter(values) == Counter(rotated)}")
