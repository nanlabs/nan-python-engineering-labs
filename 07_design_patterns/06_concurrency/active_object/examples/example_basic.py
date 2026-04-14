from queue import Queue
import threading


class ActiveObject:
    def __init__(self) -> None:
        self.queue: Queue[callable] = Queue()
        self.worker = threading.Thread(target=self._loop, daemon=True)
        self.worker.start()

    def _loop(self) -> None:
        while True:
            job = self.queue.get()
            job()
            self.queue.task_done()

    def submit(self, fn: callable) -> None:
        self.queue.put(fn)


def main() -> None:
    out: list[str] = []
    ao = ActiveObject()
    ao.submit(lambda: out.append('done'))
    ao.queue.join()
    print(out)


if __name__ == '__main__':
    main()
