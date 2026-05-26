def isolated_namespaces() -> tuple[dict[str, int], dict[str, int]]:
    a = {"counter": 1}
    b = {"counter": 99}
    return a, b


def main() -> None:
    """Entry point to demonstrate the implementation."""
    first, second = isolated_namespaces()
    first["counter"] += 1
    print(first, second)


if __name__ == "__main__":
    main()
