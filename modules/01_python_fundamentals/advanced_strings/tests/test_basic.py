"""
Basic tests for exercise_01.py to verify file existence, no TODOs,
importability, and main() execution.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

EXERCISE_FILE = Path(__file__).resolve().parents[1] / "exercise" / "exercise_01.py"


def _load_exercise_module():
    """Load exercise_01.py as a module for black-box testing."""
    if not EXERCISE_FILE.exists():
        pytest.fail(f"Missing exercise file: {EXERCISE_FILE}")

    module_id = hashlib.md5(str(EXERCISE_FILE).encode("utf-8")).hexdigest()[:10]
    module_name = f"exercise_01_{module_id}"

    spec = importlib.util.spec_from_file_location(module_name, EXERCISE_FILE)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to create import spec for: {EXERCISE_FILE}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _has_todo_placeholder() -> bool:
    content = EXERCISE_FILE.read_text(encoding="utf-8", errors="ignore")
    return "TODO" in content.upper()


def _public_user_symbols(module) -> list[str]:
    symbols = []
    for name, obj in vars(module).items():
        if name.startswith("_") or name == "main":
            continue
        if (inspect.isfunction(obj) or inspect.isclass(obj)) and getattr(
            obj, "__module__", ""
        ) == module.__name__:
            symbols.append(name)
    return symbols


def test_exercise_file_exists() -> None:
    """Exercise file must exist in the canonical path."""
    assert EXERCISE_FILE.exists(), f"Expected file not found: {EXERCISE_FILE}"


def test_exercise_has_no_todo_placeholders() -> None:
    """Exercise should be completed (no TODO placeholders)."""
    msj = "exercise_01.py still contains TODO placeholders"
    assert not _has_todo_placeholder(), msj


def test_exercise_imports_without_errors() -> None:
    """
    Exercise module should import without syntax/runtime errors on import.
    """
    _load_exercise_module()


def test_exercise_defines_user_api() -> None:
    """
    Exercise should expose at least one user-defined
    function/class besides main.
    """
    module = _load_exercise_module()
    symbols = _public_user_symbols(module)
    assert symbols, (
        "No user-defined functions/classes found in exercise_01.py. "
        "Implement at least one function or class for the topic."
    )


def test_main_runs_if_present() -> None:
    """
    If main() exists with no required args, it should run without exceptions
    """
    module = _load_exercise_module()
    main_func = getattr(module, "main", None)

    if main_func is None:
        pytest.skip("No main() function defined")

    if not callable(main_func):
        pytest.fail("'main' exists but is not callable")

    signature = inspect.signature(main_func)
    required = [
        p
        for p in signature.parameters.values()
        if p.default is inspect._empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    if required:
        pytest.skip("main() requires positional args; skipping execution")

    if inspect.iscoroutinefunction(main_func):
        asyncio.run(main_func())
    else:
        main_func()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
