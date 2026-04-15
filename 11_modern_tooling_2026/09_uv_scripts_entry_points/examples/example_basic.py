"""uv scripts: define and run inline scripts with dependencies."""


def script_header(dependencies: list[str]) -> str:
    deps = "\n".join(f'#   "{d}"' for d in dependencies)
    return f"""# /// script
# requires-python = ">=3.12"
# dependencies = [
{deps}
# ]
# ///"""


def entry_point(module: str, func: str) -> dict[str, str]:
    return {"module": module, "function": func, "invoker": f"uv run {module}.py"}


def main() -> None:
    print(script_header(["httpx>=0.27", "rich>=13"]))
    print()
    ep = entry_point("report", "main")
    print(ep)


if __name__ == "__main__":
    main()
