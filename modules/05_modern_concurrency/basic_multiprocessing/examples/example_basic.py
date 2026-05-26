from multiprocessing import Process, Queue


def worker(queue: Queue, value: int) -> None:
    queue.put(value * 2)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    queue: Queue = Queue()
    process = Process(target=worker, args=(queue, 21))
    process.start()
    process.join()
    print(queue.get())


if __name__ == "__main__":
    main()
