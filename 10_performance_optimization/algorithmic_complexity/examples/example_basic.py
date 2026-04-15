"""Compare O(n^2) and O(n) pair search approaches."""


def find_pair_bruteforce(values: list[int], target: int) -> tuple[int, int] | None:
    for i, a in enumerate(values):
        for j in range(i + 1, len(values)):
            if a + values[j] == target:
                return i, j
    return None


def find_pair_hash(values: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, value in enumerate(values):
        needed = target - value
        if needed in seen:
            return seen[needed], i
        seen[value] = i
    return None


def main() -> None:
    values = [4, 7, 1, 9, 3, 11]
    target = 10
    print(f"Bruteforce: {find_pair_bruteforce(values, target)}")
    print(f"Hash-based: {find_pair_hash(values, target)}")


if __name__ == '__main__':
    main()
