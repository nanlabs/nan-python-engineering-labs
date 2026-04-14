class WorkerPool:
    def __init__(self) -> None:
        self.free = ['w1', 'w2']

    def acquire(self) -> str:
        return self.free.pop() if self.free else 'none'

    def release(self, worker: str) -> None:
        self.free.append(worker)


def main() -> None:
    pool = WorkerPool()
    worker = pool.acquire()
    pool.release(worker)
    print(pool.free)


if __name__ == '__main__':
    main()
