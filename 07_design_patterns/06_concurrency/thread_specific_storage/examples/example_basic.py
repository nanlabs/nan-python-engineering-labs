import threading


local_data = threading.local()


def assign(value: str) -> str:
    local_data.token = value
    return local_data.token


def main() -> None:
    print(assign('main-token'))


if __name__ == '__main__':
    main()
