from concurrent.futures import ProcessPoolExecutor


def double(value: int) -> int:
    return value * 2


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(double, [1, 2, 3]))
    print(results)


if __name__ == '__main__':
    main()
