class EventBus:
    def __init__(self) -> None:
        self.subs: dict[str, list[callable]] = {}

    def subscribe(self, topic: str, fn: callable) -> None:
        self.subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, payload: str) -> None:
        for fn in self.subs.get(topic, []):
            fn(payload)


def main() -> None:
    out: list[str] = []
    bus = EventBus()
    bus.subscribe('build', lambda x: out.append(x))
    bus.publish('build', 'ok')
    print(out)


if __name__ == '__main__':
    main()
