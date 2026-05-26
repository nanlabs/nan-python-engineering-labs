class RegistryMeta(type):
    registry: dict[str, type] = {}

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if name != "Base":
            mcls.registry[name] = cls
        return cls


class Base(metaclass=RegistryMeta):
    kind = "base"


class Service(Base):
    kind = "service"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    summary = {name: cls.kind for name, cls in RegistryMeta.registry.items()}
    print(summary)


if __name__ == "__main__":
    main()
