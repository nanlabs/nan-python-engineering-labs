"""Demonstrate `unittest.mock` without depending on external services."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import Mock


@dataclass(slots=True)
class Notification:
    recipient: str
    subject: str
    body: str


class Notifier:
    def __init__(self, gateway) -> None:
        self.gateway = gateway

    def send(self, notification: Notification) -> bool:
        return self.gateway.deliver(notification)


if __name__ == "__main__":
    gateway = Mock()
    gateway.deliver.return_value = True
    notifier = Notifier(gateway)
    payload = Notification("alice@example.com", "Welcome", "Thanks for joining")
    print("mocking unittest example")
    print(f"delivery result: {notifier.send(payload)}")
    gateway.deliver.assert_called_once_with(payload)
    print("mock assertion succeeded")
