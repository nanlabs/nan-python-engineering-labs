"""Compare naive and optimized lookup strategies."""


def naive_lookup(values: list[int], targets: list[int]) -> int:
    found = 0
    for t in targets:
        if t in values:
            found += 1
    return found


def optimized_lookup(values: list[int], targets: list[int]) -> int:
    value_set = set(values)
    return sum(1 for t in targets if t in value_set)


def main() -> None:
    values = list(range(20000))
    targets = list(range(15000, 26000))

    print(f"Naive found:     {naive_lookup(values, targets)}")
    print(f"Optimized found: {optimized_lookup(values, targets)}")


if __name__ == '__main__':
    main()
