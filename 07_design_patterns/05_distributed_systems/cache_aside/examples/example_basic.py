class Cache:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}


class Store:
    def get(self, key: str) -> str:
        return f"db:{key}"


def load(key: str, cache: Cache, store: Store) -> str:
    if key not in cache.data:
        cache.data[key] = store.get(key)
    return cache.data[key]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    cache = Cache()
    store = Store()
    print(load("u1", cache, store), load("u1", cache, store))


if __name__ == "__main__":
    main()
