"""Working example of text file handling."""

from pathlib import Path
from tempfile import TemporaryDirectory


def count_non_empty_lines(file_path: Path) -> int:
    """Count non-empty lines in a text file."""
    return sum(1 for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> None:
    """Entry point to demonstrate the implementation."""
    with TemporaryDirectory() as temp_dir:
        notes_path = Path(temp_dir) / "notes.txt"
        notes_path.write_text("first line\n\nsecond line\nthird line\n", encoding="utf-8")
        print(notes_path.read_text(encoding="utf-8"))
        print(f"non-empty lines: {count_non_empty_lines(notes_path)}")


if __name__ == "__main__":
    main()
