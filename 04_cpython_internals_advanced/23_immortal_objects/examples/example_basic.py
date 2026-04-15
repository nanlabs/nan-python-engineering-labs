def maybe_immortal(value: object) -> bool:
    return value in (None, True, False, (), "")


def classify_values(values: list[object]) -> list[tuple[object, bool]]:
    return [(value, maybe_immortal(value)) for value in values]


def main() -> None:
    sample = [None, True, 10, "", "python"]
    for candidate, immortal in classify_values(sample):
        print(candidate, immortal)


if __name__ == "__main__":
    main()
