"""
Advanced type hints patterns.

Demonstrates more complex cases including callbacks,
nested types and modern typing techniques.
"""

import functools
from collections.abc import Callable, Mapping, Sequence
from typing import Generic, Literal, ParamSpec, Protocol, TypeAlias, TypeVar

# ============================================================================
# 1. TYPEVAR - GENERIC TYPES
# ============================================================================

T = TypeVar("T")  # Generic type variable


def get_first_element(items: list[T]) -> T | None:
    """
    Return the first element of a list.

    The return type matches the type of elements in the list.
    If it receives list[int], it returns int | None.
    If it receives list[str], it returns str | None.
    """
    return items[0] if items else None


def swap_pair(a: T, b: T) -> tuple[T, T]:
    """Swap two values of the same type."""
    return b, a


# ============================================================================
# 2. LITERAL TYPES - SPECIFIC VALUES
# ============================================================================

# Literal indicates that only certain string values are valid
Mode = Literal["read", "write", "append"]


def open_file(filename: str, mode: Mode) -> str:
    """
    Open a file in a specific mode.

    Args:
        filename: File name
        mode: Can only be "read", "write", or "append"
    """
    return f"Opening {filename} in {mode} mode"


# The type checker will warn you if you use an invalid value:
# open_file("data.txt", "delete")  # Error! "delete" is not a valid Mode


# ============================================================================
# 3. TYPE ALIASES - NAMED COMPLEX TYPES
# ============================================================================

# Define aliases for complex and reusable types
UserId: TypeAlias = int
UserName: TypeAlias = str
UserData: TypeAlias = dict[str, str | int]
UserDatabase: TypeAlias = dict[UserId, UserData]


def add_user(db: UserDatabase, user_id: UserId, name: UserName, age: int) -> None:
    """Add a user to the database."""
    db[user_id] = {"name": name, "age": age}


def get_user(db: UserDatabase, user_id: UserId) -> UserData | None:
    """Get user data."""
    return db.get(user_id)


# ============================================================================
# 4. PROTOCOL - STRUCTURAL TYPING (TYPED DUCK TYPING)
# ============================================================================


class Drawable(Protocol):
    """
    Protocol defines an implicit interface.

    Any class with a draw(self) -> str method
    is considered Drawable without needing explicit inheritance.
    """

    def draw(self) -> str:
        ...


class Circle:
    """Circle is Drawable because it has the draw method."""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"⭕ Circle with radius {self.radius}"


class Square:
    """Square is also Drawable."""

    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"⬜ Square with side {self.side}"


def render_shape(shape: Drawable) -> None:
    """
    Render any object that implements the Drawable protocol.

    It does not need explicit inheritance, only the draw method.
    """
    print(shape.draw())


# ============================================================================
# 5. CALLABLE CON PARAMSPEC (Python 3.10+)
# ============================================================================

P = ParamSpec("P")  # Captures the parameters of a function
R = TypeVar("R")  # Return type


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator that preserves the types of the wrapped function.

    ParamSpec allows the type checker to understand that the decorator
    does not change the function signature.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result

    return wrapper


@log_calls
def multiply(a: int, b: int) -> int:
    """The type checker knows that multiply(int, int) -> int."""
    return a * b


# ============================================================================
# 6. GENERIC CLASSES
# ============================================================================


class Stack(Generic[T]):
    """
    A generic stack that can hold any type.

    Stack[int] is a stack of integers.
    Stack[str] is a stack of strings.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Add an item to the stack."""
        self._items.append(item)

    def pop(self) -> T | None:
        """Remove and return the last item."""
        return self._items.pop() if self._items else None

    def peek(self) -> T | None:
        """Return the last item without removing it."""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """Check whether the stack is empty."""
        return len(self._items) == 0


# ============================================================================
# 7. CALLBACK PATTERNS
# ============================================================================

# Callback that receives the result of an operation
ResultCallback: TypeAlias = Callable[[int, str], None]


def async_operation(value: int, callback: ResultCallback) -> None:
    """
    Simulate an asynchronous operation that invokes a callback.

    Args:
        value: Value to process
        callback: Function that receives (result: int, status: str)
    """
    result = value * 2
    status = "success" if result > 0 else "error"
    callback(result, status)


def handle_result(result: int, status: str) -> None:
    """Handle the result of the operation."""
    print(f"Result: {result}, Status: {status}")


# ============================================================================
# 8. COLLECTIONS.ABC - ABSTRACT INTERFACES
# ============================================================================


def process_sequence(data: Sequence[int]) -> int:
    """
    Accept any sequence (list, tuple, range, etc.).

    Sequence is more flexible than list[int] because it accepts
    any type that implements the sequence protocol.
    """
    return sum(data)


def merge_mappings(m1: Mapping[str, int], m2: Mapping[str, int]) -> dict[str, int]:
    """
    Accept any mapping (dict, OrderedDict, ChainMap, etc.).

    Mapping is read-only; MutableMapping allows modification.
    """
    result = dict(m1)
    result.update(m2)
    return result


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # TypeVar - generic type
    numbers = [1, 2, 3, 4, 5]
    first_num = get_first_element(numbers)
    print(f"First number: {first_num}")

    names = ["Alice", "Bob", "Charlie"]
    first_name = get_first_element(names)
    print(f"First name: {first_name}")

    # Literal types
    result = open_file("data.txt", "read")
    print(result)

    # Type aliases
    user_db: UserDatabase = {}
    add_user(user_db, 1, "Alice", 30)
    add_user(user_db, 2, "Bob", 25)
    user = get_user(user_db, 1)
    print(f"User: {user}")

    # Protocol - structural typing
    circle = Circle(5.0)
    square = Square(10.0)
    render_shape(circle)
    render_shape(square)

    # Decorator with ParamSpec
    result = multiply(5, 3)
    print(f"5 * 3 = {result}")

    # Generic class
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    print(f"Peek: {int_stack.peek()}")
    print(f"Pop: {int_stack.pop()}")

    str_stack: Stack[str] = Stack()
    str_stack.push("Hello")
    str_stack.push("World")
    print(f"Peek: {str_stack.peek()}")

    # Callbacks
    async_operation(21, handle_result)

    # Collections.abc
    result = process_sequence([1, 2, 3])
    print(f"Sum of list: {result}")

    result = process_sequence((4, 5, 6))
    print(f"Sum of tuple: {result}")

    result = process_sequence(range(1, 4))
    print(f"Sum of range: {result}")
