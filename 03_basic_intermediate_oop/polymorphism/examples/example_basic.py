class Notification:
    def send(self, message: str) -> str:
        raise NotImplementedError


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email sent: {message}"


class SmsNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS sent: {message}"


def dispatch(notification: Notification, message: str) -> str:
    return notification.send(message)


def main() -> None:
    channels: list[Notification] = [EmailNotification(), SmsNotification()]
    for channel in channels:
        print(dispatch(channel, 'Build completed'))


if __name__ == '__main__':
    main()
