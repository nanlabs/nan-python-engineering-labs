"""Null Object example: replace optional logger checks with a safe default."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def info(self, message: str) -> None:
        ...


class ConsoleLogger(Logger):
    def info(self, message: str) -> None:
        print(f"INFO: {message}")


class NullLogger(Logger):
    def info(self, message: str) -> None:
        _ = message


class PaymentService:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def charge(self, account: str, amount: float) -> str:
        self.logger.info(f"Charging {account} for ${amount:.2f}")
        return f"Charge accepted for {account}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(PaymentService(ConsoleLogger()).charge("ACCT-1", 35.0))
    print(PaymentService(NullLogger()).charge("ACCT-2", 20.0))


if __name__ == "__main__":
    main()
