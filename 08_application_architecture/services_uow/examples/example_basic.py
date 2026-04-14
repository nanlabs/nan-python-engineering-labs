"""Unit of Work - atomic operations."""
class Transaction:
    def __init__(self, f, t, amt):
        self.from_id, self.to_id, self.amount = f, t, amt

class UoW:
    def __init__(self):
        self.txns = []
        self.committed = False
    def add_txn(self, txn):
        self.txns.append(txn)
    def commit(self):
        self.committed = True

class TransferService:
    def __init__(self, uow):
        self.uow = uow
    def transfer(self, f, t, a):
        self.uow.add_txn(Transaction(f, t, a))
        self.uow.commit()

if __name__ == "__main__":
    u = UoW()
    s = TransferService(u)
    s.transfer(1, 2, 100)
    print(f"✓ UoW: committed={u.committed}")
