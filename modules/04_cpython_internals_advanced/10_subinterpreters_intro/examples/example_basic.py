from dataclasses import dataclass


@dataclass
class Subinterpreter:
    identifier: int
    isolated_state: str


def create_subinterpreters(count: int) -> list[Subinterpreter]:
    return [Subinterpreter(i, f"state-{i}") for i in range(count)]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for sub in create_subinterpreters(3):
        print(sub)


if __name__ == "__main__":
    main()
