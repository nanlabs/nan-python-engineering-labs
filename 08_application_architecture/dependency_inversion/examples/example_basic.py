"""Dependency Inversion - depend on abstractions."""
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, key, val): pass

class DB(Storage):
    def save(self, k, v): print(f"DB.save({k}={v})")

class Service:
    def __init__(self, storage: Storage):
        self.storage = storage
    def persist(self, k, v):
        self.storage.save(k, v)

if __name__ == "__main__":
    Service(DB()).persist("x", 1)
    print("✓ Dependency Inversion")
