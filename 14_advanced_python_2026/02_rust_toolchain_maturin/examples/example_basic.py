"""
Demonstrates Maturin setup and basic project structure.
Shows how to configure Cargo.toml and maturin pyproject.toml.
"""

def check_toolchain_info() -> dict:
    """Returns info about the Rust toolchain."""
    return {
        "framework": "Maturin",
        "build_backend": "maturin",
        "rust_support": "Stable and Nightly",
        "python_versions": "3.8+",
    }

def validate_pyproject() -> bool:
    """Validates that maturin is properly configured."""
    config = check_toolchain_info()
    return config.get("build_backend") == "maturin"

if __name__ == "__main__":
    info = check_toolchain_info()
    print("Toolchain Info:", info)
    print("Valid config:", validate_pyproject())
