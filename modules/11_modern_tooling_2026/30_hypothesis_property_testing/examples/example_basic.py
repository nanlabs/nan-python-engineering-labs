"""Hypothesis: property-based testing concepts demo."""


def reverse_list(items: list[int]) -> list[int]:
    return items[::-1]


def check_reverse_involution(items: list[int]) -> bool:
    return reverse_list(reverse_list(items)) == items


def check_length_preserved(items: list[int]) -> bool:
    return len(reverse_list(items)) == len(items)


def generate_test_cases() -> list[list[int]]:
    return [[], [1], [1, 2], [1, 2, 3, 4], list(range(20))]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    cases = generate_test_cases()
    for case in cases:
        involution = check_reverse_involution(case)
        length = check_length_preserved(case)
        print(f"case={case[:5]}... involution={involution} length_ok={length}")


if __name__ == "__main__":
    main()
