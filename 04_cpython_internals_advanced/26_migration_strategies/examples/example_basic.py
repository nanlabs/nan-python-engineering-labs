from dataclasses import dataclass


@dataclass
class MigrationStep:
    name: str
    done: bool


def build_plan() -> list[MigrationStep]:
    return [
        MigrationStep("Audit shared mutable state", True),
        MigrationStep("Add synchronization primitives", True),
        MigrationStep("Run stress tests", False),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for step in build_plan():
        print(f"[{'x' if step.done else ' '}] {step.name}")


if __name__ == "__main__":
    main()
