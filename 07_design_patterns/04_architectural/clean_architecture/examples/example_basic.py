from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str


class UserRepo:
    def find(self, user_id: int) -> User:
        return User(user_id, "Ada")


class GetUserUseCase:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def execute(self, user_id: int) -> User:
        return self.repo.find(user_id)


def main() -> None:
    """Entry point to demonstrate the implementation."""
    use_case = GetUserUseCase(UserRepo())
    print(use_case.execute(7))


if __name__ == "__main__":
    main()
