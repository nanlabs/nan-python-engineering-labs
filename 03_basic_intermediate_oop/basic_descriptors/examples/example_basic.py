class PositiveNumber:
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance: object, owner: type | None = None) -> float:
        if instance is None:
            return self  # type: ignore[return-value]
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: float) -> None:
        if value <= 0:
            raise ValueError('Value must be positive')
        setattr(instance, self.private_name, value)


class Invoice:
    amount = PositiveNumber()

    def __init__(self, amount: float) -> None:
        self.amount = amount


def main() -> None:
    invoice = Invoice(250.0)
    print(invoice.amount)


if __name__ == '__main__':
    main()
