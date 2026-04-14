class OrderAggregate:
    def __init__(self) -> None:
        self.items: list[float] = []

    def add_item(self, price: float) -> None:
        self.items.append(price)

    def total(self) -> float:
        return sum(self.items)


def main() -> None:
    order = OrderAggregate()
    order.add_item(10)
    order.add_item(5)
    print(order.total())


if __name__ == '__main__':
    main()
