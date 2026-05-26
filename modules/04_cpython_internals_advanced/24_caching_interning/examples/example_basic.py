import sys


def compare_strings(left: str, right: str) -> tuple[bool, bool]:
    return left == right, left is right


def main() -> None:
    """Entry point to demonstrate the implementation."""
    a = sys.intern("free_threading")
    b = sys.intern("free_" + "threading")
    equals, identical = compare_strings(a, b)
    print(f"equals={equals}, identical={identical}")


if __name__ == "__main__":
    main()
