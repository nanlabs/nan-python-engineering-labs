HANDLERS: dict[str, callable] = {}


def register(name: str):
    def deco(fn: callable):
        HANDLERS[name] = fn
        return fn

    return deco


@register("ping")
def ping() -> str:
    return "pong"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(HANDLERS["ping"]())


if __name__ == "__main__":
    main()
