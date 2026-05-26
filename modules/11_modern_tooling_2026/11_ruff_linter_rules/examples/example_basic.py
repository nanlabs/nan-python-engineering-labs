"""Ruff linter rules: categories and selectors."""


def rule_categories() -> dict[str, str]:
    return {
        "E": "pycodestyle errors",
        "W": "pycodestyle warnings",
        "F": "pyflakes",
        "I": "isort (import order)",
        "N": "pep8-naming",
        "UP": "pyupgrade (modern syntax)",
        "S": "flake8-bandit (security)",
        "B": "flake8-bugbear",
        "C90": "mccabe complexity",
        "ANN": "flake8-annotations",
    }


def filter_rules(categories: dict[str, str], prefix: str) -> dict[str, str]:
    return {k: v for k, v in categories.items() if k.startswith(prefix)}


def main() -> None:
    """Entry point to demonstrate the implementation."""
    cats = rule_categories()
    print(f"Total rule categories: {len(cats)}")
    for code, desc in cats.items():
        print(f"  [{code}] {desc}")
    print()
    security = filter_rules(cats, "S")
    print(f"Security rules: {security}")


if __name__ == "__main__":
    main()
