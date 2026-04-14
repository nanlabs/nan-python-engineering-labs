class EmailClient:
    def send(self, text: str) -> str:
        return f'sent:{text}'


class NotificationService:
    def __init__(self, client: EmailClient) -> None:
        self.client = client

    def notify(self, text: str) -> str:
        return self.client.send(text)


def main() -> None:
    service = NotificationService(EmailClient())
    print(service.notify('build complete'))


if __name__ == '__main__':
    main()
