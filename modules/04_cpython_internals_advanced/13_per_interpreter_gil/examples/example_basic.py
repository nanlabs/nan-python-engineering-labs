from dataclasses import dataclass


@dataclass
class RuntimeMode:
    name: str
    parallel_bytecode: bool


def compare_modes() -> list[RuntimeMode]:
    return [
        RuntimeMode("legacy-global-gil", False),
        RuntimeMode("per-interpreter-gil", True),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for mode in compare_modes():
        print(f"{mode.name}: parallel_bytecode={mode.parallel_bytecode}")


if __name__ == "__main__":
    main()
