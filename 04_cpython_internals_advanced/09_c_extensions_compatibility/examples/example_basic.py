from dataclasses import dataclass


@dataclass
class ExtensionCheck:
    name: str
    gil_safe: bool


def classify_extension(name: str, gil_safe: bool) -> ExtensionCheck:
    return ExtensionCheck(name=name, gil_safe=gil_safe)


def main() -> None:
    checks = [
        classify_extension("numpy", True),
        classify_extension("legacy_ext", False),
    ]
    for check in checks:
        print(f"{check.name}: gil_safe={check.gil_safe}")


if __name__ == "__main__":
    main()
