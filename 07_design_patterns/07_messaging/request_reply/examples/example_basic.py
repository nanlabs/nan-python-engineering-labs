def service(request: str) -> str:
    return f'reply:{request}'


def client(request: str) -> str:
    return service(request)


def main() -> None:
    print(client('ping'))


if __name__ == '__main__':
    main()
