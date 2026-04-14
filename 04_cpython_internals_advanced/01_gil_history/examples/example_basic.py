import sys


def summarize_gil_state() -> str:
    enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    return f"GIL enabled: {enabled}"


def main() -> None:
    print(f"Python: {sys.version.split()[0]}")
    print(summarize_gil_state())


if __name__ == "__main__":
    main()
