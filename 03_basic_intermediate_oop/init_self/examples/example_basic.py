class Product:
    def __init__(self, sku: str, price: float) -> None:
        self.sku = sku
        self.price = price

    def apply_discount(self, percent: float) -> float:
        if percent < 0 or percent > 100:
            raise ValueError('Percent must be between 0 and 100')
        return self.price * (1 - percent / 100)


def main() -> None:
    keyboard = Product('KB-001', 120.0)
    print(keyboard.apply_discount(15))


if __name__ == '__main__':
    main()
