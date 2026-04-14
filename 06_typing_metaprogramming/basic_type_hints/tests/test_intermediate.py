"""
Tests para el ejercicio intermedio de type hints.
"""

import pytest
import sys
from pathlib import Path

# Añadir el directorio de ejercicios al path
exercises_dir = Path(__file__).parent.parent / "exercises"
sys.path.insert(0, str(exercises_dir))

try:
    from intermediate_exercise import add_book, search_books, get_books_by_year
    SOLUTION_EXISTS = True
except (ImportError, AttributeError):
    SOLUTION_EXISTS = False


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestAddBook:
    """Tests para la función add_book."""
    
    def test_add_book_creates_dict(self):
        """Verifica que add_book crea un diccionario."""
        book = add_book("1984", "George Orwell", 1949)
        assert isinstance(book, dict), "add_book debe retornar un diccionario"
    
    def test_add_book_has_correct_keys(self):
        """Verifica que el diccionario tiene las keys correctas."""
        book = add_book("1984", "George Orwell", 1949)
        assert "title" in book, "Debe tener key 'title'"
        assert "author" in book, "Debe tener key 'author'"
        assert "year" in book, "Debe tener key 'year'"
    
    def test_add_book_correct_values(self):
        """Verifica que los valores son correctos."""
        book = add_book("Dune", "Frank Herbert", 1965)
        assert book["title"] == "Dune"
        assert book["author"] == "Frank Herbert"
        assert book["year"] == 1965


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestSearchBooks:
    """Tests para la función search_books."""
    
    @pytest.fixture
    def sample_books(self):
        """Fixture con libros de ejemplo."""
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
            {"title": "Foundation", "author": "Isaac Asimov", "year": 1951},
        ]
    
    def test_search_by_author_lowercase(self, sample_books):
        """Busca por autor en minúsculas."""
        results = search_books(sample_books, "orwell")
        assert len(results) == 2, "Debe encontrar 2 libros de Orwell"
        assert all("Orwell" in book["author"] for book in results)
    
    def test_search_by_author_uppercase(self, sample_books):
        """Busca por autor en mayúsculas (case-insensitive)."""
        results = search_books(sample_books, "ORWELL")
        assert len(results) == 2, "Búsqueda debe ser case-insensitive"
    
    def test_search_by_title(self, sample_books):
        """Busca por título."""
        results = search_books(sample_books, "dune")
        assert len(results) == 1
        assert results[0]["title"] == "Dune"
    
    def test_search_partial_match(self, sample_books):
        """Busca con coincidencia parcial."""
        results = search_books(sample_books, "farm")
        assert len(results) == 1
        assert results[0]["title"] == "Animal Farm"
    
    def test_search_no_results(self, sample_books):
        """Busca sin resultados."""
        results = search_books(sample_books, "tolkien")
        assert results == [], "Debe retornar lista vacía si no hay resultados"
    
    def test_search_empty_list(self):
        """Busca en lista vacía."""
        results = search_books([], "orwell")
        assert results == [], "Debe retornar lista vacía"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solución no implementada aún")
class TestGetBooksByYear:
    """Tests para la función get_books_by_year."""
    
    @pytest.fixture
    def sample_books(self):
        """Fixture con libros de ejemplo."""
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
            {"title": "Foundation", "author": "Isaac Asimov", "year": 1951},
            {"title": "I, Robot", "author": "Isaac Asimov", "year": 1950},
        ]
    
    def test_get_books_single_result(self, sample_books):
        """Obtiene libros con un solo resultado."""
        results = get_books_by_year(sample_books, 1949)
        assert results is not None, "No debe retornar None si hay resultados"
        assert len(results) == 1
        assert results[0]["title"] == "1984"
    
    def test_get_books_multiple_results(self, sample_books):
        """Puede haber múltiples libros del mismo año."""
        # Añadir otro libro de 1950
        sample_books.append({"title": "Another Book", "author": "Someone", "year": 1950})
        results = get_books_by_year(sample_books, 1950)
        assert results is not None
        assert len(results) == 2
    
    def test_get_books_no_results(self, sample_books):
        """Retorna None si no hay libros de ese año."""
        results = get_books_by_year(sample_books, 2000)
        assert results is None, "Debe retornar None si no hay resultados"
    
    def test_get_books_empty_list(self):
        """Con lista vacía retorna lista vacía."""
        results = get_books_by_year([], 1949)
        assert results == [], "Con lista vacía debe retornar []"
    
    def test_get_books_old_year(self, sample_books):
        """Busca con año antiguo."""
        results = get_books_by_year(sample_books, 1945)
        assert results is not None
        assert len(results) == 1
        assert results[0]["title"] == "Animal Farm"


@pytest.mark.skipif(SOLUTION_EXISTS, reason="Solo mostrar cuando no hay solución")
def test_solution_not_implemented():
    """Mensaje informativo cuando no hay solución."""
    pytest.skip(
        "La solución aún no está implementada. "
        "Completa intermediate_exercise.py en el directorio exercises/"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
