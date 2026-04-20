"""uv installation and configuration overview."""


def installation_methods() -> list[dict[str, str]]:
    return [
        {"method": "curl", "command": "curl -LsSf https://astral.sh/uv/install.sh | sh"},
        {"method": "pip", "command": "pip install uv"},
        {"method": "brew", "command": "brew install uv"},
    ]


def key_config_fields() -> dict[str, str]:
    return {
        "UV_CACHE_DIR": "custom cache directory",
        "UV_PYTHON": "pin Python version",
        "UV_NO_BUILD_ISOLATION": "skip build isolation for speed",
    }


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for m in installation_methods():
        print(f"[{m['method']}] {m['command']}")
    print()
    for key, desc in key_config_fields().items():
        print(f"  {key}  # {desc}")


if __name__ == "__main__":
    main()
