class UserRepository:
    def __init__(self) -> None:
        self._items = {1: "Ada"}

    def get(self, user_id: int) -> str:
        return self._items[user_id]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(UserRepository().get(1))


if __name__ == "__main__":
    main()
