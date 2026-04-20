def retry(fn, attempts: int):
    last_err: Exception | None = None
    for _ in range(attempts):
        try:
            return fn()
        except Exception as err:
            last_err = err
    raise last_err if last_err else RuntimeError("unknown")


def main() -> None:
    """Entry point to demonstrate the implementation."""
    state = {"n": 0}

    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 2:
            raise RuntimeError("temporary")
        return "ok"

    print(retry(flaky, 3))


if __name__ == "__main__":
    main()
