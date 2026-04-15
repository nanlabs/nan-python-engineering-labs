"""Ports and adapters: swap infrastructure implementations via a port."""
from abc import ABC, abstractmethod


class PaymentPort(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        ...


class StripeAdapter(PaymentPort):
    def charge(self, amount: float) -> bool:
        print(f"Stripe charged: ${amount:.2f}")
        return True


class PayPalAdapter(PaymentPort):
    def charge(self, amount: float) -> bool:
        print(f"PayPal charged: ${amount:.2f}")
        return True


class Checkout:
    def __init__(self, payment: PaymentPort):
        self.payment = payment

    def process(self, amount: float) -> bool:
        return self.payment.charge(amount)


if __name__ == "__main__":
    Checkout(StripeAdapter()).process(50)
    Checkout(PayPalAdapter()).process(30)
