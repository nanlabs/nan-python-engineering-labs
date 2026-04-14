from dataclasses import dataclass


@dataclass
class HttpRequest:
    method: str
    path: str
    headers: dict[str, str]


class RequestBuilder:
    def __init__(self) -> None:
        self._method = 'GET'
        self._path = '/'
        self._headers: dict[str, str] = {}

    def method(self, value: str) -> 'RequestBuilder':
        self._method = value
        return self

    def path(self, value: str) -> 'RequestBuilder':
        self._path = value
        return self

    def header(self, key: str, value: str) -> 'RequestBuilder':
        self._headers[key] = value
        return self

    def build(self) -> HttpRequest:
        return HttpRequest(self._method, self._path, dict(self._headers))


def main() -> None:
    req = RequestBuilder().method('POST').path('/users').header('x-id', '42').build()
    print(req)


if __name__ == '__main__':
    main()
