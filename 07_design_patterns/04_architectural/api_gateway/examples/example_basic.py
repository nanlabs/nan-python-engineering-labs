class UserService:
    def get_user(self, user_id: int) -> dict[str, object]:
        return {'id': user_id, 'name': 'Ada'}


class BillingService:
    def get_balance(self, user_id: int) -> float:
        return 42.0


class ApiGateway:
    def __init__(self) -> None:
        self.users = UserService()
        self.billing = BillingService()

    def profile(self, user_id: int) -> dict[str, object]:
        data = self.users.get_user(user_id)
        data['balance'] = self.billing.get_balance(user_id)
        return data


def main() -> None:
    print(ApiGateway().profile(1))


if __name__ == '__main__':
    main()
