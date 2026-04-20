import asyncio


def main() -> None:
    """Entry point to demonstrate the implementation."""
    loop = asyncio.new_event_loop()
    try:
        print(type(loop).__name__)
        print(loop.is_running())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
