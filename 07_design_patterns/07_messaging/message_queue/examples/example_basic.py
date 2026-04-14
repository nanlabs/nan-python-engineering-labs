from queue import Queue


def main() -> None:
    queue: Queue[str] = Queue()
    queue.put('task-1')
    queue.put('task-2')
    print(queue.get(), queue.get())


if __name__ == '__main__':
    main()
