from concurrent.futures import ThreadPoolExecutor


def work(x: int) -> int:
    return x + 1


def main() -> None:
    with ThreadPoolExecutor(max_workers=2) as pool:
        print(list(pool.map(work, [1, 2, 3])))


if __name__ == '__main__':
    main()
