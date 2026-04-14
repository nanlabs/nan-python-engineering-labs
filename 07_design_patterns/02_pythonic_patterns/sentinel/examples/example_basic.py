MISSING = object()


def read_setting(data: dict[str, str], key: str):
    value = data.get(key, MISSING)
    if value is MISSING:
        return 'default'
    return value


def main() -> None:
    print(read_setting({}, 'region'))


if __name__ == '__main__':
    main()
