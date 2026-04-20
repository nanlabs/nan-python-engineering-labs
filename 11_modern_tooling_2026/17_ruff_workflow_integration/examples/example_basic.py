"""Ruff CI/CD integration: simulate a pre-commit hook pipeline."""


def precommit_hook(name: str, command: str) -> dict[str, str]:
    return {"hook": name, "run": command, "stages": "pre-commit, ci"}


def run_pipeline(hooks: list[dict[str, str]]) -> list[str]:
    results = []
    for hook in hooks:
        results.append(f"[{hook['hook']}] Running: {hook['run']} → PASS")
    return results


def main() -> None:
    """Entry point to demonstrate the implementation."""
    pipeline = [
        precommit_hook("ruff-lint", "ruff check ."),
        precommit_hook("ruff-format", "ruff format --check ."),
        precommit_hook("mypy", "mypy src/"),
    ]
    for result in run_pipeline(pipeline):
        print(result)


if __name__ == "__main__":
    main()
