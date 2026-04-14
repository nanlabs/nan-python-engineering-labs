class UnitOfWork:
    def __init__(self) -> None:
        self._ops: list[str] = []

    def register(self, op: str) -> None:
        self._ops.append(op)

    def commit(self) -> list[str]:
        applied = list(self._ops)
        self._ops.clear()
        return applied


def main() -> None:
    uow = UnitOfWork()
    uow.register('insert user')
    uow.register('insert order')
    print(uow.commit())


if __name__ == '__main__':
    main()
