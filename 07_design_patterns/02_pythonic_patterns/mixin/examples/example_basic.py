class JsonMixin:
    def to_json(self) -> str:
        return '{' + ', '.join(f'"{k}": "{v}"' for k, v in self.__dict__.items()) + '}'


class Customer(JsonMixin):
    def __init__(self, name: str) -> None:
        self.name = name


def main() -> None:
    print(Customer('Lin').to_json())


if __name__ == '__main__':
    main()
