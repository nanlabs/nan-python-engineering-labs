import asyncio


async def worker(name: str) -> str:
    await asyncio.sleep(0.01)
    return f"done:{name}"


async def async_main() -> None:
    results = await asyncio.gather(worker("a"), worker("b"))
    print(results)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
