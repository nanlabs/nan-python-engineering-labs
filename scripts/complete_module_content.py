#!/usr/bin/env python3
"""
Sistema inteligente para completar contenido de módulos masivamente.
Genera ejemplos, ejercicios y tests basados en el tema.
"""

from pathlib import Path

# Mapeo de temas específicos a ejemplos de código
TOPIC_EXAMPLES: dict[str, str] = {
    "abstract_base_classes": '''"""
Ejemplo de Abstract Base Classes (ABC) en Python.
Demuestra cómo definir interfaces y clases abstractas.
"""

from abc import ABC, abstractmethod
from typing import List


class Animal(ABC):
    """Clase abstracta que define la interfaz de un animal."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def make_sound(self) -> str:
        """Cada animal debe implementar su propio sonido."""
        pass

    @abstractmethod
    def move(self) -> str:
        """Cada animal se mueve de forma diferente."""
        pass

    def introduce(self) -> str:
        """Método concreto compartido por todos."""
        return f"Soy {self.name}"


class Dog(Animal):
    """Implementación concreta de Animal."""

    def make_sound(self) -> str:
        return "Woof! Woof!"

    def move(self) -> str:
        return "Corriendo en cuatro patas"


class Bird(Animal):
    """Otra implementación concreta."""

    def make_sound(self) -> str:
        return "Tweet! Tweet!"

    def move(self) -> str:
        return "Volando con alas"


def demonstrate_polymorphism(animals: List[Animal]) -> None:
    """Demuestra polimorfismo con ABC."""
    for animal in animals:
        print(f"{animal.introduce()}")
        print(f"  Sonido: {animal.make_sound()}")
        print(f"  Movimiento: {animal.move()}")
        print()


if __name__ == "__main__":
    # Crear instancias
    dog = Dog("Rex")
    bird = Bird("Tweety")

    # Demostrar polimorfismo
    demonstrate_polymorphism([dog, bird])

    # No se puede instanciar ABC directamente
    # animal = Animal("Generic")  # TypeError!
''',
    "protocol_structural_typing": '''"""
Protocoles y Structural Typing en Python.
PEP 544 - Interfaces implícitas sin herencia.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Protocolo que define la interfaz para objetos dibujables."""

    def draw(self) -> str:
        """Método que debe implementar cualquier clase dibujable."""
        ...


class Circle:
    """Clase que implementa el protocolo sin herencia explícita."""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Dibujando círculo de radio {self.radius}"


class Square:
    """Otra clase compatible con el protocolo."""

    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Dibujando cuadrado de lado {self.side}"


class NotDrawable:
    """Clase que NO implementa el protocolo."""
    pass


def render(shape: Drawable) -> None:
    """Función que acepta cualquier objeto que cumpla el protocolo."""
    print(shape.draw())


if __name__ == "__main__":
    # Ambos funcionan sin herencia explícita
    circle = Circle(5.0)
    square = Square(3.0)

    render(circle)
    render(square)

    # Verificación en runtime
    print(f"Circle es Drawable: {isinstance(circle, Drawable)}")

    not_drawable = NotDrawable()
    print(f"NotDrawable es Drawable: {isinstance(not_drawable, Drawable)}")

    # Type checker detectaría esto:
    # render(not_drawable)  # Error de tipo!
''',
    "generics_typevar": '''"""
Genéricos y TypeVar en Python.
Permite crear código type-safe reutilizable.
"""

from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Stack(Generic[T]):
    """Stack genérico type-safe."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """Añade un elemento al stack."""
        self._items.append(item)

    def pop(self) -> Optional[T]:
        """Extrae el último elemento."""
        return self._items.pop() if self._items else None

    def peek(self) -> Optional[T]:
        """Ve el último elemento sin extraerlo."""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        """Verifica si el stack está vacío."""
        return len(self._items) == 0


class Pair(Generic[K, V]):
    """Par clave-valor genérico."""

    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"Pair({self.key!r}, {self.value!r})"


def get_first_element(items: List[T]) -> Optional[T]:
    """Función genérica que retorna el primer elemento."""
    return items[0] if items else None


if __name__ == "__main__":
    # Stack de enteros
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"Pop: {int_stack.pop()}")  # 2

    # Stack de strings
    str_stack: Stack[str] = Stack()
    str_stack.push("hello")
    str_stack.push("world")
    print(f"Peek: {str_stack.peek()}")  # "world"

    # Pair con tipos diferentes
    pair = Pair[str, int]("edad", 30)
    print(pair)

    # Función genérica
    first_num = get_first_element([1, 2, 3])
    first_str = get_first_element(["a", "b", "c"])
    print(f"First number: {first_num}, First string: {first_str}")
''',
}

# Template para ejercicios básicos
EXERCISE_TEMPLATE = '''"""
Ejercicio: {topic_title}

Objetivo: Implementar y practicar {topic_name}

Instrucciones:
1. Lee atentamente los requisitos
2. Implementa las funciones/clases marcadas con TODO
3. Ejecuta los tests: pytest tests/
4. Tu solución debe ir en my_solution/

NO MODIFIQUES ESTE ARCHIVO. Copia a my_solution/ y trabaja allí.
"""

# TODO: Implementa tu solución aquí
# Sigue las especificaciones de los docstrings


def main():
    """
    Función principal para probar tu implementación.
    Añade tus propios casos de prueba.
    """
    # TODO: Añade código de prueba aquí
    pass


if __name__ == "__main__":
    main()
'''

# Template para tests
TEST_TEMPLATE = '''"""
Tests para {topic_name}
"""

import pytest
from pathlib import Path
import sys

# Añadir directorio padre al path para imports
parent_dir = Path(__file__).parent.parent / "my_solution"
sys.path.insert(0, str(parent_dir))


class Test{class_name}:
    """Suite de tests para {topic_name}."""

    def test_basic_functionality(self):
        """Test básico de funcionalidad."""
        # TODO: Implementa test básico
        pass

    def test_edge_cases(self):
        """Test de casos límite."""
        # TODO: Implementa tests de edge cases
        pass

    def test_error_handling(self):
        """Test de manejo de errores."""
        # TODO: Implementa tests de errores
        pass


def test_imports():
    """Verifica que los imports funcionan."""
    assert True  # Placeholder


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''


def create_example_file(topic_path: Path, topic_name: str) -> None:
    """Crea archivo de ejemplo si no existe."""
    examples_dir = topic_path / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)  # Asegurar que existe
    example_file = examples_dir / "example_basic.py"

    if not example_file.exists():
        if topic_name in TOPIC_EXAMPLES:
            content = TOPIC_EXAMPLES[topic_name]
        else:
            content = f'''"""
Ejemplo básico de {topic_name.replace("_", " ").title()}.
"""


def example_function():
    """
    Ejemplo funcional del concepto.
    """
    print("Ver referencias/ para documentación oficial")
    # TODO: Añadir ejemplo específico


if __name__ == "__main__":
    example_function()
'''
        example_file.write_text(content)
        print(f"  ✓ Ejemplo creado: {example_file.relative_to(topic_path.parent.parent)}")


def create_exercise_file(topic_path: Path, topic_name: str) -> None:
    """Crea archivo de ejercicio si no existe."""
    exercises_dir = topic_path / "exercises"
    exercises_dir.mkdir(parents=True, exist_ok=True)  # Asegurar que existe
    exercise_file = exercises_dir / "exercise_01.py"

    if not exercise_file.exists():
        topic_title = topic_name.replace("_", " ").title()
        content = EXERCISE_TEMPLATE.format(topic_title=topic_title, topic_name=topic_name)
        exercise_file.write_text(content)
        print(f"  ✓ Ejercicio creado: {exercise_file.relative_to(topic_path.parent.parent)}")


def create_test_file(topic_path: Path, topic_name: str) -> None:
    """Crea archivo de test si no existe."""
    tests_dir = topic_path / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)  # Asegurar que existe
    test_file = tests_dir / "test_basic.py"

    if not test_file.exists():
        class_name = "".join(word.capitalize() for word in topic_name.split("_"))
        content = TEST_TEMPLATE.format(
            topic_name=topic_name.replace("_", " "), class_name=class_name
        )
        test_file.write_text(content)
        print(f"  ✓ Test creado: {test_file.relative_to(topic_path.parent.parent)}")


def process_module(module_path: Path, module_name: str) -> int:
    """Procesa todos los temas de un módulo."""
    created = 0

    # Manejar patrones de diseño (con subcategorías)
    if "patrones" in module_name:
        subcats = [d for d in module_path.iterdir() if d.is_dir()]
        for subcat in subcats:
            topics = [t for t in subcat.iterdir() if t.is_dir()]
            for topic in topics:
                create_example_file(topic, topic.name)
                create_exercise_file(topic, topic.name)
                create_test_file(topic, topic.name)
                created += 3
    else:
        topics = [t for t in module_path.iterdir() if t.is_dir()]
        for topic in topics:
            create_example_file(topic, topic.name)
            create_exercise_file(topic, topic.name)
            create_test_file(topic, topic.name)
            created += 3

    return created


def main():
    """Completa contenido de todos los módulos."""
    base = Path(__file__).parent.parent
    modules = sorted([d for d in base.iterdir() if d.is_dir() and d.name[0].isdigit()])

    total_created = 0

    print("🚀 Completando contenido de módulos...\n")

    for module in modules:
        print(f"\n📦 Procesando {module.name}...")
        created = process_module(module, module.name)
        total_created += created
        print(f"   {created} archivos procesados")

    print(f"\n✅ Total: {total_created} archivos creados/verificados")
    print("\n⚠️  Recuerda: my_solution/ debe permanecer vacío para el usuario")


if __name__ == "__main__":
    main()
