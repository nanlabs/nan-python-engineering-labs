"""
Example of a simple BankAccount class with attributes and methods.
"""


class BankAccount:
    """A simple bank account class."""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        """
        Initialize the bank account with an owner and an optional balance.
        """
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Deposit a positive amount to the account."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Withdraw a positive amount from the account if sufficient funds exist.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount


def main() -> None:
    """Entry point to demonstrate the implementation."""
    account = BankAccount("Lin", 100)
    account.deposit(50)
    account.withdraw(30)
    print(account.balance)


if __name__ == "__main__":
    main()
