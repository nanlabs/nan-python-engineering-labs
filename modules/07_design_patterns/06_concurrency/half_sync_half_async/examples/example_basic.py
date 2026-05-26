import queue
import threading


def main() -> None:
    """Entry point to demonstrate the implementation."""
    q: queue.Queue[int] = queue.Queue()
    out: list[int] = []

    def producer() -> None:
        for i in [1, 2, 3]:
            q.put(i)
        q.put(-1)

    def consumer() -> None:
        while True:
            item = q.get()
            if item == -1:
                break
            out.append(item * 2)

    tp = threading.Thread(target=producer)
    tc = threading.Thread(target=consumer)
    tp.start()
    tc.start()
    tp.join()
    tc.join()
    print(out)


if __name__ == "__main__":
    main()
