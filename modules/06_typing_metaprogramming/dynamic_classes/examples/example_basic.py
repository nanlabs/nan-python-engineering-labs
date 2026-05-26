"""Create classes dynamically with type()."""


def describe(self) -> str:
    return f"{self.name} ({self.category})"


def build_product_class():
    def init(self, name: str, category: str) -> None:
        self.name = name
        self.category = category

    return type("Product", (), {"__init__": init, "describe": describe})


def main() -> None:
    """Entry point to demonstrate the implementation."""
    Product = build_product_class()
    item = Product("Mechanical Keyboard", "Accessories")
    print(item.describe())


if __name__ == "__main__":
    main()
