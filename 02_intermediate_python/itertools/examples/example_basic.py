"""Demonstrate practical itertools workflows for analytics."""

from itertools import accumulate, groupby, islice


def rolling_totals(values: list[int], window: int) -> list[int]:
    return [sum(values[i:i+window]) for i in range(len(values) - window + 1)]


def main() -> None:
    sales = [5, 8, 8, 3, 10, 10, 2]
    print("cumulative:", list(accumulate(sales)))
    print("first 4:", list(islice(sales, 4)))
    print("frequency:", [(k, len(list(g))) for k, g in groupby(sorted(sales))])
    print("rolling totals:", rolling_totals(sales, 3))


if __name__ == "__main__":
    main()
