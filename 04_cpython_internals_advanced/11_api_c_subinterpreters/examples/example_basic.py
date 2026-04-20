def build_c_api_call(interpreter_id: int) -> str:
    return f"Py_NewInterpreterFromConfig -> id={interpreter_id}"


def describe_lifecycle(interpreter_id: int) -> list[str]:
    return [
        f"Create subinterpreter {interpreter_id}",
        f"Run isolated code in subinterpreter {interpreter_id}",
        f"Finalize subinterpreter {interpreter_id}",
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(build_c_api_call(2))
    for event in describe_lifecycle(2):
        print(event)


if __name__ == "__main__":
    main()
