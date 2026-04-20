#!/usr/bin/env python3
"""Run topic exercise tests sequentially.

This repository stores many files named tests/test_basic.py. Running pytest
against multiple topics in one collection pass can trigger module name
collisions, so this helper executes one test file at a time.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def discover_test_files() -> list[Path]:
    return sorted(REPO_ROOT.glob("**/tests/test_basic.py"))


def resolve_target(target: str) -> list[Path]:
    path = (REPO_ROOT / target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target not found: {target}")

    if path.is_file():
        if path.name != "test_basic.py":
            raise ValueError("Only tests/test_basic.py files are supported")
        return [path]

    tests_dir = path / "tests"
    direct_test = tests_dir / "test_basic.py"
    if direct_test.exists():
        return [direct_test]

    return sorted(path.glob("**/tests/test_basic.py"))


def run_test_file(test_file: Path, verbose: bool) -> int:
    cmd = [sys.executable, "-m", "pytest"]
    if not verbose:
        cmd.append("-q")

    cmd.extend(["-o", "addopts=", str(test_file)])

    return subprocess.run(cmd, cwd=REPO_ROOT).returncode  # noqa: S603


def main() -> int:
    parser = argparse.ArgumentParser(
        description=("Run topic tests one file at a time to avoid pytest collisions."),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=("Optional topic/module paths or specific tests/test_basic.py files."),
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop after the first failing test file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Use normal pytest output instead of -q.",
    )
    args = parser.parse_args()

    try:
        files = []
        if args.targets:
            for target in args.targets:
                files.extend(resolve_target(target))
        else:
            files = discover_test_files()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    unique_files = sorted({path.resolve() for path in files})
    if not unique_files:
        print("ERROR: no tests/test_basic.py files found for the given target(s)")
        return 2

    failures = 0
    for test_file in unique_files:
        rel = test_file.relative_to(REPO_ROOT)
        print(f"== {rel} ==")
        exit_code = run_test_file(test_file, verbose=args.verbose)
        if exit_code == 0:
            print("PASS\n")
            continue

        failures += 1
        print(f"FAIL (exit {exit_code})\n")
        if args.fail_fast:
            break

    passed = len(unique_files) - failures
    print(f"Summary: {passed}/{len(unique_files)} test files passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
