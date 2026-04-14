from dataclasses import dataclass


@dataclass
class HttpClientChoice:
    name: str
    style: str


def compare_clients() -> list[HttpClientChoice]:
    return [
        HttpClientChoice('aiohttp', 'async server and client ecosystem'),
        HttpClientChoice('httpx', 'modern sync/async client API'),
    ]


def main() -> None:
    for client in compare_clients():
        print(f"{client.name}: {client.style}")


if __name__ == '__main__':
    main()
