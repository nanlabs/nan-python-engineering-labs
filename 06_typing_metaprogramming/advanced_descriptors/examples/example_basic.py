class Positive:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = f'_{name}'

    def __get__(self, instance, owner=None):
        return getattr(instance, self.name)

    def __set__(self, instance, value: int) -> None:
        if value <= 0:
            raise ValueError('value must be positive')
        setattr(instance, self.name, value)


class Product:
    stock = Positive()

    def __init__(self, stock: int) -> None:
        self.stock = stock


def main() -> None:
    print(Product(10).stock)


if __name__ == '__main__':
    main()
