class Reactor:
    def __init__(self) -> None:
        self.handlers: dict[str, callable] = {}

    def register(self, event: str, fn: callable) -> None:
        self.handlers[event] = fn

    def dispatch(self, event: str, payload: str) -> str:
        return self.handlers[event](payload)


def main() -> None:
    reactor = Reactor()
    reactor.register('read', lambda p: f'read:{p}')
    print(reactor.dispatch('read', 'socket-1'))


if __name__ == '__main__':
    main()
