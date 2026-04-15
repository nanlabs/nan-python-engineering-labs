"""Hexagonal architecture: domain logic does not depend on adapters."""
from abc import ABC, abstractmethod


class UserRepo(ABC):
    @abstractmethod
    def save(self, user_id: int, name: str) -> None:
        ...


class MemoryRepo(UserRepo):
    def __init__(self) -> None:
        self.users: dict[int, dict[str, object]] = {}

    def save(self, user_id: int, name: str) -> None:
        self.users[user_id] = {"id": user_id, "name": name}


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def register(self, user_id: int, name: str) -> None:
        self.repo.save(user_id, name)


if __name__ == "__main__":
    repo = MemoryRepo()
    UserService(repo).register(1, "Alice")
    print(repo.users[1])
