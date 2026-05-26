from concurrent.futures import ThreadPoolExecutor


def compute() -> int:
    return sum(range(10))


def main() -> None:
    """Entry point to demonstrate the implementation."""
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(compute)
        print(future.result())


if __name__ == "__main__":
    main()
