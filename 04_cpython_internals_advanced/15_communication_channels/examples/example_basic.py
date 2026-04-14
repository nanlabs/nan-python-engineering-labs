from queue import Queue


def send_message(channel: Queue[str], payload: str) -> None:
    channel.put(payload)


def receive_message(channel: Queue[str]) -> str:
    return channel.get()


def main() -> None:
    channel: Queue[str] = Queue()
    send_message(channel, "ready")
    print(receive_message(channel))


if __name__ == "__main__":
    main()
