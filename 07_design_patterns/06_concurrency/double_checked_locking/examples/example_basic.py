import threading


class LazyCache:
    _instance: 'LazyCache | None' = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls) -> 'LazyCache':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = LazyCache()
        return cls._instance


def main() -> None:
    print(LazyCache.instance() is LazyCache.instance())


if __name__ == '__main__':
    main()
