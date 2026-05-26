import sys


def refcount_of(value: object) -> int:
    return sys.getrefcount(value)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    sample: list[int] = [1, 2, 3]
    before = refcount_of(sample)
    alias = sample
    after = refcount_of(sample)
    print(f"before={before}, after_alias={after}, same={alias is sample}")


if __name__ == "__main__":
    main()
