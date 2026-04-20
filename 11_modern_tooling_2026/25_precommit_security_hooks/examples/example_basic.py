"""pre-commit security hooks: detect-secrets and bandit patterns."""


def scan_for_secrets(code_lines: list[str]) -> list[str]:
    patterns = ["password", "api_key", "secret", "token", "auth"]
    flagged = []
    for i, line in enumerate(code_lines, 1):
        low = line.lower()
        if any(p in low for p in patterns) and "=" in line:
            flagged.append(f"  Line {i}: potential secret → {line.strip()[:60]}")
    return flagged or ["  No secrets detected"]


def bandit_check(code_lines: list[str]) -> list[str]:
    issues = []
    for i, line in enumerate(code_lines, 1):
        if "eval(" in line:
            issues.append(f"  B307 line:{i} use of eval() detected")
        if "exec(" in line:
            issues.append(f"  B102 line:{i} use of exec() detected")
    return issues or ["  No bandit issues detected"]


def main() -> None:
    """Entry point to demonstrate the implementation."""
    sample = ['api_key = "hardcoded_key_12345"', "result = eval(user_input)", 'name = "Alice"']
    print("Secret scan:")
    for line in scan_for_secrets(sample):
        print(line)
    print("Bandit scan:")
    for line in bandit_check(sample):
        print(line)


if __name__ == "__main__":
    main()
