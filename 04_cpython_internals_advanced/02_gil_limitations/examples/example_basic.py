import threading
import time


def cpu_task(iterations: int) -> int:
    value = 0
    for _ in range(iterations):
        value += 1
    return value


def benchmark(threads: int, iterations: int) -> float:
    start = time.perf_counter()
    workers = [threading.Thread(target=cpu_task, args=(iterations,)) for _ in range(threads)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return time.perf_counter() - start


def main() -> None:
    one = benchmark(1, 500_000)
    four = benchmark(4, 500_000)
    print(f"1 thread: {one:.4f}s")
    print(f"4 threads: {four:.4f}s")


if __name__ == "__main__":
    main()
