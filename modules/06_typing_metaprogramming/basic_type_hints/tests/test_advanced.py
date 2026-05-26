"""
Tests for the advanced type hints exercise - validate_types decorator.
"""

import sys
from pathlib import Path

import pytest

# Add exercises directory to path
exercises_dir = Path(__file__).parent.parent / "exercises"
sys.path.insert(0, str(exercises_dir))

try:
    from advanced_exercise import validate_types

    SOLUTION_EXISTS = True
except (ImportError, AttributeError):
    SOLUTION_EXISTS = False


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesBasic:
    """Basic tests for the validate_types decorator."""

    def test_validates_int_parameter(self):
        """Validate int parameters."""

        @validate_types
        def add(a: int, b: int) -> int:
            return a + b

        # Should work with ints
        assert add(1, 2) == 3

        # Should fail with strings
        with pytest.raises(TypeError):
            add("1", "2")

    def test_validates_str_parameter(self):
        """Validate str parameters."""

        @validate_types
        def greet(name: str) -> str:
            return f"Hello {name}"

        assert greet("Alice") == "Hello Alice"

        with pytest.raises(TypeError):
            greet(123)

    def test_validates_return_type(self):
        """Validate the return type."""

        @validate_types
        def get_number() -> int:
            return "not a number"  # Returns incorrect type

        with pytest.raises(TypeError):
            get_number()

    def test_validates_float_parameter(self):
        """Validate float parameters."""

        @validate_types
        def calculate(value: float) -> float:
            return value * 2

        assert calculate(3.14) == 6.28

        # int can be promoted to float in Python
        assert calculate(3) == 6


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesOptional:
    """Tests for Optional types."""

    def test_optional_accepts_none(self):
        """Optional accepts None."""

        @validate_types
        def find_user(user_id: int) -> str | None:
            return None if user_id != 1 else "Alice"

        assert find_user(1) == "Alice"
        assert find_user(2) is None

    def test_optional_accepts_value(self):
        """Optional accepts the specified type."""

        @validate_types
        def get_age(name: str) -> int | None:
            return 30 if name == "Alice" else None

        assert get_age("Alice") == 30
        assert get_age("Bob") is None

    def test_optional_parameter(self):
        """Optional parameter."""

        @validate_types
        def create_user(name: str, age: int | None = None) -> str:
            if age:
                return f"{name} ({age})"
            return name

        assert create_user("Alice", 30) == "Alice (30)"
        assert create_user("Bob") == "Bob"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesUnion:
    """Tests for Union types."""

    def test_union_accepts_first_type(self):
        """Union accepts the first type."""

        @validate_types
        def process_id(value: int | str) -> int:
            if isinstance(value, str):
                return int(value)
            return value

        assert process_id(123) == 123

    def test_union_accepts_second_type(self):
        """Union accepts the second type."""

        @validate_types
        def process_id(value: int | str) -> int:
            if isinstance(value, str):
                return int(value)
            return value

        assert process_id("456") == 456

    def test_union_rejects_other_types(self):
        """Union rejects unsupported types."""

        @validate_types
        def process_id(value: int | str) -> int:
            if isinstance(value, str):
                return int(value)
            return value

        with pytest.raises(TypeError):
            process_id(3.14)

    def test_pipe_union_syntax(self):
        """Modern union syntax with |."""

        @validate_types
        def process(value: int | str) -> str:
            return str(value)

        assert process(123) == "123"
        assert process("hello") == "hello"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesCollections:
    """Tests for collection types."""

    def test_validates_list_container(self):
        """Validate that the container is a list."""

        @validate_types
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)

        assert sum_numbers([1, 2, 3]) == 6

        with pytest.raises(TypeError):
            sum_numbers("123")

    def test_validates_dict_container(self):
        """Validate that the container is a dict."""

        @validate_types
        def get_keys(data: dict[str, int]) -> list:
            return list(data.keys())

        result = get_keys({"a": 1, "b": 2})
        assert result == ["a", "b"]

        with pytest.raises(TypeError):
            get_keys([("a", 1), ("b", 2)])

    def test_validates_tuple_container(self):
        """Validate that the container is a tuple."""

        @validate_types
        def process_pair(pair: tuple[int, int]) -> int:
            return pair[0] + pair[1]

        assert process_pair((1, 2)) == 3

        with pytest.raises(TypeError):
            process_pair([1, 2])


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesEdgeCases:
    """Tests for special cases."""

    def test_none_return_type(self):
        """Function that returns None."""

        @validate_types
        def print_message(msg: str) -> None:
            print(msg)

        result = print_message("Hello")
        assert result is None

    def test_function_without_type_hints(self):
        """Function without type hints should not fail."""

        @validate_types
        def no_hints(a, b):
            return a + b

        # It should not validate when there are no type hints
        assert no_hints(1, 2) == 3
        assert no_hints("a", "b") == "ab"

    def test_multiple_parameters(self):
        """Function with multiple parameters."""

        @validate_types
        def complex_func(a: int, b: str, c: float, d: bool) -> str:
            return f"{a}-{b}-{c}-{d}"

        result = complex_func(1, "test", 3.14, True)
        assert result == "1-test-3.14-True"

        with pytest.raises(TypeError):
            complex_func("1", "test", 3.14, True)


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestValidateTypesErrorMessages:
    """Tests for descriptive error messages."""

    def test_error_message_includes_parameter_name(self):
        """The error must include the parameter name."""

        @validate_types
        def greet(name: str) -> str:
            return f"Hello {name}"

        with pytest.raises(TypeError) as exc_info:
            greet(123)

        assert "name" in str(exc_info.value).lower()

    def test_error_message_includes_expected_type(self):
        """The error must include the expected type."""

        @validate_types
        def add(a: int, b: int) -> int:
            return a + b

        with pytest.raises(TypeError) as exc_info:
            add("1", 2)

        error_msg = str(exc_info.value)
        assert "int" in error_msg or "str" in error_msg


@pytest.mark.skipif(SOLUTION_EXISTS, reason="Show only when there is no solution")
def test_solution_not_implemented():
    """Informational message when there is no solution."""
    pytest.skip(
        "The solution is not implemented yet. "
        "Complete advanced_exercise.py in the exercises/ directory"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
