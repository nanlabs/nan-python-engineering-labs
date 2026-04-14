import threading
from queue import SimpleQueue


def worker(queue: SimpleQueue[int], number: int) -> None:
    queue.put(number * number)


def main() -> None:
    queue: SimpleQueue[int] = SimpleQueue()
    threads = [threading.Thread(target=worker, args=(queue, i)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    values = [queue.get() for _ in range(5)]
    print(sorted(values))


if __name__ == "__main__":
    main()
