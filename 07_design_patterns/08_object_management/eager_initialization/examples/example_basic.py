class EagerConfig:
    instance = {'env': 'prod', 'region': 'us-east-1'}


def main() -> None:
    print(EagerConfig.instance)


if __name__ == '__main__':
    main()
