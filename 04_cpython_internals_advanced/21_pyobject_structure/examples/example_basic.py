import sys


def inspect_object(obj: object) -> dict[str, int]:
    return {
        "id": id(obj),
        "size": sys.getsizeof(obj),
        "refcount": sys.getrefcount(obj),
    }


def main() -> None:
    info = inspect_object({"key": "value"})
    print(info)


if __name__ == "__main__":
    main()
