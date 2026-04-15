"""uv tool: install and run global CLI tools without polluting env."""


def tool_commands() -> list[tuple[str, str]]:
    return [
        ("uv tool install ruff",      "global install of ruff"),
        ("uv tool install mypy",      "global install of mypy"),
        ("uv tool run ruff check .",  "run ruff without installing"),
        ("uv tool list",              "show installed global tools"),
        ("uv tool uninstall ruff",    "remove a global tool"),
    ]


def isolation_benefit() -> str:
    return "Each tool gets its own isolated env → no dependency conflicts."


def main() -> None:
    for cmd, desc in tool_commands():
        print(f"  $ {cmd}  # {desc}")
    print()
    print(isolation_benefit())


if __name__ == "__main__":
    main()
