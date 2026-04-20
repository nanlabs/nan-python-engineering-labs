"""Domain-Driven Design - business model explicit."""


class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency


class Order:
    def __init__(self, id, total):
        self.id, self.total = id, total


class Repository:
    def __init__(self):
        self.orders = {}

    def save(self, order):
        self.orders[order.id] = order


if __name__ == "__main__":
    order = Order("1", Money(100))
    repo = Repository()
    repo.save(order)
    print("✓ DDD")
