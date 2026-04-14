"""Exercise: pytest-asyncio.

Goal:
Create `my_solution/async_cache.py`.

Requirements:
- Create `AsyncCache` with an internal dictionary.
- `get_or_set(key, loader)` must await the loader once per missing key and cache the result.
- Return the cached value for repeated requests.

The provided tests use `pytest.mark.asyncio` to verify behavior.
"""
