class Order:
    def __init__(self) -> None:
        self._total = 0.0

    @property
    def total(self) -> float:
        return self._total

    @total.setter
    def total(self, value: float) -> None:
        if value < 0:
            raise ValueError('Total cannot be negative')
        self._total = value


def main() -> None:
    order = Order()
    order.total = 199.99
    print(order.total)


if __name__ == '__main__':
    main()
