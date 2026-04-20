class Base:
    registry: list[type] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base.registry.append(cls)


class ChildA(Base):
    role = "validator"


class ChildB(Base):
    role = "serializer"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    pairs = [(cls.__name__, cls.role) for cls in Base.registry]
    print(pairs)


if __name__ == "__main__":
    main()
