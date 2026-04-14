class Saga:
    def __init__(self) -> None:
        self.steps: list[tuple[callable, callable]] = []

    def add(self, action: callable, compensation: callable) -> None:
        self.steps.append((action, compensation))

    def run(self) -> str:
        done: list[callable] = []
        try:
            for action, compensation in self.steps:
                action()
                done.append(compensation)
            return 'committed'
        except Exception:
            for comp in reversed(done):
                comp()
            return 'compensated'


def main() -> None:
    events: list[str] = []
    saga = Saga()
    saga.add(lambda: events.append('reserve'), lambda: events.append('undo_reserve'))
    saga.add(lambda: events.append('charge'), lambda: events.append('refund'))
    print(saga.run(), events)


if __name__ == '__main__':
    main()
