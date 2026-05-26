from dataclasses import dataclass


@dataclass
class RuntimeComponent:
    name: str
    responsibility: str


def build_components() -> list[RuntimeComponent]:
    return [
        RuntimeComponent("RefCount", "Safe ownership tracking"),
        RuntimeComponent("GC", "Concurrent-safe cycle collection"),
        RuntimeComponent("Locks", "Shared-state protection"),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for component in build_components():
        print(f"{component.name}: {component.responsibility}")


if __name__ == "__main__":
    main()
