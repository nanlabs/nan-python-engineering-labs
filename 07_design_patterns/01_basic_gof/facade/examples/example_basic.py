class AuthService:
    def login(self, user: str) -> str:
        return f"auth:{user}"


class DataService:
    def fetch_dashboard(self, user: str) -> str:
        return f"dashboard:{user}"


class DashboardFacade:
    def __init__(self) -> None:
        self.auth = AuthService()
        self.data = DataService()

    def load(self, user: str) -> str:
        _ = self.auth.login(user)
        return self.data.fetch_dashboard(user)


def main() -> None:
    print(DashboardFacade().load('ada'))


if __name__ == '__main__':
    main()
