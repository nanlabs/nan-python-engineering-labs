def safe_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError('b must be non-zero')
    return a / b


def main() -> None:
    print(safe_divide(10.0, 2.0))


if __name__ == '__main__':
    main()
