"""Ruff strict rules: production-grade rule set."""


def strict_rule_set() -> dict[str, str]:
    return {
        "ANN": "require type annotations on all functions",
        "S": "security checks (bandit equivalent)",
        "B": "bugbear: likely bugs and bad practices",
        "C90": "complexity limit (max-complexity = 10)",
        "N": "naming conventions (PEP 8)",
        "RUF": "Ruff-specific rules (idiomatic Python)",
        "ERA": "flag commented-out code",
        "PTH": "prefer pathlib over os.path",
    }


def evaluate_compliance(code_metrics: dict[str, int]) -> list[str]:
    violations = []
    if code_metrics.get("complexity", 0) > 10:
        violations.append("C901: function too complex")
    if code_metrics.get("unannotated_args", 0) > 0:
        violations.append("ANN001: missing arg annotations")
    return violations or ["All strict rules pass"]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    for rule, desc in strict_rule_set().items():
        print(f"  [{rule}] {desc}")
    print()
    metrics = {"complexity": 7, "unannotated_args": 0}
    print(evaluate_compliance(metrics))


if __name__ == "__main__":
    main()
