"""Ruff pyproject.toml configuration demo."""


def build_ruff_config(
    line_length: int = 88,
    select: list[str] | None = None,
    ignore: list[str] | None = None,
) -> dict:
    select = select or ["E", "W", "F", "I", "UP"]
    ignore = ignore or ["E501"]
    return {
        "tool": {
            "ruff": {
                "line-length": line_length,
                "select": select,
                "ignore": ignore,
                "fix": True,
            }
        }
    }


def render_toml(config: dict) -> list[str]:
    lines = []
    for section, values in config.items():
        for subsection, settings in values.items():
            lines.append(f"[{section}.{subsection}]")
            for k, v in settings.items():
                if isinstance(v, list):
                    lines.append(f'{k} = {v}')
                else:
                    lines.append(f'{k} = {v!r}')
    return lines


def main() -> None:
    cfg = build_ruff_config(line_length=100, select=["E", "W", "F", "I", "S"])
    for line in render_toml(cfg):
        print(line)


if __name__ == "__main__":
    main()
