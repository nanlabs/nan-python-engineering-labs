from functools import wraps


def trace(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} -> {result}")
        return result

    return wrapper


@trace
def area(w: int, h: int) -> int:
    return w * h


def main() -> None:
    area(4, 5)


if __name__ == '__main__':
    main()
