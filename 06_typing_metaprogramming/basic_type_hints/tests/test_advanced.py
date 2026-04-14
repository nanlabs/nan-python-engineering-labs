"""
Tests para el ejercicio avanzado de type hints - decorador validate_types.
"""

import pytest
import sys
from pathlib import Path
from typing import Optional, Union

# Añadir el directorio de ejercicios al path
exercises_dir = Path(__file__).parent.parent / "exercises"
sys.path.insert(0, str(exercises_dir))

try:
    from advanced_exercise import validate_types
    SOLUTION_EXISTS = True
except (ImportError, AttributeError):
    SOLUTION_EXISTS = False


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesBasic:
    """Tests básicos del decorador validate_types."""
    
    def test_validates_int_parameter(self):
        """Valida parámetros de tipo int."""
        @validate_types
        def add(a: int, b: int) -> int:
            return a + b
        
        # Debe funcionar con ints
        assert add(1, 2) == 3
        
        # Debe fallar con strings
        with pytest.raises(TypeError):
            add("1", "2")
    
    def test_validates_str_parameter(self):
        """Valida parámetros de tipo str."""
        @validate_types
        def greet(name: str) -> str:
            return f"Hello {name}"
        
        assert greet("Alice") == "Hello Alice"
        
        with pytest.raises(TypeError):
            greet(123)
    
    def test_validates_return_type(self):
        """Valida el tipo de retorno."""
        @validate_types
        def get_number() -> int:
            return "not a number"  # Retorna tipo incorrecto
        
        with pytest.raises(TypeError):
            get_number()
    
    def test_validates_float_parameter(self):
        """Valida parámetros float."""
        @validate_types
        def calculate(value: float) -> float:
            return value * 2
        
        assert calculate(3.14) == 6.28
        
        # int puede ser promovido a float en Python
        assert calculate(3) == 6


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesOptional:
    """Tests para Optional types."""
    
    def test_optional_accepts_none(self):
        """Optional acepta None."""
        @validate_types
        def find_user(user_id: int) -> Optional[str]:
            return None if user_id != 1 else "Alice"
        
        assert find_user(1) == "Alice"
        assert find_user(2) is None
    
    def test_optional_accepts_value(self):
        """Optional acepta el tipo especificado."""
        @validate_types
        def get_age(name: str) -> Optional[int]:
            return 30 if name == "Alice" else None
        
        assert get_age("Alice") == 30
        assert get_age("Bob") is None
    
    def test_optional_parameter(self):
        """Parámetro opcional."""
        @validate_types
        def create_user(name: str, age: Optional[int] = None) -> str:
            if age:
                return f"{name} ({age})"
            return name
        
        assert create_user("Alice", 30) == "Alice (30)"
        assert create_user("Bob") == "Bob"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesUnion:
    """Tests para Union types."""
    
    def test_union_accepts_first_type(self):
        """Union acepta el primer tipo."""
        @validate_types
        def process_id(value: Union[int, str]) -> int:
            if isinstance(value, str):
                return int(value)
            return value
        
        assert process_id(123) == 123
    
    def test_union_accepts_second_type(self):
        """Union acepta el segundo tipo."""
        @validate_types
        def process_id(value: Union[int, str]) -> int:
            if isinstance(value, str):
                return int(value)
            return value
        
        assert process_id("456") == 456
    
    def test_union_rejects_other_types(self):
        """Union rechaza tipos no incluidos."""
        @validate_types
        def process_id(value: Union[int, str]) -> int:
            if isinstance(value, str):
                return int(value)
            return value
        
        with pytest.raises(TypeError):
            process_id(3.14)
    
    def test_pipe_union_syntax(self):
        """Sintaxis moderna de union con |."""
        @validate_types
        def process(value: int | str) -> str:
            return str(value)
        
        assert process(123) == "123"
        assert process("hello") == "hello"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesCollections:
    """Tests para tipos de colecciones."""
    
    def test_validates_list_container(self):
        """Valida que el contenedor sea una lista."""
        @validate_types
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)
        
        assert sum_numbers([1, 2, 3]) == 6
        
        with pytest.raises(TypeError):
            sum_numbers("123")
    
    def test_validates_dict_container(self):
        """Valida que el contenedor sea un dict."""
        @validate_types
        def get_keys(data: dict[str, int]) -> list:
            return list(data.keys())
        
        result = get_keys({"a": 1, "b": 2})
        assert result == ["a", "b"]
        
        with pytest.raises(TypeError):
            get_keys([("a", 1), ("b", 2)])
    
    def test_validates_tuple_container(self):
        """Valida que el contenedor sea una tupla."""
        @validate_types
        def process_pair(pair: tuple[int, int]) -> int:
            return pair[0] + pair[1]
        
        assert process_pair((1, 2)) == 3
        
        with pytest.raises(TypeError):
            process_pair([1, 2])


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesEdgeCases:
    """Tests para casos especiales."""
    
    def test_none_return_type(self):
        """Función que retorna None."""
        @validate_types
        def print_message(msg: str) -> None:
            print(msg)
        
        result = print_message("Hello")
        assert result is None
    
    def test_function_without_type_hints(self):
        """Función sin type hints no debe fallar."""
        @validate_types
        def no_hints(a, b):
            return a + b
        
        # No debe validar si no hay type hints
        assert no_hints(1, 2) == 3
        assert no_hints("a", "b") == "ab"
    
    def test_multiple_parameters(self):
        """Función con múltiples parámetros."""
        @validate_types
        def complex_func(a: int, b: str, c: float, d: bool) -> str:
            return f"{a}-{b}-{c}-{d}"
        
        result = complex_func(1, "test", 3.14, True)
        assert result == "1-test-3.14-True"
        
        with pytest.raises(TypeError):
            complex_func("1", "test", 3.14, True)


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestValidateTypesErrorMessages:
    """Tests para mensajes de error descriptivos."""
    
    def test_error_message_includes_parameter_name(self):
        """El error debe incluir el nombre del parámetro."""
        @validate_types
        def greet(name: str) -> str:
            return f"Hello {name}"
        
        with pytest.raises(TypeError) as exc_info:
            greet(123)
        
        assert "name" in str(exc_info.value).lower()
    
    def test_error_message_includes_expected_type(self):
        """El error debe incluir el tipo esperado."""
        @validate_types
        def add(a: int, b: int) -> int:
            return a + b
        
        with pytest.raises(TypeError) as exc_info:
            add("1", 2)
        
        error_msg = str(exc_info.value)
        assert "int" in error_msg or "str" in error_msg


@pytest.mark.skipif(SOLUTION_EXISTS, reason="Solo mostrar cuando no hay solución")
def test_solution_not_implemented():
    """Mensaje informativo cuando no hay solución."""
    pytest.skip(
        "La solución aún no está implementada. "
        "Completa advanced_exercise.py en el directorio exercises/"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
