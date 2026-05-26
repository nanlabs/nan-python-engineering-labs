"""Keep suites easy to navigate by mirroring behavioral areas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    email: str
    active: bool = True


class UserService:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def create_user(self, email: str) -> User:
        user = User(email=email)
        self._users[email] = user
        return user

    def active_emails(self) -> list[str]:
        return sorted(email for email, user in self._users.items() if user.active)


if __name__ == "__main__":
    service = UserService()
    service.create_user("alice@example.com")
    service.create_user("bob@example.com")
    print("test organization example")
    print(service.active_emails())
