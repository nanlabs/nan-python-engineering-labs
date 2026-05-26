class Descriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)


class Model:
    field = Descriptor()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    item = Model()
    item.field = "value"
    print(item.field)


if __name__ == "__main__":
    main()
