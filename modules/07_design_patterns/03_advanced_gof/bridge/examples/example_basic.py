"""Bridge pattern example: separate notification abstraction from channels."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Channel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        ...


class EmailChannel(Channel):
    def send(self, recipient: str, message: str) -> str:
        return f"Email to {recipient}: {message}"


class SmsChannel(Channel):
    def send(self, recipient: str, message: str) -> str:
        return f"SMS to {recipient}: {message}"


class Notification:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel

    def notify(self, recipient: str, message: str) -> str:
        return self.channel.send(recipient, message)


class AlertNotification(Notification):
    def notify(self, recipient: str, message: str) -> str:
        return self.channel.send(recipient, f"[ALERT] {message}")


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Notification(EmailChannel()).notify("team@example.com", "Daily summary ready"))
    print(AlertNotification(SmsChannel()).notify("+1-555-0100", "CPU is above threshold"))


if __name__ == "__main__":
    main()
