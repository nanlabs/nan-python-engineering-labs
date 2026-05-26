"""Define contracts with abstract base classes."""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> str:
        raise RuntimeError("override required")


class CardProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"Card charged: ${amount:.2f}"


class WalletProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"Wallet debited: ${amount:.2f}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for processor in [CardProcessor(), WalletProcessor()]:
        print(processor.process(19.99))


if __name__ == "__main__":
    main()
