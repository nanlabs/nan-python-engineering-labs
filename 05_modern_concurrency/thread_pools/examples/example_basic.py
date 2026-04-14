from concurrent.futures import ThreadPoolExecutor


def square(value: int) -> int:
    return value * value


def main() -> None:
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(square, [1, 2, 3, 4]))
    print(results)


if __name__ == '__main__':
    main()
