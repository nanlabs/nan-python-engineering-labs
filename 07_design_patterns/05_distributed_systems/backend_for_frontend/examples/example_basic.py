class UserApi:
    def profile(self) -> dict[str, str]:
        return {"name": "Ada"}


class BFF:
    def __init__(self, api: UserApi) -> None:
        self.api = api

    def mobile_payload(self) -> dict[str, str]:
        user = self.api.profile()
        return {"display_name": user["name"]}


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(BFF(UserApi()).mobile_payload())


if __name__ == "__main__":
    main()
