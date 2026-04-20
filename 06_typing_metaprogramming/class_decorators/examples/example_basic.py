def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"

    cls.__repr__ = __repr__
    return cls


@add_repr
class Config:
    def __init__(self, env: str) -> None:
        self.env = env


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(Config("dev"))


if __name__ == "__main__":
    main()
