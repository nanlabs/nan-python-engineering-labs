import os


def detect_gil_env() -> str:
    value = os.environ.get("PYTHON_GIL", "default")
    return f"PYTHON_GIL={value}"


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print("Free-threading activation relies on build/runtime flags.")
    print(detect_gil_env())


if __name__ == "__main__":
    main()
