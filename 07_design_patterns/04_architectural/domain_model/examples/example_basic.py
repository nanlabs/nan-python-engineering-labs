from dataclasses import dataclass


@dataclass
class CartItem:
    price: float
    quantity: int


class Cart:
    def __init__(self) -> None:
        self.items: list[CartItem] = []

    def add(self, item: CartItem) -> None:
        self.items.append(item)

    def total(self) -> float:
        return sum(i.price * i.quantity for i in self.items)


def main() -> None:
    cart = Cart()
    cart.add(CartItem(10.0, 2))
    print(cart.total())


if __name__ == '__main__':
    main()
