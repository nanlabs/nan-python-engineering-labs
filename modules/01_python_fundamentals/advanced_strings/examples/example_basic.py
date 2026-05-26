"""Working example of advanced strings."""


def build_slug(title: str) -> str:
    """Normalize a title so it can be used as a slug."""
    return "-".join(title.strip().lower().split())


def highlight_keyword(text: str, keyword: str) -> str:
    """Replace a keyword using string methods."""
    return text.replace(keyword, keyword.upper())


def format_progress(module: str, completed: int, total: int) -> str:
    """Use f-strings to build a readable progress report."""
    percentage = 0.0 if total == 0 else completed / total * 100
    return f"{module}: {completed}/{total} ({percentage:.1f}%)"


def main() -> None:
    """
    Run examples of advanced string manipulation.
    """
    print(build_slug("  Python Fundamentals Module  "))
    print(highlight_keyword("python makes automation fun", "automation"))
    print(format_progress("Module 01", 4, 12))


if __name__ == "__main__":
    main()
