class SortStrategy:
    def sort(self, items: list[int]) -> list[int]:
        raise NotImplementedError


class AscSort(SortStrategy):
    def sort(self, items: list[int]) -> list[int]:
        return sorted(items)


class DescSort(SortStrategy):
    def sort(self, items: list[int]) -> list[int]:
        return sorted(items, reverse=True)


def run_sort(strategy: SortStrategy, values: list[int]) -> list[int]:
    return strategy.sort(values)


def main() -> None:
    print(run_sort(DescSort(), [3, 1, 2]))


if __name__ == '__main__':
    main()
