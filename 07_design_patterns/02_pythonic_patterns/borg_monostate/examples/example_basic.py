class Borg:
    _state: dict[str, object] = {}

    def __init__(self) -> None:
        self.__dict__ = self._state


def main() -> None:
    a = Borg()
    b = Borg()
    a.value = 10
    print(getattr(b, 'value'))


if __name__ == '__main__':
    main()
