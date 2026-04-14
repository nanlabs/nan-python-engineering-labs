"""Hexagonal Architecture - domain isolated."""
from abc import ABC, abstractmethod

class UserRepo(ABC):
    @abstractmethod
    def save(self, id, name): pass

class Memory(UserRepo):
    def __init__(self): self.users = {}
    def save(self, id, name):
        self.users[id] = {"id": id, "name": name}

class UserService:
    def __init__(self, repo):
        self.repo = repo
    def register(self, id, name):
        self.repo.save(id, name)

if __name__ == "__main__":
    s = UserService(Memory())
    s.register(1, "Alice")
    print("✓ Hexagonal")
