class Report:
    def __init__(self, raw: list[int]) -> None:
        self.raw = raw

    @property
    def total(self) -> int:
        if not hasattr(self, '_cached_total'):
            self._cached_total = sum(self.raw)
        return self._cached_total


def main() -> None:
    report = Report([1, 2, 3])
    print(report.total, report.total)


if __name__ == '__main__':
    main()
