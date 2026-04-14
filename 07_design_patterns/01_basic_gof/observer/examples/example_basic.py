class Topic:
    def __init__(self) -> None:
        self._subs: list[callable] = []

    def subscribe(self, fn: callable) -> None:
        self._subs.append(fn)

    def notify(self, event: str) -> None:
        for sub in self._subs:
            sub(event)


def main() -> None:
    events: list[str] = []
    topic = Topic()
    topic.subscribe(lambda e: events.append(f'a:{e}'))
    topic.subscribe(lambda e: events.append(f'b:{e}'))
    topic.notify('build_done')
    print(events)


if __name__ == '__main__':
    main()
