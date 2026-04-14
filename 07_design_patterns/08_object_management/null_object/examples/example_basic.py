class PaymentMethod:
    def pay(self, amount: float) -> str:
        raise NotImplementedError


class NullPayment(PaymentMethod):
    def pay(self, amount: float) -> str:
        return 'no-op'


def checkout(method: PaymentMethod, amount: float) -> str:
    return method.pay(amount)


def main() -> None:
    print(checkout(NullPayment(), 20))


if __name__ == '__main__':
    main()
