import asyncio


async def fetch_value(delay: float, value: str) -> str:
    await asyncio.sleep(delay)
    return value


async def async_main() -> None:
    result = await fetch_value(0.01, 'ready')
    print(result)


def main() -> None:
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
