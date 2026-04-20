from dataclasses import dataclass, field


@dataclass
class Actor:
    name: str
    mailbox: list[str] = field(default_factory=list)

    def send(self, message: str) -> None:
        self.mailbox.append(message)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    actor = Actor("worker")
    actor.send("start")
    actor.send("stop")
    print(actor.mailbox)


if __name__ == "__main__":
    main()
