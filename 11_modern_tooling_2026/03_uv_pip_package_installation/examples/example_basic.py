"""uv pip: ultra-fast package installation API demo."""


def simulate_install(packages: list[str]) -> list[str]:
    return [f"Installed {pkg} via uv (cached)" for pkg in packages]


def resolution_log(packages: list[str]) -> list[str]:
    steps = []
    for i, pkg in enumerate(packages, 1):
        steps.append(f"  [{i}] Resolved {pkg} in <1ms")
    return steps


def main() -> None:
    packages = ["requests==2.31.0", "httpx>=0.27", "pydantic>=2"]
    print("Resolution:")
    for step in resolution_log(packages):
        print(step)
    print("Installation:")
    for line in simulate_install(packages):
        print(f"  {line}")


if __name__ == "__main__":
    main()
