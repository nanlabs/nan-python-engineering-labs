def maybe_immortal(value: object) -> bool:
    # In CPython, some singletons/objects may be immortalized internally.
    return value in (None, True, False, (), "")


def main() -> None:
    for candidate in [None, True, 10, "", "python"]:
        print(candidate, maybe_immortal(candidate))


if __name__ == "__main__":
    main()
