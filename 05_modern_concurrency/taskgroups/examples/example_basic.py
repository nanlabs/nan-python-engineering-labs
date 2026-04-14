import asyncio


async def unit(value: int) -> None:
    await asyncio.sleep(0.01)
    print(value)


async def async_main() -> None:
    async with asyncio.TaskGroup() as group:
        for value in [1, 2, 3]:
            group.create_task(unit(value))


def main() -> None:
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
