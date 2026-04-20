class NonEmpty:
    def __set_name__(self, owner: type, name: str) -> None:
        self.key = f"_{name}"

    def __get__(self, instance, owner=None):
        return getattr(instance, self.key)

    def __set__(self, instance, value: str):
        if not value.strip():
            raise ValueError("empty value")
        setattr(instance, self.key, value)


class Article:
    title = NonEmpty()

    def __init__(self, title: str) -> None:
        self.title = title


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Article("Patterns").title)


if __name__ == "__main__":
    main()
