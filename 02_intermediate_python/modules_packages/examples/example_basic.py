"""Working example of modules and packages."""

from importlib import import_module
from types import ModuleType


def load_serializer(module_name: str) -> ModuleType:
    """Import a module dynamically and return it."""
    return import_module(module_name)


def summarize_module(module: ModuleType, attrs: list[str]) -> dict[str, bool]:
    return {name: hasattr(module, name) for name in attrs}


def main() -> None:
    json_module = load_serializer("json")
    print(json_module.dumps({"topic": "modules", "status": "ready"}))
    print(summarize_module(json_module, ["dumps", "loads", "missing_attr"]))


if __name__ == "__main__":
    main()
