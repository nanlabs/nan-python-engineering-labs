#!/usr/bin/env python3
"""Transitional CI gate for module validation.

Runs `validate_all_modules.py` and enforces that core modules remain healthy
while legacy modules with known exercise debt are allowed temporarily.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MODULE_STATUS_RE = re.compile(r"^(✅|❌)\s+([0-9]{2}_[a-z0-9_]+)\s+topics:\s+(\d+)/(\d+)")
SUMMARY_RE = re.compile(r"^SUMMARY:\s+(\d+)/(\d+)\s+modules passed")

REQUIRED_PASS_MODULES = {
    "09_testing_qa",
    "14_advanced_python_2026",
    "15_basic_data_science",
}


def run_validation(repo_root: Path) -> tuple[int, str]:
    cmd = [sys.executable, "scripts/validate_all_modules.py"]
    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
    output = f"{proc.stdout}{proc.stderr}"
    return proc.returncode, output


def parse_output(output: str) -> tuple[dict[str, str], tuple[int, int] | None]:
    module_status: dict[str, str] = {}
    summary: tuple[int, int] | None = None

    for raw_line in output.splitlines():
        line = raw_line.strip()
        match = MODULE_STATUS_RE.match(line)
        if match:
            status_symbol, module_name, _, _ = match.groups()
            module_status[module_name] = status_symbol
            continue

        summary_match = SUMMARY_RE.match(line)
        if summary_match:
            passed, total = summary_match.groups()
            summary = (int(passed), int(total))

    return module_status, summary


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    _, output = run_validation(repo_root)
    print(output, end="")

    module_status, summary = parse_output(output)

    if not summary:
        print("\nCI gate error: missing SUMMARY line from validate_all_modules.py output")
        return 1

    missing_required = [
        module for module in sorted(REQUIRED_PASS_MODULES) if module_status.get(module) != "✅"
    ]
    if missing_required:
        print("\nCI gate failure: required modules must pass:")
        for module in missing_required:
            print(f"- {module}")
        return 1

    if summary[1] < 15:
        print(f"\nCI gate failure: expected at least 15 modules in scope, got {summary[1]}")
        return 1

    print("\nCI gate passed: required modules are green; legacy module debt tolerated temporarily.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
