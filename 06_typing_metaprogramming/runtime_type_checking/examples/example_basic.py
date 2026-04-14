def validate_port(value: object) -> int:
    if not isinstance(value, int):
        raise TypeError('port must be int')
    if value <= 0 or value > 65535:
        raise ValueError('invalid port range')
    return value


def main() -> None:
    print(validate_port(8080))


if __name__ == '__main__':
    main()
