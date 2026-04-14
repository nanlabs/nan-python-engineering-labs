def run_in_subinterpreter(script: str) -> str:
    return f"Executing in isolated runtime: {script[:30]}..."


def main() -> None:
    print(run_in_subinterpreter("print('hello from subinterpreter')"))


if __name__ == "__main__":
    main()
