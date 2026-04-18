"""
Creating Python modules in Rust with PyO3.
Module initialization and function export.
"""

def module_function(x: int) -> int:
    """Module-level function."""
    return x ** 2

class ModuleClass:
    """Class in Rust module."""
    def __init__(self, value: int):
        self.value = value

def get_module_metadata() -> dict:
    """Module metadata."""
    return {
        "name": "rust_module",
        "version": "0.1.0",
        "exports": ["module_function", "ModuleClass"],
    }

if __name__ == "__main__":
    print("Result:", module_function(5))
    print("Metadata:", get_module_metadata())
