"""SOLID Principles foundation."""
from abc import ABC, abstractmethod

class Logger:
    def log(self, msg: str):
        print(f"[LOG] {msg}")

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: pass

class CreditCard(PaymentProcessor):
    def process(self, amount: float) -> bool:
        print(f"Processing ${amount}")
        return True

if __name__ == "__main__":
    print("✓ SOLID Principles demonstrated")
