class Borg:
    """
    Borg (also known as Monostate) is a design pattern that allows
    multiple instances of a class to share the same state.
    This is achieved by having all instances share the same __dict__,
    which holds the instance attributes
    """

    _state: dict[str, object] = {}

    def __init__(self) -> None:
        self.__dict__ = self._state


def main() -> None:
    """
    In this example, we create two instances of the Borg class, `a` and `b`.
    When we set an attribute `value` on instance `a`, it is actually stored
    in the shared state dictionary. Therefore,
    when we access `value` from instance `b
    """
    a = Borg()
    b = Borg()
    a.value = 10
    print(b.value)


if __name__ == "__main__":
    main()
