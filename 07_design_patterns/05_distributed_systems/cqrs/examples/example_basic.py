class WriteModel:
    def __init__(self) -> None:
        self.events: list[str] = []

    def add_user(self, name: str) -> None:
        self.events.append(f'user_added:{name}')


class ReadModel:
    def __init__(self) -> None:
        self.users: list[str] = []

    def project(self, event: str) -> None:
        if event.startswith('user_added:'):
            self.users.append(event.split(':', 1)[1])


def main() -> None:
    write = WriteModel()
    read = ReadModel()
    write.add_user('Ada')
    for event in write.events:
        read.project(event)
    print(read.users)


if __name__ == '__main__':
    main()
