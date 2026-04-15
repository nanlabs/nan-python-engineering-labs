"""Ruff formatter: Black-compatible formatting demo."""


def normalize_code(code: str) -> str:
    lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if stripped.startswith("def ") and not stripped.endswith(":"):
            stripped += ":"
        lines.append(stripped)
    return "\n".join(lines)


MESSY = "def   add( a,b ) : return a+b"


def format_differences(original: str, formatted: str) -> list[str]:
    orig_lines = original.splitlines()
    fmt_lines = formatted.splitlines()
    diffs = []
    for i, (o, f) in enumerate(zip(orig_lines, fmt_lines)):
        if o != f:
            diffs.append(f"line {i+1}: {o!r} → {f!r}")
    return diffs


def main() -> None:
    normalized = normalize_code(MESSY)
    diffs = format_differences(MESSY, normalized)
    print(f"Original: {MESSY!r}")
    print(f"Formatted: {normalized!r}")
    for d in diffs or ["No textual diffs (already formatted)"]:
        print(f"  {d}")


if __name__ == "__main__":
    main()
