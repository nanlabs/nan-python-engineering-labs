#!/usr/bin/env python3
"""Audit NaN learning modules for English compliance and duplication.

Checks by module:
- C1: Spanish content hits in .md/.py
- C2: Spanish file-name hits
- C3: Spanish directory-slug hits
- C4: ES/EN duplicate pairs in same directory
- C5: Canonical topic structure ratio

Usage:
  python scripts/audit_nan_modules.py
  python scripts/audit_nan_modules.py --module 10_performance_optimization
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

SPANISH_CONTENT_RE = re.compile(
    r"\b("
    r"m[oó]dulo|descripci[oó]n|objetivo|ejercicio|instrucciones|"
    r"referencias|documentaci[oó]n|configuraci[oó]n|instalaci[oó]n|"
    r"verificaci[oó]n|avanzad[oa]s?|paraleli[sz]aci[oó]n|"
    r"entornos|herramientas|soluci[oó]n|a[ñn]adir|"
    r"lee atentamente|tu solution|debe ir|directorio padre|"
    r"documentaci[oó]n oficial|implementar y practicar"
    r")\b",
    re.IGNORECASE,
)

SPANISH_NAME_RE = re.compile(
    r"(ejercicio|solucion|referencias|instalacion|configuracion|"
    r"avanzad|seguridad|paralelizacion|comparacion|tipado)",
    re.IGNORECASE,
)

EN_TO_ES_STEM = {
    "exercise": "ejercicio",
    "references": "referencias",
    "solution": "solucion",
    "installation": "instalacion",
    "configuration": "configuracion",
}

REQUIRED_TOPIC_FILES = [
    "README.md",
    "examples/example_basic.py",
    "exercises/exercise_01.py",
    "tests/test_basic.py",
    "references/links.md",
    "my_solution/.gitkeep",
]


@dataclass
class ModuleAudit:
    module: str
    c1_spanish_content_hits: int
    c2_spanish_filename_hits: int
    c3_spanish_directory_hits: int
    c4_duplicate_pairs: int
    c5_canonical_topics_ok: int
    c5_canonical_topics_total: int


@dataclass
class Hit:
    path: str
    line: int
    snippet: str


def iter_modules(repo_root: Path) -> list[Path]:
    return sorted(
        path for path in repo_root.iterdir() if path.is_dir() and re.match(r"^\d{2}_", path.name)
    )


def iter_learning_files(module_dir: Path) -> list[Path]:
    files: list[Path] = []

    # Module-level README is part of learning content.
    module_readme = module_dir / "README.md"
    if module_readme.exists():
        files.append(module_readme)

    # Only include topic learning assets to avoid false positives in helper scripts.
    for topic in detect_topic_dirs(module_dir):
        topic_readme = topic / "README.md"
        if topic_readme.exists():
            files.append(topic_readme)

        for subdir in ["examples", "exercises", "tests", "references"]:
            base = topic / subdir
            if not base.exists():
                continue
            for path in base.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".py"}:
                    files.append(path)

    return sorted(set(files))


def count_spanish_content(files: list[Path], repo_root: Path) -> tuple[int, list[Hit]]:
    count = 0
    hits: list[Hit] = []
    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(content.splitlines(), 1):
            if SPANISH_CONTENT_RE.search(line):
                count += 1
                if len(hits) < 200:
                    hits.append(
                        Hit(
                            path=str(file_path.relative_to(repo_root)),
                            line=line_no,
                            snippet=line.strip(),
                        )
                    )
    return count, hits


def count_spanish_file_names(files: list[Path]) -> int:
    return sum(1 for file_path in files if SPANISH_NAME_RE.search(file_path.stem))


def count_spanish_dir_names(module_dir: Path) -> int:
    dirs = {
        path
        for path in module_dir.rglob("*")
        if path.is_dir() and SPANISH_NAME_RE.search(path.name)
    }
    return len(dirs)


def detect_duplicate_pairs(module_dir: Path) -> int:
    pairs = 0
    for dir_path in [p for p in module_dir.rglob("*") if p.is_dir()]:
        names = [p.stem.lower() for p in dir_path.iterdir() if p.is_file()]
        for en_stem, es_stem in EN_TO_ES_STEM.items():
            en_exists = any(name.startswith(en_stem) for name in names)
            es_exists = any(name.startswith(es_stem) for name in names)
            if en_exists and es_exists:
                pairs += 1
    return pairs


def detect_topic_dirs(module_dir: Path) -> list[Path]:
    topics: list[Path] = []
    for path in module_dir.rglob("*"):
        if not path.is_dir():
            continue
        if path == module_dir:
            continue
        if (path / "README.md").exists() and any(
            (path / seg).exists() for seg in ["examples", "exercises", "tests"]
        ):
            topics.append(path)
    return sorted(set(topics))


def canonical_topic_ratio(module_dir: Path) -> tuple[int, int]:
    topics = detect_topic_dirs(module_dir)
    if not topics:
        return 0, 0

    ok = 0
    for topic in topics:
        if all((topic / rel).exists() for rel in REQUIRED_TOPIC_FILES):
            ok += 1
    return ok, len(topics)


def audit_module(module_dir: Path, repo_root: Path) -> tuple[ModuleAudit, list[Hit]]:
    files = iter_learning_files(module_dir)
    c1_hits, samples = count_spanish_content(files, repo_root)
    c2_hits = count_spanish_file_names(files)
    c3_hits = count_spanish_dir_names(module_dir)
    c4_hits = detect_duplicate_pairs(module_dir)
    c5_ok, c5_total = canonical_topic_ratio(module_dir)

    return (
        ModuleAudit(
            module=module_dir.name,
            c1_spanish_content_hits=c1_hits,
            c2_spanish_filename_hits=c2_hits,
            c3_spanish_directory_hits=c3_hits,
            c4_duplicate_pairs=c4_hits,
            c5_canonical_topics_ok=c5_ok,
            c5_canonical_topics_total=c5_total,
        ),
        samples,
    )


def markdown_table(rows: list[ModuleAudit]) -> str:
    lines = [
        "| module | C1 hits | C2 names | C3 dirs | C4 dup pairs | C5 canonical |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        ratio = f"{row.c5_canonical_topics_ok}/{row.c5_canonical_topics_total}"
        lines.append(
            f"| {row.module} | {row.c1_spanish_content_hits} | {row.c2_spanish_filename_hits} | "
            f"{row.c3_spanish_directory_hits} | {row.c4_duplicate_pairs} | {ratio} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", help="Single module to audit, e.g. 10_performance_optimization")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    modules = iter_modules(repo_root)
    if args.module:
        modules = [m for m in modules if m.name == args.module]

    audits: list[ModuleAudit] = []
    sample_hits: list[Hit] = []
    for module_dir in modules:
        audit, samples = audit_module(module_dir, repo_root)
        audits.append(audit)
        sample_hits.extend(samples)

    if args.json:
        print(json.dumps([asdict(a) for a in audits], indent=2))
        return 0

    print(markdown_table(audits))
    print("\nSample content hits:")
    for hit in sample_hits[:30]:
        print(f"- {hit.path}:{hit.line}: {hit.snippet}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
