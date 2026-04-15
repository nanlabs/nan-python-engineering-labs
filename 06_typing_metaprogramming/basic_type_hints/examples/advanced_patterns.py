"""
Advanced type hints patterns.

Demonstrates more complex cases including callbacks,
nested types and modern typing techniques.
"""

from typing import (
    Callable, TypeVar, Generic, Protocol, 
    Literal, TypeAlias, ParamSpec, Concatenate
)
from collections.abc import Sequence, Mapping
import functools


# ============================================================================
# 1. TYPEVAR - TIPOS GENÉRICOS
# ============================================================================

T = TypeVar('T')  # Variable de tipo genérica


def get_first_element(items: list[T]) -> T | None:
    """
    Retorna el primer elemento de una lista.
    
    El tipo de retorno es el mismo que el tipo de elementos en la lista.
    Si recibe list[int], retorna int | None.
    Si recibe list[str], retorna str | None.
    """
    return items[0] if items else None


def swap_pair(a: T, b: T) -> tuple[T, T]:
    """Intercambia dos valores del mismo tipo."""
    return b, a


# ============================================================================
# 2. LITERAL TYPES - VALORES ESPECÍFICOS
# ============================================================================

# Literal indica que solo ciertos valores string son válidos
Mode = Literal["read", "write", "append"]


def open_file(filename: str, mode: Mode) -> str:
    """
    Abre un archivo en un modo específico.
    
    Args:
        filename: Nombre del archivo
        mode: Solo puede ser "read", "write" o "append"
    """
    return f"Opening {filename} in {mode} mode"


# Type checker advertirá si usas un valor inválido:
# open_file("data.txt", "delete")  # Error! "delete" no es un Mode válido


# ============================================================================
# 3. TYPE ALIASES - TIPOS COMPLEJOS CON NOMBRE
# ============================================================================

# Define aliases para tipos complejos y reutilizables
UserId: TypeAlias = int
UserName: TypeAlias = str
UserData: TypeAlias = dict[str, str | int]
UserDatabase: TypeAlias = dict[UserId, UserData]


def add_user(db: UserDatabase, user_id: UserId, name: UserName, age: int) -> None:
    """Añade un usuario a la base de datos."""
    db[user_id] = {"name": name, "age": age}


def get_user(db: UserDatabase, user_id: UserId) -> UserData | None:
    """Obtiene datos de un usuario."""
    return db.get(user_id)


# ============================================================================
# 4. PROTOCOL - STRUCTURAL TYPING (DUCK TYPING TIPADO)
# ============================================================================

class Drawable(Protocol):
    """
    Protocol define una interfaz implícita.
    
    Cualquier clase con un método draw(self) -> str
    es considerada Drawable sin necesidad de heredar explícitamente.
    """
    def draw(self) -> str: ...


class Circle:
    """Circle es Drawable porque tiene el método draw."""
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return f"⭕ Circle with radius {self.radius}"


class Square:
    """Square también es Drawable."""
    def __init__(self, side: float):
        self.side = side
    
    def draw(self) -> str:
        return f"⬜ Square with side {self.side}"


def render_shape(shape: Drawable) -> None:
    """
    Renderiza cualquier objeto que implemente el protocol Drawable.
    
    No necesita herencia explícita, solo el método draw.
    """
    print(shape.draw())


# ============================================================================
# 5. CALLABLE CON PARAMSPEC (Python 3.10+)
# ============================================================================

P = ParamSpec('P')  # Captura parámetros de una función
R = TypeVar('R')    # Tipo de retorno


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorador que preserva los tipos de la función decorada.
    
    ParamSpec permite que el type checker entienda que el decorador
    no cambia la signature de la función.
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
    """El type checker sabe que multiply(int, int) -> int."""
    return a * b


# ============================================================================
# 6. GENERIC CLASSES
# ============================================================================

class Stack(Generic[T]):
    """
    Una pila genérica que puede contener cualquier tipo.
    
    Stack[int] es una pila de enteros.
    Stack[str] es una pila de strings.
    """
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        """Añade un item a la pila."""
        self._items.append(item)
    
    def pop(self) -> T | None:
        """Remueve y retorna el último item."""
        return self._items.pop() if self._items else None
    
    def peek(self) -> T | None:
        """Retorna el último item sin removerlo."""
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        """Verifica si la pila está vacía."""
        return len(self._items) == 0


# ============================================================================
# 7. CALLBACK PATTERNS
# ============================================================================

# Callback que recibe el resultado de una operación
ResultCallback: TypeAlias = Callable[[int, str], None]


def async_operation(value: int, callback: ResultCallback) -> None:
    """
    Simula una operación asíncrona que llama un callback.
    
    Args:
        value: Valor a procesar
        callback: Función que recibe (result: int, status: str)
    """
    result = value * 2
    status = "success" if result > 0 else "error"
    callback(result, status)


def handle_result(result: int, status: str) -> None:
    """Maneja el resultado de la operación."""
    print(f"Result: {result}, Status: {status}")


# ============================================================================
# 8. COLLECTIONS.ABC - INTERFACES ABSTRACTAS
# ============================================================================

def process_sequence(data: Sequence[int]) -> int:
    """
    Acepta cualquier secuencia (list, tuple, range, etc).
    
    Sequence es más flexible que list[int] porque acepta
    cualquier tipo que implemente el protocol de secuencia.
    """
    return sum(data)


def merge_mappings(m1: Mapping[str, int], m2: Mapping[str, int]) -> dict[str, int]:
    """
    Acepta cualquier mapeo (dict, OrderedDict, ChainMap, etc).
    
    Mapping es read-only, MutableMapping permite modificación.
    """
    result = dict(m1)
    result.update(m2)
    return result


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # TypeVar - tipo genérico
    numbers = [1, 2, 3, 4, 5]
    first_num = get_first_element(numbers)
    print(f"Primer número: {first_num}")
    
    names = ["Alice", "Bob", "Charlie"]
    first_name = get_first_element(names)
    print(f"Primer nombre: {first_name}")
    
    # Literal types
    result = open_file("data.txt", "read")
    print(result)
    
    # Type aliases
    user_db: UserDatabase = {}
    add_user(user_db, 1, "Alice", 30)
    add_user(user_db, 2, "Bob", 25)
    user = get_user(user_db, 1)
    print(f"Usuario: {user}")
    
    # Protocol - structural typing
    circle = Circle(5.0)
    square = Square(10.0)
    render_shape(circle)
    render_shape(square)
    
    # Decorador con ParamSpec
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
