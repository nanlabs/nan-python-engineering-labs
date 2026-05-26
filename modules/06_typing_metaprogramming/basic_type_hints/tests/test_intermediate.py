"""
Tests for the intermediate type hints exercise.
"""

import sys
from pathlib import Path

import pytest

# Add exercises directory to path
exercises_dir = Path(__file__).parent.parent / "exercises"
sys.path.insert(0, str(exercises_dir))

try:
    from intermediate_exercise import add_book, get_books_by_year, search_books

    SOLUTION_EXISTS = True
except (ImportError, AttributeError):
    SOLUTION_EXISTS = False


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestAddBook:
    """Tests for the add_book function."""

    def test_add_book_creates_dict(self):
        """Verify that add_book creates a dictionary."""
        book = add_book("1984", "George Orwell", 1949)
        assert isinstance(book, dict), "add_book must return a dictionary"

    def test_add_book_has_correct_keys(self):
        """Verify that the dictionary has the correct keys."""
        book = add_book("1984", "George Orwell", 1949)
        assert "title" in book, "Must have key 'title'"
        assert "author" in book, "Must have key 'author'"
        assert "year" in book, "Must have key 'year'"

    def test_add_book_correct_values(self):
        """Verify that the values are correct."""
        book = add_book("Dune", "Frank Herbert", 1965)
        assert book["title"] == "Dune"
        assert book["author"] == "Frank Herbert"
        assert book["year"] == 1965


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestSearchBooks:
    """Tests for the search_books function."""

    @pytest.fixture
    def sample_books(self):
        """Fixture with example books."""
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
            {"title": "Foundation", "author": "Isaac Asimov", "year": 1951},
        ]

    def test_search_by_author_lowercase(self, sample_books):
        """Search by author in lowercase."""
        results = search_books(sample_books, "orwell")
        assert len(results) == 2, "It must find 2 Orwell books"
        assert all("Orwell" in book["author"] for book in results)

    def test_search_by_author_uppercase(self, sample_books):
        """Search by author in uppercase (case-insensitive)."""
        results = search_books(sample_books, "ORWELL")
        assert len(results) == 2, "Search must be case-insensitive"

    def test_search_by_title(self, sample_books):
        """Search by title."""
        results = search_books(sample_books, "dune")
        assert len(results) == 1
        assert results[0]["title"] == "Dune"

    def test_search_partial_match(self, sample_books):
        """Search with a partial match."""
        results = search_books(sample_books, "farm")
        assert len(results) == 1
        assert results[0]["title"] == "Animal Farm"

    def test_search_no_results(self, sample_books):
        """Search with no results."""
        results = search_books(sample_books, "tolkien")
        assert results == [], "It must return an empty list when there are no results"

    def test_search_empty_list(self):
        """Search in an empty list."""
        results = search_books([], "orwell")
        assert results == [], "It must return an empty list"


@pytest.mark.skipif(not SOLUTION_EXISTS, reason="Solution not implemented yet")
class TestGetBooksByYear:
    """Tests for the get_books_by_year function."""

    @pytest.fixture
    def sample_books(self):
        """Fixture with example books."""
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
            {"title": "Foundation", "author": "Isaac Asimov", "year": 1951},
            {"title": "I, Robot", "author": "Isaac Asimov", "year": 1950},
        ]

    def test_get_books_single_result(self, sample_books):
        """Get books with a single result."""
        results = get_books_by_year(sample_books, 1949)
        assert results is not None, "It must not return None when there are results"
        assert len(results) == 1
        assert results[0]["title"] == "1984"

    def test_get_books_multiple_results(self, sample_books):
        """There can be multiple books from the same year."""
        # Add another book from 1950
        sample_books.append({"title": "Another Book", "author": "Someone", "year": 1950})
        results = get_books_by_year(sample_books, 1950)
        assert results is not None
        assert len(results) == 2

    def test_get_books_no_results(self, sample_books):
        """Return None if there are no books from that year."""
        results = get_books_by_year(sample_books, 2000)
        assert results is None, "It must return None when there are no results"

    def test_get_books_empty_list(self):
        """With an empty list it returns an empty list."""
        results = get_books_by_year([], 1949)
        assert results == [], "With an empty list it must return []"

    def test_get_books_old_year(self, sample_books):
        """Search by an old year."""
        results = get_books_by_year(sample_books, 1945)
        assert results is not None
        assert len(results) == 1
        assert results[0]["title"] == "Animal Farm"


@pytest.mark.skipif(SOLUTION_EXISTS, reason="Show only when there is no solution")
def test_solution_not_implemented():
    """Informational message when there is no solution."""
    pytest.skip(
        "The solution is not implemented yet. "
        "Complete intermediate_exercise.py in the exercises/ directory"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
