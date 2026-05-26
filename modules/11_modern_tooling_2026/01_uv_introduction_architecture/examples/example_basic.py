"""uv architecture: resolver, cache, and workspace layers."""


def describe_architecture() -> dict[str, str]:
    return {
        "resolver": "PubGrub-based dependency resolver",
        "cache": "global content-addressed package cache",
        "venv": "lightweight virtual environments",
        "workspace": "multi-package monorepo support",
    }


def uv_commands() -> list[tuple[str, str]]:
    return [
        ("uv add <package>", "install and lock a dependency"),
        ("uv sync", "restore env from uv.lock"),
        ("uv run <script>", "run a script in the managed env"),
    ]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for layer, desc in describe_architecture().items():
        print(f"[{layer}] {desc}")
    for cmd, desc in uv_commands():
        print(f"  $ {cmd}  # {desc}")


if __name__ == "__main__":
    main()
