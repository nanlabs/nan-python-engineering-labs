from concurrent.futures import ThreadPoolExecutor


def disk_write(payload: str) -> str:
    return f'written:{payload}'


def main() -> None:
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(disk_write, 'event')
        print(future.result())


if __name__ == '__main__':
    main()
