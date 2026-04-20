"""pre-commit hooks configuration demo."""


def hook_config(id_: str, repo: str, rev: str) -> dict[str, str]:
    return {"id": id_, "repo": repo, "rev": rev}


def build_precommit_config(hooks: list[dict[str, str]]) -> list[str]:
    lines = ["repos:"]
    for h in hooks:
        lines += [
            f"  - repo: {h['repo']}",
            f"    rev: {h['rev']}",
            "    hooks:",
            f"      - id: {h['id']}",
        ]
    return lines


def main() -> None:
    """Entry point to demonstrate the implementation."""
    hooks = [
        hook_config("ruff", "https://github.com/astral-sh/ruff-pre-commit", "v0.4.0"),
        hook_config("mypy", "https://github.com/pre-commit/mirrors-mypy", "v1.10.0"),
    ]
    config = build_precommit_config(hooks)
    for line in config:
        print(line)


if __name__ == "__main__":
    main()
