import threading


storage = threading.local()


def set_value(value: str) -> str:
    storage.tag = value
    return storage.tag


def main() -> None:
    print(set_value("main-thread"))


if __name__ == "__main__":
    main()
