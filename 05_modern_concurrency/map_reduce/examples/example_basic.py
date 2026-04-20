from collections import defaultdict


def map_words(words: list[str]) -> list[tuple[str, int]]:
    return [(word, 1) for word in words]


def reduce_counts(pairs: list[tuple[str, int]]) -> dict[str, int]:
    result: dict[str, int] = defaultdict(int)
    for key, value in pairs:
        result[key] += value
    return dict(result)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    pairs = map_words(["a", "b", "a"])
    print(reduce_counts(pairs))


if __name__ == "__main__":
    main()
