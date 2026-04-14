from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    title: str
    resolved: bool = False


def main() -> None:
    ticket = Ticket(101, 'Fix login bug')
    print(ticket)


if __name__ == '__main__':
    main()
