"""
Advanced Exercise: Type Hints - Type Validation Decorator

OBJECTIVE:
Create a @validate_types decorator that verifies at runtime that the arguments
passed to a function match its type hints.

REQUIREMENTS:
1. The decorator must work with any function that has type hints
2. It must validate parameter types before executing the function
3. It must validate the return value type after execution
4. If there is a type mismatch, it must raise TypeError with a descriptive message
5. It must handle:
   - Basic types: int, str, float, bool
   - Optional[T] (accepts T or None)
   - Union[T1, T2, ...] o T1 | T2 (accepts any of the types)
   - List[T], Dict[K, V] (validate the container type, not the elements)
   - Functions without type hints (do not validate)
   - Functions that return None

CHALLENGES:
- Use the inspect module to obtain the function signature
- Use typing.get_type_hints() to extract type hints
- Handle special types from the typing module (Union, Optional, etc)
- Use typing.get_origin() and typing.get_args() to decompose generic types

USAGE EXAMPLE:
@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)      # OK: returns 3
add("1", "2")  # ERROR: TypeError - expected int, got str

@validate_types
def find_user(user_id: int) -> Optional[str]:
    return "Alice" if user_id == 1 else None

find_user(1)   # OK: returns "Alice"
find_user(2)   # OK: returns None
find_user("1") # ERROR: TypeError
"""

import functools
from collections.abc import Callable
from typing import Any


def validate_types(func: Callable) -> Callable:
    """
    Decorator that validates type hints at runtime.

    Verify that passed arguments and the return value
    match the type hints declared on the function.

    Args:
        func: Function to decorate (must have type hints)

    Returns:
        Function decorated with type validation

    Raises:
        TypeError: If there is a mismatch between expected and received types

    Examples:
        >>> @validate_types
        ... def greet(name: str, age: int) -> str:
        ...     return f"{name} has {age} years"
        >>> greet("Alice", 30)
        'Alice has 30 years'
        >>> greet(123, 30)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError: Parameter 'name' expected <class 'str'>, got <class 'int'>
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper that performs validation."""

        # TODO: Step 1 - Get function type hints
        # Use: type_hints = get_type_hints(func)
        # This returns a dict: {"param_name": type, "return": return_type}

        # TODO: Step 2 - Get the function signature
        # Use: sig = inspect.signature(func)
        # Use: bound = sig.bind(*args, **kwargs)
        # bound.arguments is a dict of {param_name: value}

        # TODO: Step 3 - Validate each parameter
        # For each parameter in bound.arguments:
        #   - Get the expected type hint from type_hints
        #   - Get the current value
        #   - Call _check_type(param_name, value, expected_type)

        # TODO: Step 4 - Execute the original function
        # result = func(*args, **kwargs)

        # TODO: Step 5 - Validate the return type if it exists
        # If "return" is in type_hints:
        #   - Call _check_type("return", result, type_hints["return"])

        # TODO: Step 6 - Return the result
        # return result

        pass

    return wrapper


def _check_type(param_name: str, value: Any, expected_type: Any) -> None:
    """
    Verify that a value matches the expected type.

    This helper function handles complex validation logic
    including Optional, Union, and generic types.

    Args:
        param_name: Parameter name (for error messages)
        value: Value to validate
        expected_type: Expected type (can be Union, Optional, etc)

    Raises:
        TypeError: If the value does not match the expected type
    """
    # TODO: Implement type validation

    # Special cases:
    # 1. If expected_type is None or type(None), only accept None
    # 2. If expected_type is Union or has __origin__ == Union:
    #    - Get the types with get_args(expected_type)
    #    - Validate that value is an instance of one of them
    # 3. If expected_type is Optional (Union[T, None]):
    #    - Accept None or type T
    # 4. If expected_type is a generic type (List, Dict, etc):
    #    - Validate only the container type with get_origin()
    #    - Example: List[int] -> validate isinstance(value, list)
    # 5. For basic types, use isinstance(value, expected_type)

    # Hints:
    # - get_origin(List[int]) returns list
    # - get_args(Union[int, str]) returns (int, str)
    # - get_args(Optional[int]) returns (int, type(None))
    # - type(None) is the NoneType class

    pass


# ============================================================================
# AUXILIARY TESTS (DO NOT MODIFY)
# ============================================================================

if __name__ == "__main__":
    # These tests are used to verify your implementation
    # DO NOT modify them; implement the functions above

    print("Testing validate_types decorator...")

    # Test 1: Basic types
    @validate_types
    def add(a: int, b: int) -> int:
        return a + b

    try:
        result = add(1, 2)
        print(f"✓ Test 1.1 passed: add(1, 2) = {result}")
    except TypeError as e:
        print(f"✗ Test 1.1 failed: {e}")

    try:
        result = add("1", "2")
        print("✗ Test 1.2 failed: Should have raised TypeError")
    except TypeError:
        print("✓ Test 1.2 passed: Correctly rejected add('1', '2')")

    # Test 2: Optional
    @validate_types
    def find_user(user_id: int) -> str | None:
        return "Alice" if user_id == 1 else None

    try:
        result = find_user(1)
        print(f"✓ Test 2.1 passed: find_user(1) = {result}")
    except TypeError as e:
        print(f"✗ Test 2.1 failed: {e}")

    try:
        result = find_user(2)
        print(f"✓ Test 2.2 passed: find_user(2) = {result} (None is valid)")
    except TypeError as e:
        print(f"✗ Test 2.2 failed: {e}")

    # Test 3: Union types
    @validate_types
    def process_id(value: int | str) -> int:
        if isinstance(value, str):
            return int(value)
        return value

    try:
        result = process_id(123)
        print(f"✓ Test 3.1 passed: process_id(123) = {result}")
    except TypeError as e:
        print(f"✗ Test 3.1 failed: {e}")

    try:
        result = process_id("456")
        print(f"✓ Test 3.2 passed: process_id('456') = {result}")
    except TypeError as e:
        print(f"✗ Test 3.2 failed: {e}")

    # Test 4: Generic collections
    @validate_types
    def sum_list(numbers: list[int]) -> int:
        return sum(numbers)

    try:
        result = sum_list([1, 2, 3])
        print(f"✓ Test 4.1 passed: sum_list([1, 2, 3]) = {result}")
    except TypeError as e:
        print(f"✗ Test 4.1 failed: {e}")

    try:
        result = sum_list("123")
        print("✗ Test 4.2 failed: Should have raised TypeError")
    except TypeError:
        print("✓ Test 4.2 passed: Correctly rejected sum_list('123')")

    print("\n¡Tests completados!")
