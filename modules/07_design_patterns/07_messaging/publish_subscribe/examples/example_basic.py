class PubSub:
    def __init__(self) -> None:
        self.subs: list[callable] = []

    def subscribe(self, fn: callable) -> None:
        self.subs.append(fn)

    def publish(self, message: str) -> None:
        for sub in self.subs:
            sub(message)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    out: list[str] = []
    ps = PubSub()
    ps.subscribe(lambda m: out.append(m.upper()))
    ps.publish("event")
    print(out)


if __name__ == "__main__":
    main()
