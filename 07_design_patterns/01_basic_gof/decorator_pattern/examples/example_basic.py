class Text:
    def render(self) -> str:
        return 'report'


class BoldDecorator:
    def __init__(self, inner: Text) -> None:
        self.inner = inner

    def render(self) -> str:
        return f"<b>{self.inner.render()}</b>"


class UpperDecorator:
    def __init__(self, inner: Text) -> None:
        self.inner = inner

    def render(self) -> str:
        return self.inner.render().upper()


def main() -> None:
    decorated = UpperDecorator(BoldDecorator(Text()))
    print(decorated.render())


if __name__ == '__main__':
    main()
