import asyncio


async def compute(value: int) -> int:
    await asyncio.sleep(0.01)
    return value * value


async def async_main() -> None:
    print(await compute(5))


def main() -> None:
    """Entry point to demonstrate the implementation."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
