"""Ruff introduction: lint an in-memory code fragment."""


def lint_snippet(code: str) -> list[str]:
    issues = []
    for i, line in enumerate(code.splitlines(), 1):
        if "	" in line:
            issues.append(f"W191 line:{i} indentation contains tabs")
        if "==" in line and "if" not in line and "==" != line.strip():
            pass  # simplified heuristic only
        if len(line) > 88:
            issues.append(f"E501 line:{i} too long ({len(line)} > 88 chars)")
    return issues or ["No issues found"]


SAMPLE_CODE = """def add(a,b):
	return a+b
"""


def main() -> None:
    print(f"Linting snippet ({len(SAMPLE_CODE.splitlines())} lines):")
    for issue in lint_snippet(SAMPLE_CODE):
        print(f"  {issue}")


if __name__ == "__main__":
    main()
