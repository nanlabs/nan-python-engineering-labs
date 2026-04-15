"""Ruff as import sorter: mimic isort section grouping."""


def sort_imports(imports: list[str]) -> dict[str, list[str]]:
    stdlib_mods = {"os", "sys", "re", "pathlib", "typing", "collections", "subprocess"}
    first_party = {"myapp", "mylib"}
    groups: dict[str, list[str]] = {"stdlib": [], "third_party": [], "first_party": [], "local": []}
    for imp in imports:
        name = imp.split()[1].split(".")[0]
        if name in stdlib_mods:
            groups["stdlib"].append(imp)
        elif name in first_party:
            groups["first_party"].append(imp)
        elif imp.startswith("from .") or imp.startswith("import ."):
            groups["local"].append(imp)
        else:
            groups["third_party"].append(imp)
    return groups


def main() -> None:
    imports = [
        "import os", "import httpx", "from myapp import models",
        "import sys", "from . import utils", "import pydantic",
    ]
    grouped = sort_imports(imports)
    for section, lines in grouped.items():
        if lines:
            print(f"# {section}")
            for line in sorted(lines):
                print(f"  {line}")


if __name__ == "__main__":
    main()
