"""
Basic examples of type hints in Python.

This file demonstrates the fundamental use of type annotations
for variables, functions, and collections.
"""

from typing import Optional, List, Dict, Tuple, Set, Union, Callable, Any


# ============================================================================
# 1. PRIMITIVE TYPES
# ============================================================================

def add_numbers(a: int, b: int) -> int:
    """
    Add two integer numbers.
    
    Args:
        a: First integer number
        b: Second integer number
        
    Returns:
        The sum of a and b
    """
    return a + b


def format_greeting(name: str, age: int) -> str:
    """Format a custom greeting."""
    return f"Hola {name}, tienes {age} años"


def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0.0


# ============================================================================
# 2. OPTIONAL AND DEFAULT VALUES
# ============================================================================

def find_user_by_id(user_id: int, users: Dict[int, str]) -> Optional[str]:
    """
    Find a user by ID.
    
    Returns:
        The user name if it exists, otherwise None.
    """
    return users.get(user_id)


def create_user(name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
    """
    Create a user dictionary.
    
    Age is optional and can be None.
    """
    user = {"name": name, "email": email}
    if age is not None:
        user["age"] = age
    return user


# ============================================================================
# 3. GENERIC COLLECTIONS
# ============================================================================

def merge_dictionaries(
    dict1: Dict[str, int],
    dict2: Dict[str, int]
) -> Dict[str, int]:
    """Merge two dictionaries; dict2 overrides values from dict1."""
    result = dict1.copy()
    result.update(dict2)
    return result


def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Return only the even numbers from the list."""
    return [n for n in numbers if n % 2 == 0]


def get_unique_values(items: List[str]) -> Set[str]:
    """Convert a list into a set of unique values."""
    return set(items)


def split_name(full_name: str) -> Tuple[str, str]:
    """
    Split a full name into first name and last name.
    
    Returns:
        A tuple (first_name, last_name)
    """
    parts = full_name.split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], ""


# ============================================================================
# 4. TYPE UNIONS (Python 3.10+)
# ============================================================================

def parse_id(value: int | str) -> int:
    """
    Convert an ID to an integer from int or str.
    
    Equivalent to Union[int, str] in Python < 3.10
    """
    if isinstance(value, str):
        return int(value)
    return value


def process_data(data: list[int] | list[str]) -> int:
    """
    Process data that can be a list of integers or strings.
    
    Returns:
        The number of processed elements
    """
    return len(data)


# ============================================================================
# 5. CALLABLES (FUNCTIONS AS PARAMETERS)
# ============================================================================

def apply_to_all(items: List[int], func: Callable[[int], int]) -> List[int]:
    """
    Apply a function to each item in the list.
    
    Args:
        items: List of integers
        func: Function that takes an int and returns an int
        
    Returns:
        New list with the function applied
    """
    return [func(item) for item in items]


def double(x: int) -> int:
    """Double a number."""
    return x * 2


def square(x: int) -> int:
    """Square a number."""
    return x * x


# ============================================================================
# 6. COMPLEX NESTED TYPES
# ============================================================================

def group_by_key(
    items: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group dictionaries by a specific key.
    
    Args:
        items: List of dictionaries with at least the key "category"
        
    Returns:
        Dictionary where each key is a category and the value is the list of items
    """
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        category = item.get("category", "unknown")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped


# ============================================================================
# 7. VARIABLES ANOTADAS
# ============================================================================

# Variable annotations (Python 3.6+)
user_count: int = 0
active_users: List[str] = []
configuration: Dict[str, str | int | bool] = {
    "host": "localhost",
    "port": 8000,
    "debug": True
}


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Basic types
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
    
    greeting = format_greeting("Alice", 30)
    print(greeting)
    
    # Optional
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    user = find_user_by_id(2, users)
    print(f"User found: {user}")
    
    user = find_user_by_id(999, users)
    print(f"User not found: {user}")
    
    # Collections
    numbers = [1, 2, 3, 4, 5, 6]
    even = filter_even_numbers(numbers)
    print(f"Even numbers: {even}")
    
    names = ["Ana", "Bob", "Ana", "Charlie", "Bob"]
    unique = get_unique_values(names)
    print(f"Unique names: {unique}")
    
    # Callables
    numbers = [1, 2, 3, 4, 5]
    doubled = apply_to_all(numbers, double)
    squared = apply_to_all(numbers, square)
    print(f"Doubled: {doubled}")
    print(f"Squared: {squared}")
    
    # Lambda with inferred type hints
    tripled = apply_to_all(numbers, lambda x: x * 3)
    print(f"Tripled: {tripled}")
    
    # Union types
    id1 = parse_id(123)
    id2 = parse_id("456")
    print(f"Parsed IDs: {id1}, {id2}")
    
    # Nested types
    products = [
        {"name": "Laptop", "category": "Electronics", "price": 999},
        {"name": "Mouse", "category": "Electronics", "price": 25},
        {"name": "Desk", "category": "Furniture", "price": 299},
    ]
    grouped = group_by_key(products)
    print(f"Products grouped by category:")
    for category, items in grouped.items():
        print(f"  {category}: {len(items)} items")
