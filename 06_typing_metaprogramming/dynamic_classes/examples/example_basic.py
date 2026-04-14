def build_model(name: str, fields: dict[str, object]) -> type:
    return type(name, (), fields)


def main() -> None:
    User = build_model('User', {'role': 'admin'})
    user = User()
    print(user.role)


if __name__ == '__main__':
    main()
