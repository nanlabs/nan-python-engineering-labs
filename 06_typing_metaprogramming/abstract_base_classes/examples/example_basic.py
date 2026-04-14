from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def dump(self, value: dict[str, object]) -> str:
        raise NotImplementedError


class JsonLikeSerializer(Serializer):
    def dump(self, value: dict[str, object]) -> str:
        pairs = ', '.join(f'{k}={v}' for k, v in value.items())
        return '{' + pairs + '}'


def main() -> None:
    serializer = JsonLikeSerializer()
    print(serializer.dump({'ok': True}))


if __name__ == '__main__':
    main()
