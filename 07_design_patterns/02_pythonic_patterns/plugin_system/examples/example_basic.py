class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, callable] = {}

    def register(self, name: str, fn: callable) -> None:
        self._plugins[name] = fn

    def run(self, name: str, value: str) -> str:
        return self._plugins[name](value)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    registry = PluginRegistry()
    registry.register("upper", str.upper)
    print(registry.run("upper", "hello"))


if __name__ == "__main__":
    main()
