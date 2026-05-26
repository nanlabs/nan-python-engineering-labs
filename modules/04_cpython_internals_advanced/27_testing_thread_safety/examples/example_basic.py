import threading


def thread_safe_increment(iterations: int) -> int:
    value = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal value
        for _ in range(iterations):
            with lock:
                value += 1

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(thread_safe_increment(1000))


if __name__ == "__main__":
    main()
