import asyncio


def main() -> None:
    """Entry point to demonstrate the implementation."""
    loop = asyncio.new_event_loop()
    try:
        loop.set_debug(True)
        print(loop.get_debug())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
