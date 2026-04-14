class PaymentProcessor:
    def process(self, amount: float) -> str:
        raise NotImplementedError


class CardProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"card:{amount:.2f}"


class PaypalProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"paypal:{amount:.2f}"


class Checkout:
    def create_processor(self, kind: str) -> PaymentProcessor:
        if kind == 'card':
            return CardProcessor()
        return PaypalProcessor()


def main() -> None:
    checkout = Checkout()
    print(checkout.create_processor('card').process(19.9))


if __name__ == '__main__':
    main()
