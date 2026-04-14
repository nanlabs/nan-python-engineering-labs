class Account:
    def __init__(self) -> None:
        self.events: list[tuple[str, int]] = []

    def deposit(self, amount: int) -> None:
        self.events.append(('deposit', amount))

    def balance(self) -> int:
        total = 0
        for kind, amount in self.events:
            if kind == 'deposit':
                total += amount
        return total


def main() -> None:
    acc = Account()
    acc.deposit(10)
    acc.deposit(15)
    print(acc.balance())


if __name__ == '__main__':
    main()
