class Handler:
    def __init__(self, nxt: "Handler | None" = None) -> None:
        self.nxt = nxt

    def handle(self, level: int) -> str:
        if self.nxt:
            return self.nxt.handle(level)
        return "unhandled"


class WarnHandler(Handler):
    def handle(self, level: int) -> str:
        if level == 1:
            return "warn"
        return super().handle(level)


class ErrorHandler(Handler):
    def handle(self, level: int) -> str:
        if level >= 2:
            return "error"
        return super().handle(level)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    chain = WarnHandler(ErrorHandler())
    print(chain.handle(2))


if __name__ == "__main__":
    main()
