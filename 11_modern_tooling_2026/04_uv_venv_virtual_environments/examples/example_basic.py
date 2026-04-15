"""uv venv: virtual environment creation and activation."""


def venv_lifecycle() -> list[tuple[str, str]]:
    return [
        ("uv venv .venv",                    "create venv at .venv"),
        ("source .venv/bin/activate",         "activate on Unix"),
        (".venv\\Scripts\\activate",       "activate on Windows"),
        ("uv pip install -r requirements.txt","install into venv"),
    ]


def inspect_venv(path: str) -> dict[str, str]:
    return {
        "location": path,
        "python": "3.12.x",
        "total_packages": "0 (fresh)",
        "isolation": "full",
    }


def main() -> None:
    for cmd, desc in venv_lifecycle():
        print(f"  $ {cmd}  # {desc}")
    print()
    for k, v in inspect_venv(".venv").items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
