import threading


def main() -> None:
    """Entry point to demonstrate the implementation."""
    counter = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal counter
        for _ in range(100):
            with lock:
                counter += 1

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(counter)


if __name__ == "__main__":
    main()
