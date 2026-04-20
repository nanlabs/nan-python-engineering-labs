import threading


def synchronized_sum(values: list[int]) -> int:
    total = 0
    lock = threading.Lock()

    def worker(chunk: list[int]) -> None:
        nonlocal total
        subtotal = sum(chunk)
        with lock:
            total += subtotal

    midpoint = len(values) // 2
    threads = [
        threading.Thread(target=worker, args=(values[:midpoint],)),
        threading.Thread(target=worker, args=(values[midpoint:],)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return total


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(synchronized_sum(list(range(1, 101))))


if __name__ == "__main__":
    main()
