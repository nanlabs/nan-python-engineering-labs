"""Small pure functions are a great fit for Hypothesis."""

from __future__ import annotations


def collapse_whitespace(value: str) -> str:
    return " ".join(value.split())


def normalize_title(value: str) -> str:
    return collapse_whitespace(value).title()


if __name__ == "__main__":
    samples = ["  hello   world  ", "multiple\nlines\tinside", " already clean "]
    print("hypothesis intro example")
    for sample in samples:
        print(repr(sample), "->", repr(normalize_title(sample)))
