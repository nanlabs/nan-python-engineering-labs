#!/usr/bin/env python3
"""Unified validation script for all lab modules.

Checks per module (NaN repo):
  L1  Language  — 0 Spanish keywords in any .md/.py file
  S1  Structure — 6 canonical files exist in every topic
  R1  References — references/links.md has ≥3 real https:// URLs, no placeholder
  X1  Examples  — examples/example_basic.py executes without error
  E1  Exercises — exercise/exercise_01.py has no TODO / no Spanish keywords
  M1  README    — topic README has ≥18 headings

Exit code 0 if all checks pass, 1 if any fail.

Usage:
  python scripts/validate_all_modules.py
  python scripts/validate_all_modules.py --module 14_advanced_python_2026
  python scripts/validate_all_modules.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

PYTHON = sys.executable  # Use the same python running this script

CANONICAL_FILES = [
    "README.md",
    "examples/example_basic.py",
    "exercise/exercise_01.py",
    "tests/test_basic.py",
    "references/links.md",
]

SPANISH_KEYWORDS_RE = re.compile(
    r"\b("
    r"m[oó]dulo|descripci[oó]n|objetivo|ejercicio|instrucciones|"
    r"referencias|documentaci[oó]n|configuraci[oó]n|instalaci[oó]n|"
    r"verificaci[oó]n|avanzad[oa]s?|paraleli[sz]aci[oó]n|"
    r"entornos|herramientas|soluci[oó]n|a[ñn]adir|"
    r"implementar y practicar|lee atentamente|tu solution|"
    r"debe ir|directorio padre|implementa|añade|resuelve|"
    r"aprende|dise[ñn]a|debes|requisitos"
    r")\b",
    re.IGNORECASE,
)

REFERENCES_PLACEHOLDER_RE = re.compile(
    r"add relevant documentation links here|agregar enlaces",
    re.IGNORECASE,
)

EXAMPLE_TIMEOUT = 10  # seconds per example

# ── Data structures ───────────────────────────────────────────────────────────


@dataclass
class CheckResult:
    passed: bool
    details: list[str] = field(default_factory=list)


@dataclass
class TopicResult:
    topic: str
    s1: CheckResult = field(default_factory=lambda: CheckResult(True))
    r1: CheckResult = field(default_factory=lambda: CheckResult(True))
    x1: CheckResult = field(default_factory=lambda: CheckResult(True))
    e1: CheckResult = field(default_factory=lambda: CheckResult(True))
    m1: CheckResult = field(default_factory=lambda: CheckResult(True))

    def all_passed(self) -> bool:
        return all(
            r.passed for r in [self.s1, self.r1, self.x1, self.e1, self.m1]
        )


@dataclass
class ModuleResult:
    module: str
    l1: CheckResult = field(default_factory=lambda: CheckResult(True))
    topics: list[TopicResult] = field(default_factory=list)

    def all_passed(self) -> bool:
        return self.l1.passed and all(t.all_passed() for t in self.topics)

    def topic_counts(self) -> tuple[int, int]:
        total = len(self.topics)
        ok = sum(1 for t in self.topics if t.all_passed())
        return ok, total


# ── Helpers ───────────────────────────────────────────────────────────────────


def iter_modules(repo_root: Path, only_module: str | None) -> list[Path]:
    all_modules = sorted(
        p for p in repo_root.iterdir()
        if p.is_dir() and re.match(r"^\d{2}_", p.name)
    )
    if only_module:
        return [m for m in all_modules if m.name == only_module]
    return all_modules


def detect_topic_dirs(module_dir: Path) -> list[Path]:
    """Return all topic dirs: direct children with README.md + examples/ OR exercise/."""
    topics: list[Path] = []
    for path in sorted(module_dir.iterdir()):
        if not path.is_dir():
            continue
        if (path / "README.md").exists() and (
            (path / "examples").exists() or (path / "exercise").exists()
        ):
            topics.append(path)
        else:
            # Nested structure: look one level deeper (e.g. 07_design_patterns/01_basic_gof/singleton)
            for sub in sorted(path.iterdir()):
                if sub.is_dir() and (sub / "README.md").exists() and (
                    (sub / "examples").exists() or (sub / "exercise").exists()
                ):
                    topics.append(sub)
    return topics


def iter_text_files(root: Path) -> list[Path]:
    """Return .md/.py files that are learning assets (excludes module-root helper scripts)."""
    files = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in {".md", ".py"}:
            continue
        # Only include files inside topic subdirectories (depth ≥ 2 from module root)
        # This excludes module-root helper scripts like create_templates.py, generate_*.py
        rel = p.relative_to(root)
        if len(rel.parts) < 2:
            continue  # skip module-root scripts
        files.append(p)
    return sorted(files)


# ── L1: Language check (NaN repo) ─────────────────────────────────────────────


def check_l1_language(module_dir: Path, repo_root: Path) -> CheckResult:
    hits: list[str] = []
    for f in iter_text_files(module_dir):
        for lineno, line in enumerate(
            f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if SPANISH_KEYWORDS_RE.search(line):
                rel = f.relative_to(repo_root)
                hits.append(f"  {rel}:{lineno}: {line.strip()[:80]}")
                if len(hits) >= 20:
                    hits.append("  ... (truncated)")
                    return CheckResult(False, hits)
    return CheckResult(len(hits) == 0, hits)


# ── S1: Canonical structure ───────────────────────────────────────────────────


def check_s1_structure(topic_dir: Path) -> CheckResult:
    missing = [f for f in CANONICAL_FILES if not (topic_dir / f).exists()]
    return CheckResult(len(missing) == 0, [f"  missing: {m}" for m in missing])


# ── R1: References quality ────────────────────────────────────────────────────


def check_r1_references(topic_dir: Path) -> CheckResult:
    links_file = topic_dir / "references" / "links.md"
    if not links_file.exists():
        return CheckResult(False, ["  references/links.md not found"])

    content = links_file.read_text(encoding="utf-8", errors="ignore")

    # Check for placeholder
    if REFERENCES_PLACEHOLDER_RE.search(content):
        return CheckResult(False, ["  contains placeholder text"])

    # Count real https:// URLs
    urls = re.findall(r"https://\S+", content)
    if len(urls) < 3:
        return CheckResult(
            False, [f"  only {len(urls)} https:// URL(s) found (need ≥3)"]
        )

    return CheckResult(True)


# ── X1: Example execution ─────────────────────────────────────────────────────


def check_x1_example(topic_dir: Path) -> CheckResult:
    example = topic_dir / "examples" / "example_basic.py"
    if not example.exists():
        return CheckResult(False, ["  examples/example_basic.py not found"])

    try:
        result = subprocess.run(
            [PYTHON, str(example)],
            capture_output=True,
            timeout=EXAMPLE_TIMEOUT,
            text=True,
        )
        if result.returncode != 0:
            err = (result.stdout + result.stderr).strip()[:120]
            return CheckResult(False, [f"  exit {result.returncode}: {err}"])
        return CheckResult(True)
    except subprocess.TimeoutExpired:
        return CheckResult(False, [f"  timeout after {EXAMPLE_TIMEOUT}s"])
    except Exception as exc:  # noqa: BLE001
        return CheckResult(False, [f"  error: {exc}"])


# ── E1: Exercise quality ───────────────────────────────────────────────────────


TODO_RE = re.compile(r"\bTODO\b", re.IGNORECASE)


def check_e1_exercise(topic_dir: Path) -> CheckResult:
    exercise = topic_dir / "exercise" / "exercise_01.py"
    if not exercise.exists():
        return CheckResult(False, ["  exercise/exercise_01.py not found"])

    content = exercise.read_text(encoding="utf-8", errors="ignore")
    issues: list[str] = []

    if TODO_RE.search(content):
        issues.append("  contains TODO placeholder")

    # Spanish in exercises (stricter keywords for code files)
    exercise_spanish_re = re.compile(
        r"\b(objetivo|instrucciones|ejercicio|implementa|a[ñn]ade|resuelve|"
        r"descripci[oó]n|soluci[oó]n|practica|debes)\b",
        re.IGNORECASE,
    )
    for lineno, line in enumerate(content.splitlines(), 1):
        if exercise_spanish_re.search(line):
            issues.append(f"  line {lineno}: Spanish keyword: {line.strip()[:70]}")
            if len(issues) >= 5:
                break

    return CheckResult(len(issues) == 0, issues)


# ── M1: README heading schema ─────────────────────────────────────────────────


def check_m1_readme(topic_dir: Path) -> CheckResult:
    readme = topic_dir / "README.md"
    if not readme.exists():
        return CheckResult(False, ["  README.md not found"])

    content = readme.read_text(encoding="utf-8", errors="ignore")
    headings = re.findall(r"^#{1,3} ", content, re.MULTILINE)
    count = len(headings)
    if count < 18:
        return CheckResult(False, [f"  only {count} headings (need ≥18)"])
    return CheckResult(True)


# ── Module validation ─────────────────────────────────────────────────────────


def validate_module(module_dir: Path, repo_root: Path, is_nan: bool) -> ModuleResult:
    result = ModuleResult(module=module_dir.name)

    # L1: whole-module language scan (NaN only)
    if is_nan:
        result.l1 = check_l1_language(module_dir, repo_root)

    topics = detect_topic_dirs(module_dir)
    for topic_dir in topics:
        tr = TopicResult(topic=topic_dir.name)
        tr.s1 = check_s1_structure(topic_dir)
        tr.r1 = check_r1_references(topic_dir)
        tr.x1 = check_x1_example(topic_dir)
        tr.e1 = check_e1_exercise(topic_dir)
        tr.m1 = check_m1_readme(topic_dir)
        result.topics.append(tr)

    return result


# ── Reporting ─────────────────────────────────────────────────────────────────


def icon(passed: bool) -> str:
    return "✅" if passed else "❌"


def print_results(results: list[ModuleResult], is_nan: bool, verbose: bool) -> int:
    total_modules = len(results)
    failed_modules = 0

    for mod in results:
        ok, total = mod.topic_counts()
        l1_col = f" L1{icon(mod.l1.passed)}" if is_nan else ""
        all_ok = mod.all_passed()
        if not all_ok:
            failed_modules += 1

        status = icon(all_ok)
        print(f"{status} {mod.module:<45} topics:{ok:>3}/{total}{l1_col}")

        if not all_ok or verbose:
            # L1 language issues
            if is_nan and not mod.l1.passed:
                print("    L1 FAIL — Spanish keywords found:")
                for d in mod.l1.details[:10]:
                    print(d)

            # Per-topic failures
            for tr in mod.topics:
                if tr.all_passed() and not verbose:
                    continue
                checks = {
                    "S1": tr.s1, "R1": tr.r1, "X1": tr.x1,
                    "E1": tr.e1, "M1": tr.m1,
                }
                row_icons = " ".join(f"{k}{icon(v.passed)}" for k, v in checks.items())
                if not tr.all_passed():
                    print(f"    [{row_icons}] {tr.topic}")
                    for key, chk in checks.items():
                        if not chk.passed:
                            for d in chk.details:
                                print(f"      {key}: {d}")

    print()
    checks_label = "L1 S1 R1 X1 E1 M1" if is_nan else "SP1 S1 R1 X1 E1 M1"
    print(f"SUMMARY: {total_modules - failed_modules}/{total_modules} modules passed [{checks_label}]")

    return 0 if failed_modules == 0 else 1


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all lab modules.")
    parser.add_argument("--module", help="Validate a single module by name.")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--verbose", action="store_true", help="Show all topics, not just failures.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    is_nan = repo_root.name == "nan-python-engineering-labs"

    modules = iter_modules(repo_root, args.module)
    if not modules:
        print(f"ERROR: no modules found (module={args.module!r})")
        return 2

    results: list[ModuleResult] = []
    for module_dir in modules:
        print(f"  Scanning {module_dir.name}...", end="\r", flush=True)
        results.append(validate_module(module_dir, repo_root, is_nan))
    print(" " * 60, end="\r")  # clear progress line

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
        return 0

    return print_results(results, is_nan, args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
