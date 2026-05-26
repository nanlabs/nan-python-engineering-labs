from typing import Protocol


class SupportsClose(Protocol):
    def close(self) -> str:
        ...


class Connection:
    def close(self) -> str:
        return "closed"


def shutdown(resource: SupportsClose) -> str:
    return resource.close()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(shutdown(Connection()))


if __name__ == "__main__":
    main()
