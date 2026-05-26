class EagerConfig:
    instance = {"env": "prod", "region": "us-east-1", "retries": 3}


def update_region(region: str) -> None:
    EagerConfig.instance["region"] = region


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(EagerConfig.instance)
    update_region("eu-west-1")
    print(EagerConfig.instance)


if __name__ == "__main__":
    main()
