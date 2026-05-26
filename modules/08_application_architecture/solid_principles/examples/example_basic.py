"""SOLID mini-demo: SRP + DIP with swappable payment providers."""

from abc import ABC, abstractmethod


class Logger:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        ...


class CreditCard(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"Processing credit card payment: ${amount:.2f}")
        return True


class CheckoutService:
    def __init__(self, processor: PaymentProcessor, logger: Logger):
        self.processor = processor
        self.logger = logger

    def checkout(self, amount: float) -> bool:
        self.logger.log("Checkout started")
        result = self.processor.process(amount)
        self.logger.log(f"Checkout result: {result}")
        return result


if __name__ == "__main__":
    CheckoutService(CreditCard(), Logger()).checkout(42)
