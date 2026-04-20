from queue import Queue


def send_messages(channel: Queue[str], payloads: list[str]) -> None:
    for payload in payloads:
        channel.put(payload)


def receive_all(channel: Queue[str], total: int) -> list[str]:
    return [channel.get() for _ in range(total)]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    channel: Queue[str] = Queue()
    messages = ["task-1", "task-2", "done"]
    send_messages(channel, messages)
    print(receive_all(channel, len(messages)))


if __name__ == "__main__":
    main()
