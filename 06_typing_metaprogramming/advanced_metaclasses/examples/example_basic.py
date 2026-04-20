class ValidateAttrsMeta(type):
    def __new__(mcls, name, bases, namespace):
        required = namespace.get("required_attrs", [])
        for attr in required:
            if attr not in namespace:
                raise TypeError(f"missing required attr: {attr}")
        return super().__new__(mcls, name, bases, namespace)


class Plugin(metaclass=ValidateAttrsMeta):
    required_attrs = ["name"]
    name = "demo"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Plugin.name)


if __name__ == "__main__":
    main()
