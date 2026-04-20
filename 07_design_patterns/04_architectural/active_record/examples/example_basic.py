class UserRecord:
    _db: dict[int, str] = {}

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    def save(self) -> None:
        self._db[self.user_id] = self.name

    @classmethod
    def find(cls, user_id: int) -> str | None:
        return cls._db.get(user_id)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    user = UserRecord(1, "Ada")
    user.save()
    print(UserRecord.find(1))


if __name__ == "__main__":
    main()
