class ChatMediator:
    def __init__(self) -> None:
        self.logs: list[str] = []

    def send(self, sender: str, msg: str) -> None:
        self.logs.append(f"{sender}:{msg}")


class User:
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self.mediator = mediator

    def say(self, msg: str) -> None:
        self.mediator.send(self.name, msg)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    med = ChatMediator()
    User("a", med).say("hello")
    print(med.logs)


if __name__ == "__main__":
    main()
