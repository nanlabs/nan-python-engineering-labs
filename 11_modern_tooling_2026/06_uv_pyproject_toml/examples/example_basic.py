"""uv and pyproject.toml: declarative project metadata and dependencies."""


def parse_pyproject_snippet(snippet: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current_section = ""
    for line in snippet.splitlines():
        line = line.strip()
        if line.startswith("["):
            current_section = line
            result[current_section] = []
        elif line and current_section:
            result[current_section].append(line)
    return result


SAMPLE = """[project]
name = "my-app"
version = "1.0.0"
requires-python = ">=3.12"

[project.dependencies]
httpx = ">=0.27"
pydantic = ">=2"
"""


def main() -> None:
    parsed = parse_pyproject_snippet(SAMPLE)
    for section, lines in parsed.items():
        print(f"{section}")
        for line in lines:
            print(f"  {line}")


if __name__ == "__main__":
    main()
