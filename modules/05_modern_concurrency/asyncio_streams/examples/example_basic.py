import asyncio


async def produce_lines() -> list[str]:
    reader = asyncio.StreamReader()
    reader.feed_data(b"one\ntwo\n")
    reader.feed_eof()
    first = await reader.readline()
    second = await reader.readline()
    return [first.decode().strip(), second.decode().strip()]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(asyncio.run(produce_lines()))


if __name__ == "__main__":
    main()
