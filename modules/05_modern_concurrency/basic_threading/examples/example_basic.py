import threading


def worker(name: str, output: list[str]) -> None:
    output.append(f"done:{name}")


def main() -> None:
    """Entry point to demonstrate the implementation."""
    results: list[str] = []
    threads = [threading.Thread(target=worker, args=(f"t{i}", results)) for i in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(sorted(results))


if __name__ == "__main__":
    main()
