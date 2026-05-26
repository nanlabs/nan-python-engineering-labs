import threading


def with_timeout(fn, timeout_s: float):
    result: dict[str, object] = {"value": None}

    def run() -> None:
        result["value"] = fn()

    t = threading.Thread(target=run)
    t.start()
    t.join(timeout=timeout_s)
    return "timeout" if t.is_alive() else result["value"]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(with_timeout(lambda: "ok", 0.1))


if __name__ == "__main__":
    main()
