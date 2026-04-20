import sys


def describe_runtime() -> str:
    enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    return f"GIL enabled: {enabled}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print("Free-threading changes shared-state assumptions.")
    print(describe_runtime())


if __name__ == "__main__":
    main()
