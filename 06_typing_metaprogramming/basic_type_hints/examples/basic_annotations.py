"""
Ejemplos básicos de type hints en Python.

Este archivo demuestra el uso fundamental de anotaciones de tipo
para variables, funciones y colecciones.
"""

from typing import Optional, List, Dict, Tuple, Set, Union, Callable, Any


# ============================================================================
# 1. TIPOS PRIMITIVOS
# ============================================================================

def add_numbers(a: int, b: int) -> int:
    """
    Suma dos números enteros.
    
    Args:
        a: Primer número entero
        b: Segundo número entero
        
    Returns:
        La suma de a y b
    """
    return a + b


def format_greeting(name: str, age: int) -> str:
    """Formatea un saludo personalizado."""
    return f"Hola {name}, tienes {age} años"


def calculate_average(numbers: List[float]) -> float:
    """Calcula el promedio de una lista de números."""
    return sum(numbers) / len(numbers) if numbers else 0.0


# ============================================================================
# 2. OPTIONAL Y VALORES POR DEFECTO
# ============================================================================

def find_user_by_id(user_id: int, users: Dict[int, str]) -> Optional[str]:
    """
    Busca un usuario por ID.
    
    Returns:
        El nombre del usuario si existe, None en caso contrario.
    """
    return users.get(user_id)


def create_user(name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
    """
    Crea un diccionario de usuario.
    
    La edad es opcional y puede ser None.
    """
    user = {"name": name, "email": email}
    if age is not None:
        user["age"] = age
    return user


# ============================================================================
# 3. COLECCIONES GENÉRICAS
# ============================================================================

def merge_dictionaries(
    dict1: Dict[str, int],
    dict2: Dict[str, int]
) -> Dict[str, int]:
    """Fusiona dos diccionarios, dict2 sobrescribe valores de dict1."""
    result = dict1.copy()
    result.update(dict2)
    return result


def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Retorna solo los números pares de la lista."""
    return [n for n in numbers if n % 2 == 0]


def get_unique_values(items: List[str]) -> Set[str]:
    """Convierte una lista en un conjunto de valores únicos."""
    return set(items)


def split_name(full_name: str) -> Tuple[str, str]:
    """
    Divide un nombre completo en nombre y apellido.
    
    Returns:
        Una tupla (nombre, apellido)
    """
    parts = full_name.split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], ""


# ============================================================================
# 4. UNIONES DE TIPOS (Python 3.10+)
# ============================================================================

def parse_id(value: int | str) -> int:
    """
    Convierte un ID a entero desde int o str.
    
    Equivalente a Union[int, str] en Python < 3.10
    """
    if isinstance(value, str):
        return int(value)
    return value


def process_data(data: list[int] | list[str]) -> int:
    """
    Procesa datos que pueden ser lista de enteros o strings.
    
    Returns:
        El número de elementos procesados
    """
    return len(data)


# ============================================================================
# 5. CALLABLES (FUNCIONES COMO PARÁMETROS)
# ============================================================================

def apply_to_all(items: List[int], func: Callable[[int], int]) -> List[int]:
    """
    Aplica una función a cada elemento de la lista.
    
    Args:
        items: Lista de enteros
        func: Función que toma un int y retorna un int
        
    Returns:
        Nueva lista con la función aplicada
    """
    return [func(item) for item in items]


def double(x: int) -> int:
    """Duplica un número."""
    return x * 2


def square(x: int) -> int:
    """Eleva un número al cuadrado."""
    return x * x


# ============================================================================
# 6. TIPOS ANIDADOS COMPLEJOS
# ============================================================================

def group_by_key(
    items: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Agrupa diccionarios por un key específico.
    
    Args:
        items: Lista de diccionarios con al menos la key "category"
        
    Returns:
        Diccionario donde cada key es una categoría y el value es la lista de items
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

# Anotaciones de variables (Python 3.6+)
user_count: int = 0
active_users: List[str] = []
configuration: Dict[str, str | int | bool] = {
    "host": "localhost",
    "port": 8000,
    "debug": True
}


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # Tipos básicos
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
    
    greeting = format_greeting("Alice", 30)
    print(greeting)
    
    # Optional
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    user = find_user_by_id(2, users)
    print(f"Usuario encontrado: {user}")
    
    user = find_user_by_id(999, users)
    print(f"Usuario no encontrado: {user}")
    
    # Colecciones
    numbers = [1, 2, 3, 4, 5, 6]
    even = filter_even_numbers(numbers)
    print(f"Números pares: {even}")
    
    names = ["Ana", "Bob", "Ana", "Charlie", "Bob"]
    unique = get_unique_values(names)
    print(f"Nombres únicos: {unique}")
    
    # Callables
    numbers = [1, 2, 3, 4, 5]
    doubled = apply_to_all(numbers, double)
    squared = apply_to_all(numbers, square)
    print(f"Duplicados: {doubled}")
    print(f"Cuadrados: {squared}")
    
    # Lambda con type hint inferido
    tripled = apply_to_all(numbers, lambda x: x * 3)
    print(f"Triplicados: {tripled}")
    
    # Union types
    id1 = parse_id(123)
    id2 = parse_id("456")
    print(f"IDs parseados: {id1}, {id2}")
    
    # Tipos anidados
    products = [
        {"name": "Laptop", "category": "Electronics", "price": 999},
        {"name": "Mouse", "category": "Electronics", "price": 25},
        {"name": "Desk", "category": "Furniture", "price": 299},
    ]
    grouped = group_by_key(products)
    print(f"Productos agrupados por categoría:")
    for category, items in grouped.items():
        print(f"  {category}: {len(items)} items")
