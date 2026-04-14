"""Ports & Adapters - swap implementations."""
from abc import ABC, abstractmethod

class PaymentPort(ABC):
    @abstractmethod
    def charge(self, amt): pass

class Stripe(PaymentPort):
    def charge(self, amt):
        print(f"Stripe: ${amt}")
        return True

class PPal(PaymentPort):
    def charge(self, amt):
        print(f"PayPal: ${amt}")
        return True

class Checkout:
    def __init__(self, payment):
        self.payment = payment
    def process(self, amt):
        return self.payment.charge(amt)

if __name__ == "__main__":
    Checkout(Stripe()).process(50)
    Checkout(PPal()).process(30)
    print("✓ Ports&Adapters")
