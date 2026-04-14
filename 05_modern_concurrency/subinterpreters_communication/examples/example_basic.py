from queue import Queue


def main() -> None:
    channel: Queue[str] = Queue()
    channel.put('payload')
    print(channel.get())


if __name__ == '__main__':
    main()
