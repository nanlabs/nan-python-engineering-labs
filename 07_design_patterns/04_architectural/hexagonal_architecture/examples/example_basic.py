class UserPort:
    def get_name(self, user_id: int) -> str:
        raise NotImplementedError


class InMemoryUserAdapter(UserPort):
    def get_name(self, user_id: int) -> str:
        return {1: 'Ada'}.get(user_id, 'Unknown')


class UserService:
    def __init__(self, port: UserPort) -> None:
        self.port = port

    def greet(self, user_id: int) -> str:
        return f"Hello {self.port.get_name(user_id)}"


def main() -> None:
    print(UserService(InMemoryUserAdapter()).greet(1))


if __name__ == '__main__':
    main()
