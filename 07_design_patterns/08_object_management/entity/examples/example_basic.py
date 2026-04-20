class UserEntity:
    def __init__(self, user_id: int, email: str) -> None:
        self.user_id = user_id
        self.email = email

    def change_email(self, value: str) -> None:
        self.email = value


def main() -> None:
    """Entry point to demonstrate the implementation."""
    user = UserEntity(1, "a@example.com")
    user.change_email("b@example.com")
    print(user.user_id, user.email)


if __name__ == "__main__":
    main()
