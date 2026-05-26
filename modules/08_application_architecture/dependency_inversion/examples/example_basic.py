"""Dependency Inversion: high-level policies depend on abstractions."""

from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, key: str, value: int) -> None:
        ...


class MemoryStorage(Storage):
    def __init__(self) -> None:
        self.data: dict[str, int] = {}

    def save(self, key: str, value: int) -> None:
        self.data[key] = value


class Service:
    def __init__(self, storage: Storage):
        self.storage = storage

    def persist(self, key: str, value: int) -> None:
        self.storage.save(key, value)


if __name__ == "__main__":
    adapter = MemoryStorage()
    Service(adapter).persist("x", 1)
    print(adapter.data)
