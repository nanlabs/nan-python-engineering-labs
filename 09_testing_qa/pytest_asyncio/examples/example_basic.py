"""Minimal async cache example used by coroutine tests."""

from __future__ import annotations

import asyncio


class AsyncCache:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    async def get_or_set(self, key: str, loader) -> object:
        if key not in self._values:
            self._values[key] = await loader()
        return self._values[key]


async def build_value() -> str:
    await asyncio.sleep(0.01)
    return "computed"


async def main() -> None:
    cache = AsyncCache()
    print("pytest-asyncio example")
    first = await cache.get_or_set("answer", build_value)
    second = await cache.get_or_set("answer", build_value)
    print(first, second)


if __name__ == "__main__":
    asyncio.run(main())
