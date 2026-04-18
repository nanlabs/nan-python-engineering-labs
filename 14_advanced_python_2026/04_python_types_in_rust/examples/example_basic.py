"""
Type conversion between Python and Rust.
Shows how Python types map to Rust primitives.
"""

def handle_int(value: int) -> int:
    """Process integer."""
    return value * 2

def handle_string(text: str) -> str:
    """Process string."""
    return text.upper()

def handle_list(items: list) -> list:
    """Process list of integers."""
    return [x * 2 for x in items]

def handle_dict(data: dict) -> dict:
    """Process dictionary."""
    return {k: v * 2 if isinstance(v, (int, float)) else v for k, v in data.items()}

if __name__ == "__main__":
    print("Int:", handle_int(5))
    print("String:", handle_string("rust"))
    print("List:", handle_list([1, 2, 3]))
    print("Dict:", handle_dict({"x": 10, "y": 20}))
