class RegistryMeta(type):
    registry: dict[str, type] = {}

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name != 'Base':
            mcls.registry[name] = cls
        return cls


class Base(metaclass=RegistryMeta):
    pass


class Service(Base):
    pass


def main() -> None:
    print(sorted(RegistryMeta.registry.keys()))


if __name__ == '__main__':
    main()
