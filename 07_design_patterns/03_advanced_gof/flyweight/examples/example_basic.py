class GlyphFactory:
    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def get(self, char: str) -> str:
        if char not in self.cache:
            self.cache[char] = f"glyph:{char}"
        return self.cache[char]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    factory = GlyphFactory()
    a1 = factory.get("a")
    a2 = factory.get("a")
    print(a1 is a2, len(factory.cache))


if __name__ == "__main__":
    main()
