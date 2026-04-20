from dataclasses import dataclass


@dataclass
class Model:
    name: str
    good_for: str


def build_models() -> list[Model]:
    return [
        Model("threading", "I/O concurrency"),
        Model("multiprocessing", "CPU-bound work"),
        Model("asyncio", "high-volume async I/O"),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for model in build_models():
        print(f"{model.name}: {model.good_for}")


if __name__ == "__main__":
    main()
