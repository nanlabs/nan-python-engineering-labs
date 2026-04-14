from queue import Queue


def process_jobs(jobs: list[str]) -> list[str]:
    queue: Queue[str] = Queue()
    for job in jobs:
        queue.put(job)

    processed: list[str] = []
    while not queue.empty():
        processed.append(queue.get().upper())
    return processed


def main() -> None:
    print(process_jobs(["build", "test", "deploy"]))


if __name__ == "__main__":
    main()
