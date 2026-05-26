"""uv introduction: demonstrate the key concepts of the uv package manager."""


def uv_summary() -> dict[str, str]:
    return {
        "tool": "uv",
        "language": "Rust",
        "speed": "10-100x faster than pip",
        "features": "packaging, venvs, scripts, workspaces",
    }


def compare_install_time(packages: list[str]) -> list[str]:
    return [f"uv add {pkg}  # ~10ms" for pkg in packages]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    print(uv_summary())
    print(compare_install_time(["requests", "fastapi", "pydantic"]))


if __name__ == "__main__":
    main()
