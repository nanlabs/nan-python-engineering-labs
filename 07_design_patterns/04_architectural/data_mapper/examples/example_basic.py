class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name


class UserMapper:
    @staticmethod
    def to_row(user: User) -> dict[str, object]:
        return {"id": user.user_id, "name": user.name}

    @staticmethod
    def from_row(row: dict[str, object]) -> User:
        return User(int(row["id"]), str(row["name"]))


def main() -> None:
    """Entry point to demonstrate the implementation."""
    row = UserMapper.to_row(User(2, "Lin"))
    print(UserMapper.from_row(row).name)


if __name__ == "__main__":
    main()
