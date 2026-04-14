class Account:
    def __init__(self) -> None:
        self._balance = 0.0

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError('negative balance')
        self._balance = value


def main() -> None:
    acc = Account()
    acc.balance = 10.5
    print(acc.balance)


if __name__ == '__main__':
    main()
