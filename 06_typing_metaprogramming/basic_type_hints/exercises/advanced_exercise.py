"""
Advanced Exercise: Type Hints - Type Validation Decorator

OBJECTIVE:
Crear un decorador @validate_types que verifique en runtime que los argumentos
pasados a una función coincidan con sus type hints.

REQUISITOS:
1. El decorador debe funcionar con cualquier función que tenga type hints
2. Debe validar tipos de parámetros antes de ejecutar la función
3. Debe validar el tipo del valor de retorno después de ejecutar
4. Si hay un mismatch de tipos, debe lanzar TypeError con mensaje descriptivo
5. Debe manejar:
   - Tipos básicos: int, str, float, bool
   - Optional[T] (acepta T o None)
   - Union[T1, T2, ...] o T1 | T2 (acepta cualquiera de los tipos)
   - List[T], Dict[K, V] (validar el tipo del contenedor, no los elementos)
   - Funciones sin type hints (no validar)
   - Funciones que retornan None

CHALLENGES:
- Use the inspect module to obtain the function signature
- Usar typing.get_type_hints() para extraer los type hints
- Handle special types from the typing module (Union, Optional, etc)
- Usar typing.get_origin() y typing.get_args() para descomponer tipos genéricos

EJEMPLO DE USO:
@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)      # OK: retorna 3
add("1", "2")  # ERROR: TypeError - esperaba int, recibió str

@validate_types
def find_user(user_id: int) -> Optional[str]:
    return "Alice" if user_id == 1 else None

find_user(1)   # OK: retorna "Alice"
find_user(2)   # OK: retorna None
find_user("1") # ERROR: TypeError
"""

import functools
import inspect
from typing import Any, Callable, get_type_hints, Union, get_origin, get_args


def validate_types(func: Callable) -> Callable:
    """
    Decorador que valida types hints en runtime.
    
    Verifica que los argumentos pasados y el valor de retorno
    coincidan con los type hints declarados en la función.
    
    Args:
        func: Función a decorar (debe tener type hints)
        
    Returns:
        Función decorada con validación de tipos
        
    Raises:
        TypeError: Si hay un mismatch entre tipos esperados y recibidos
    
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
        """Wrapper que ejecuta la validación."""
        
        # TODO: Paso 1 - Obtener type hints de la función
        # Usar: type_hints = get_type_hints(func)
        # Esto retorna un dict: {"param_name": type, "return": return_type}
        
        # TODO: Paso 2 - Obtener la signature de la función
        # Usar: sig = inspect.signature(func)
        # Usar: bound = sig.bind(*args, **kwargs)
        # bound.arguments es un dict de {param_name: value}
        
        # TODO: Paso 3 - Validar cada parámetro
        # Para cada parámetro en bound.arguments:
        #   - Obtener el type hint esperado de type_hints
        #   - Obtener el valor actual
        #   - Llamar a _check_type(param_name, value, expected_type)
        
        # TODO: Paso 4 - Ejecutar la función original
        # result = func(*args, **kwargs)
        
        # TODO: Paso 5 - Validar el tipo de retorno si existe
        # Si "return" está en type_hints:
        #   - Llamar a _check_type("return", result, type_hints["return"])
        
        # TODO: Paso 6 - Retornar el resultado
        # return result
        
        pass
    
    return wrapper


def _check_type(param_name: str, value: Any, expected_type: Any) -> None:
    """
    Verifica que un valor coincida con el tipo esperado.
    
    Esta función auxiliar maneja la lógica compleja de validación
    incluyendo Optional, Union, y tipos genéricos.
    
    Args:
        param_name: Nombre del parámetro (para mensajes de error)
        value: Valor a validar
        expected_type: Tipo esperado (puede ser Union, Optional, etc)
        
    Raises:
        TypeError: Si el valor no coincide con el tipo esperado
    """
    # TODO: Implementar validación de tipos
    
    # Casos especiales:
    # 1. Si expected_type es None o type(None), solo aceptar None
    # 2. Si expected_type es Union o tiene __origin__ == Union:
    #    - Obtener los tipos con get_args(expected_type)
    #    - Validar que value sea instancia de alguno de ellos
    # 3. Si expected_type es Optional (Union[T, None]):
    #    - Aceptar None o el tipo T
    # 4. Si expected_type es un tipo genérico (List, Dict, etc):
    #    - Validar solo el tipo del contenedor con get_origin()
    #    - Ejemplo: List[int] -> validar isinstance(value, list)
    # 5. Para tipos básicos, usar isinstance(value, expected_type)
    
    # Pistas:
    # - get_origin(List[int]) retorna list
    # - get_args(Union[int, str]) retorna (int, str)
    # - get_args(Optional[int]) retorna (int, type(None))
    # - type(None) es la clase NoneType
    
    pass


# ============================================================================
# TESTS AUXILIARES (NO MODIFICAR)
# ============================================================================

if __name__ == "__main__":
    # Estos tests son para verificar tu implementación
    # NO los modifiques, implementa las funciones arriba
    
    print("Testing validate_types decorator...")
    
    # Test 1: Tipos básicos
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
        print(f"✗ Test 1.2 failed: Should have raised TypeError")
    except TypeError:
        print(f"✓ Test 1.2 passed: Correctly rejected add('1', '2')")
    
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
    
    # Test 4: Colecciones genéricas
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
        print(f"✗ Test 4.2 failed: Should have raised TypeError")
    except TypeError:
        print(f"✓ Test 4.2 passed: Correctly rejected sum_list('123')")
    
    print("\n¡Tests completados!")
