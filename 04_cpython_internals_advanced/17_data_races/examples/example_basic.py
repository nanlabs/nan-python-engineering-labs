import threading


def run_without_lock() -> int:
    value = 0

    def writer() -> None:
        nonlocal value
        for _ in range(5_000):
            value += 1

    threads = [threading.Thread(target=writer) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(f"Final value (race-prone): {run_without_lock()}")


if __name__ == "__main__":
    main()
