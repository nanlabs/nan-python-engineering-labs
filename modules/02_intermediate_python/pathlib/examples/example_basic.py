"""Working example of pathlib."""

from pathlib import Path


def describe_path(path: Path) -> dict[str, str]:
    """Return a few useful path properties."""
    return {
        "name": path.name,
        "suffix": path.suffix,
        "parent": path.parent.name,
    }


def main() -> None:
    """Entry point to demonstrate the implementation."""
    path = Path("02_intermediate_python/pathlib/examples/example_basic.py")
    print(describe_path(path))
    print(path.with_name("notes.txt"))


if __name__ == "__main__":
    main()
