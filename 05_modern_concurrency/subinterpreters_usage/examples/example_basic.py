def describe_subinterpreters() -> list[str]:
    return [
        'Isolated runtime state',
        'Separate module imports',
        'Useful for runtime isolation',
    ]


def main() -> None:
    for line in describe_subinterpreters():
        print(line)


if __name__ == '__main__':
    main()
