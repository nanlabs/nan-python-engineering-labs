class Base:
    registry: list[type] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base.registry.append(cls)


class ChildA(Base):
    pass


class ChildB(Base):
    pass


def main() -> None:
    print([cls.__name__ for cls in Base.registry])


if __name__ == '__main__':
    main()
