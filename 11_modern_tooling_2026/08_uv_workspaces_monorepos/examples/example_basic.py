"""uv workspaces: managing multiple packages in one repository."""


def workspace_layout() -> list[str]:
    return [
        "monorepo/",
        "  pyproject.toml        # root workspace config",
        "  packages/",
        "    api/pyproject.toml  # sub-package",
        "    lib/pyproject.toml  # sub-package",
        "  uv.lock               # shared lock file",
    ]


def workspace_commands() -> list[tuple[str, str]]:
    return [
        ("uv sync", "install all workspace packages"),
        ("uv run -p api tests", "run tests in a specific member"),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print("Workspace layout:")
    for line in workspace_layout():
        print(f"  {line}")
    print("Commands:")
    for cmd, desc in workspace_commands():
        print(f"  $ {cmd}  # {desc}")


if __name__ == "__main__":
    main()
