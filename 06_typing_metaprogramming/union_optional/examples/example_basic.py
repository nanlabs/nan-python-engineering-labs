"""Handle optional values and union return types safely."""


def parse_quantity(raw: str) -> int | None:
    text = raw.strip()
    return int(text) if text.isdigit() else None


def normalize_quantities(values: list[str]) -> list[int | None]:
    return [parse_quantity(value) for value in values]


def main() -> None:
    for raw in ["42", "abc", " 7"]:
        print(raw, "->", parse_quantity(raw))
    print("batch:", normalize_quantities(["1", "x", "22"]))


if __name__ == "__main__":
    main()
