def build_c_api_call(interpreter_id: int) -> str:
    return f"Py_NewInterpreterFromConfig -> id={interpreter_id}"


def main() -> None:
    print(build_c_api_call(2))


if __name__ == "__main__":
    main()
