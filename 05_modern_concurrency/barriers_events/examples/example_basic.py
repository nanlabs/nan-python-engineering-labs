import threading


def main() -> None:
    """Entry point to demonstrate the implementation."""
    barrier = threading.Barrier(3)
    event = threading.Event()
    results: list[str] = []

    def worker(name: str) -> None:
        results.append(f"ready:{name}")
        barrier.wait()
        event.wait()
        results.append(f"go:{name}")

    threads = [threading.Thread(target=worker, args=(f"w{i}",)) for i in range(3)]
    for thread in threads:
        thread.start()
    event.set()
    for thread in threads:
        thread.join()
    print(sorted(results))


if __name__ == "__main__":
    main()
