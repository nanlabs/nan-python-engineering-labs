"""
Automatic type conversions from Python to Rust and vice versa.
PyO3 handles most conversions transparently.
"""

def auto_convert_number(val) -> int:
    """Automatic conversion of numeric types."""
    return int(val) * 10

def auto_convert_string(val) -> str:
    """Automatic string conversion."""
    return str(val).lower()

def auto_convert_sequence(val: list) -> list:
    """Automatic sequence conversion."""
    return [x for x in val if x]

if __name__ == "__main__":
    print("Number:", auto_convert_number(3.14))
    print("String:", auto_convert_string("RUST"))
    print("Sequence:", auto_convert_sequence([1, 0, 2, None, 3]))
