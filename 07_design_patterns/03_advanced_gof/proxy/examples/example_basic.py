class Image:
    def show(self) -> str:
        raise NotImplementedError


class RealImage(Image):
    def __init__(self, path: str) -> None:
        self.path = path

    def show(self) -> str:
        return f'loaded:{self.path}'


class LazyImageProxy(Image):
    def __init__(self, path: str) -> None:
        self.path = path
        self._real: RealImage | None = None

    def show(self) -> str:
        if self._real is None:
            self._real = RealImage(self.path)
        return self._real.show()


def main() -> None:
    print(LazyImageProxy('chart.png').show())


if __name__ == '__main__':
    main()
