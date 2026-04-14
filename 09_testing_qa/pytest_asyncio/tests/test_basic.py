"""Tests for the pytest-asyncio exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "async_cache.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/async_cache.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("async_cache", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
async def test_get_or_set_caches_values() -> None:
    module = load_solution_module()
    cache = module.AsyncCache()
    calls = 0

    async def loader() -> str:
        nonlocal calls
        calls += 1
        return "value"

    first = await cache.get_or_set("answer", loader)
    second = await cache.get_or_set("answer", loader)
    assert first == second == "value"
    assert calls == 1
