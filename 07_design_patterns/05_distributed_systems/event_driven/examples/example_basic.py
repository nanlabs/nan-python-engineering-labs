class EventBus:
    def __init__(self) -> None:
        self.handlers: dict[str, list[callable]] = {}

    def on(self, event: str, fn: callable) -> None:
        self.handlers.setdefault(event, []).append(fn)

    def emit(self, event: str, payload: str) -> None:
        for fn in self.handlers.get(event, []):
            fn(payload)


def main() -> None:
    out: list[str] = []
    bus = EventBus()
    bus.on('user_created', lambda x: out.append(x.upper()))
    bus.emit('user_created', 'ada')
    print(out)


if __name__ == '__main__':
    main()
