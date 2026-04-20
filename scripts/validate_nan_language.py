#!/usr/bin/env python3
"""Fail if Spanish content is detected in NaN module files.

Usage:
  python scripts/validate_nan_language.py --module 11_modern_tooling_2026
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SPANISH_KEYWORDS = re.compile(
    r"\b("
    r"módulo|descripcion|descripción|objetivo|ejercicio|instrucciones|"
    r"referencias|enlaces|recursos|aprende|diseña|debes|requisitos|"
    r"ejemplo|solución|practica|práctica|implementa|función|"
    r"resolución|contribuciones|útiles"
    r")\b",
    re.IGNORECASE,
)


def iter_text_files(module_path: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(module_path.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".py"}:
            files.append(path)
    return files


def find_hits(module_path: Path) -> list[tuple[Path, int, str]]:
    hits: list[tuple[Path, int, str]] = []
    for file_path in iter_text_files(module_path):
        content = file_path.read_text(encoding="utf-8")
        for line_no, line in enumerate(content.splitlines(), 1):
            if SPANISH_KEYWORDS.search(line):
                hits.append((file_path, line_no, line.strip()))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--module",
        default="11_modern_tooling_2026",
        help="Module folder relative to repository root.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / args.module

    if not module_path.exists():
        print(f"ERROR: module path not found: {module_path}")
        return 2

    hits = find_hits(module_path)
    if not hits:
        print(f"OK: no Spanish keywords found in {args.module}")
        return 0

    print(f"FAIL: found {len(hits)} Spanish keyword hits in {args.module}")
    for file_path, line_no, line in hits[:200]:
        rel = file_path.relative_to(repo_root)
        print(f"  {rel}:{line_no}: {line}")
    if len(hits) > 200:
        print(f"  ... and {len(hits) - 200} more")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
