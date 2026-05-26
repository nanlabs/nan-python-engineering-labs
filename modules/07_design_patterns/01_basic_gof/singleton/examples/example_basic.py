class ConfigStore:
    _instance: "ConfigStore | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.env = "dev"
        return cls._instance


def main() -> None:
    """Entry point to demonstrate the implementation."""
    a = ConfigStore()
    b = ConfigStore()
    b.env = "prod"
    print(a is b, a.env)


if __name__ == "__main__":
    main()
