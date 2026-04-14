"""Working example of comprehensions."""


def even_squares(numbers: list[int]) -> list[int]:
    """Build a list of squares for even numbers."""
    return [number * number for number in numbers if number % 2 == 0]


def word_lengths(words: list[str]) -> dict[str, int]:
    """Build a word -> length dictionary."""
    return {word: len(word) for word in words}


def normalized_initials(words: list[str]) -> set[str]:
    """Build a set with uppercase initials."""
    return {word[0].upper() for word in words if word}


def main() -> None:
    words = ["python", "pytest", "pydantic"]
    print(even_squares([1, 2, 3, 4, 5, 6]))
    print(word_lengths(words))
    print(normalized_initials(words))


if __name__ == "__main__":
    main()
