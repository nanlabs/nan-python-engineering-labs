from queue import Queue


def main() -> None:
    queue: Queue[int] = Queue()
    for number in [1, 2, 3]:
        queue.put(number)
    values = []
    while not queue.empty():
        values.append(queue.get())
    print(values)


if __name__ == '__main__':
    main()
